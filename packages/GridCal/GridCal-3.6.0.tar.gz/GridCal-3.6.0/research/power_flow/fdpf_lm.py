"""
This is the traditional fast decoupled PF using an LM update strategy
"""
import numpy as np
np.set_printoptions(linewidth=320)
from numpy import zeros, ones, mod, conj, array, c_, r_, linalg, Inf, complex128
from itertools import product
from numpy.linalg import solve, inv
from scipy.sparse.linalg import factorized
from scipy.sparse import issparse, csc_matrix as sparse

# Set the complex precision to use
complex_type = complex128


import numpy as np
np.set_printoptions(linewidth=320)
from numpy import angle, conj, exp, r_, Inf
from numpy.linalg import norm
from scipy.sparse.linalg import splu
import time


def make_idn(nn):
    ii = np.linspace(0, nn - 1, nn)
    Idn = sparse((np.ones(nn), (ii, ii)), shape=(nn, nn))  # csr_matrix identity
    return Idn


def FDPFLM(Vbus, Sbus, Ibus, Ybus, B1, B2, pq, pv, pqpv, tol=1e-9, max_it=100):
    """
    Fast decoupled power flow
    Args:
        Vbus:
        Sbus:
        Ibus:
        Ybus:
        B1:
        B2:
        pq:
        pv:
        pqpv:
        tol:

    Returns:

    """

    start = time.time()

    npv = len(pv)
    npq = len(pq)
    npqpv = npq + npv

    # set voltage vector for the iterations
    voltage = Vbus.copy()
    Va = np.angle(voltage)
    Vm = np.abs(voltage)

    # Factorize B1 and B2
    J1 = B1[pqpv, :][:, pqpv]
    J2 = B2[pq, :][:, pq]

    # evaluate initial mismatch
    Scalc = voltage * conj(Ybus * voltage - Ibus)
    mis = Scalc - Sbus  # complex power mismatch
    incP = mis[pqpv].real
    incQ = mis[pq].imag
    normP = norm(incP, Inf)
    normQ = norm(incQ, Inf)

    # evaluate convergence
    if normP < tol and normQ < tol:
        converged = True
    else:
        converged = False

    # iterate
    iteration = 0

    Idn1 = make_idn(npqpv)
    Idn2 = make_idn(npq)

    # P iteration vars
    nu1 = 2.0
    f_prev1 = 1e9  # very large number
    Hp1 = J1.transpose()
    Hp2 = J1.dot(J1)
    lbmda1 = 1e-3 * Hp2.diagonal().max()
    A1 = splu(Hp2 + lbmda1 * Idn1)

    # Q iteration vars
    nu2 = 2.0
    f_prev2 = 1e9  # very large number
    Hq1 = J2.transpose()
    Hq2 = J2.dot(J2)
    lbmda2 = 1e-3 * Hq2.diagonal().max()
    A2 = splu(Hq2 + lbmda1 * Idn2)

    while not converged and iteration < max_it:

        iteration += 1

        # Solve P iteration
        rhs1 = Hp1.dot(incP)

        # solve voltage angles
        dVa = -A1.solve(rhs1)

        # objective function to minimize
        f1 = 0.5 * incP.dot(incP)

        # decision function
        rho1 = (f_prev1 - f1) / (0.5 * dVa.dot(lbmda1 * dVa + rhs1))

        # lambda update
        if rho1 > 0:
            lbmda1 *= max([1.0 / 3.0, 1 - (2 * rho1 - 1) ** 3])
            nu1 = 2.0

            # update voltage
            Va[pqpv] = Va[pqpv] + dVa

        else:
            lbmda1 *= nu1
            nu1 *= 2
            print('Not improving -> correcting lambda1 and nu1')

            # Solve Q iteration

            rhs2 = Hq1.dot(incQ)

            # Solve voltage modules
            dVm = -A2.solve(rhs2)

            # objective function to minimize
            f2 = 0.5 * incQ.dot(incQ)

            # decision function
            rho2 = (f_prev2 - f2) / (0.5 * dVm.dot(lbmda2 * dVm + rhs2))

            # lambda update
            if rho2 > 0:
                lbmda2 *= max([1.0 / 3.0, 1 - (2 * rho2 - 1) ** 3])
                nu2 = 2.0

                # update voltage
                Vm[pq] = Vm[pq] + dVm

            else:
                lbmda2 *= nu2
                nu2 *= 2
                print('Not improving -> correcting lambda2 and nu2')

        # evaluate mismatch
        voltage = Vm * exp(1j * Va)
        Scalc = voltage * conj(Ybus * voltage - Ibus)
        mis = Scalc - Sbus  # complex power mismatch
        incP = mis[pqpv].real
        incQ = mis[pq].imag
        normP = norm(incP, Inf)
        normQ = norm(incQ, Inf)

        if normP < tol and normQ < tol:
            converged = True

    # evaluate F(x)
    Scalc = voltage * conj(Ybus * voltage - Ibus)
    mis = Scalc - Sbus  # complex power mismatch
    F = r_[mis[pv].real, mis[pq].real, mis[pq].imag]  # concatenate again

    # check for convergence
    normF = norm(F, Inf)

    end = time.time()
    elapsed = end - start

    return voltage, converged, normF, Scalc, iteration, elapsed


if __name__ == '__main__':
    from GridCal.Engine.calculation_engine import *

    grid = MultiCircuit()
    # grid.load_file('lynn5buspq.xlsx')
    # grid.load_file('IEEE30.xlsx')
    grid.load_file('Illinois200Bus.xlsx')
    # grid.load_file('/home/santi/Documentos/GitHub/GridCal/Grids_and_profiles/grids/IEEE_57BUS.xls')
    # grid.load_file('/home/santi/Documentos/GitHub/GridCal/Grids_and_profiles/grids/1951 Bus RTE.xlsx')
    # grid.load_file('/home/santi/Documentos/GitHub/GridCal/Grids_and_profiles/grids/Pegasus 89 Bus.xlsx')

    grid.compile()

    circuit = grid.circuits[0]

    # print('\nYbus:\n', circuit.power_flow_input.Ybus.todense())
    # print('\nYseries:\n', circuit.power_flow_input.Yseries.todense())
    # print('\nYshunt:\n', circuit.power_flow_input.Yshunt)
    # print('\nSbus:\n', circuit.power_flow_input.Sbus)
    # print('\nIbus:\n', circuit.power_flow_input.Ibus)
    # print('\nVbus:\n', circuit.power_flow_input.Vbus)
    # print('\ntypes:\n', circuit.power_flow_input.types)
    # print('\npq:\n', circuit.power_flow_input.pq)
    # print('\npv:\n', circuit.power_flow_input.pv)
    # print('\nvd:\n', circuit.power_flow_input.ref)

    import time

    print('FDPF LM')
    start_time = time.time()

    v, converged_, err, Scalc, it, el = FDPFLM(Vbus=circuit.power_flow_input.Vbus,
                                               Sbus=circuit.power_flow_input.Sbus,
                                               Ibus=circuit.power_flow_input.Ibus,
                                               Ybus=circuit.power_flow_input.Ybus,
                                               B1=circuit.power_flow_input.B1,
                                               B2=circuit.power_flow_input.B2,
                                               pq=circuit.power_flow_input.pq,
                                               pv=circuit.power_flow_input.pv,
                                               pqpv=circuit.power_flow_input.pqpv,
                                               tol=1e-10,
                                               max_it=20)

    t1 = time.time() - start_time
    print("--- %s seconds ---" % (t1))

    print('V module:\t', np.abs(v), np.max(np.abs(v)), np.min(np.abs(v)))
    print('V angle: \t', np.angle(v))
    print('error: \t', err)

    # check the HELM solution: v against the hte LM power flow
    print('\nLM')
    options = PowerFlowOptions(SolverType.FASTDECOUPLED, verbose=False, robust=False, tolerance=1e-9)
    power_flow = PowerFlow(grid, options)

    start_time = time.time()
    power_flow.run()

    t2 = time.time() - start_time
    print("--- %s seconds ---" % (t2))
    vnr = circuit.power_flow_results.voltage

    print('V module:\t', np.abs(vnr), np.max(np.abs(vnr)), np.min(np.abs(vnr)))
    print('V angle: \t', np.angle(vnr))
    print('error: \t', circuit.power_flow_results.error)

    # check
    print('\nMethod 1 is ', t2/t1, 'times faster.')
    print('max diff:\t', np.max(v - vnr))