# This file is part of GridCal.
#
# GridCal is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# GridCal is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with GridCal.  If not, see <http://www.gnu.org/licenses/>.
import os
import sys
import networkx as nx
from PySide2.QtCore import *
from PySide2.QtSvg import QSvgGenerator
# import smopy
# from PIL.ImageQt import ImageQt


from GridCal.Engine.Devices import *
from GridCal.Gui.GuiFunctions import *
from GridCal.Engine.Simulations.Topology.topology_driver import reduce_grid_brute, reduce_buses
from GridCal.Engine.Core.multi_circuit import MultiCircuit
'''
Dependencies:

GridEditor
 |
  - EditorGraphicsView (Handles the drag and drop)
 |   |
  ---- DiagramScene
        |
         - MultiCircuit (Calculation engine)
        |
         - Graphic Objects: (BusGraphicItem, BranchGraphicItem, LoadGraphicItem, ...)


The graphic objects need to call the API objects and functions inside the MultiCircuit instance.
To do this the graphic objects call "parent.circuit.<function or object>"
'''

# Declare colors
ACTIVE = {'style': Qt.SolidLine, 'color': Qt.black}
DEACTIVATED = {'style': Qt.DashLine, 'color': Qt.gray}
EMERGENCY = {'style': Qt.SolidLine, 'color': QtCore.Qt.yellow}
OTHER = ACTIVE
FONT_SCALE = 1.9


class LineEditor(QDialog):

    def __init__(self, branch: Branch, Sbase=100):
        """
        Line Editor constructor
        :param branch: Branch object to update
        :param Sbase: Base power in MVA
        """
        super(LineEditor, self).__init__()

        # keep pointer to the line object
        self.branch = branch

        self.Sbase = Sbase

        self.setObjectName("self")

        self.setContextMenuPolicy(QtCore.Qt.NoContextMenu)

        self.layout = QVBoxLayout(self)

        # ------------------------------------------------------------------------------------------
        # Set the object values
        # ------------------------------------------------------------------------------------------
        Vf = self.branch.bus_from.Vnom
        Vt = self.branch.bus_to.Vnom

        Zbase = self.Sbase / (Vf * Vf)
        Ybase = 1 / Zbase

        R = self.branch.R * Zbase
        X = self.branch.X * Zbase
        G = self.branch.G * Ybase
        B = self.branch.B * Ybase

        I = self.branch.rate / Vf  # current in kA

        # ------------------------------------------------------------------------------------------

        # line length
        self.l_spinner = QDoubleSpinBox()
        self.l_spinner.setMinimum(0)
        self.l_spinner.setMaximum(9999999)
        self.l_spinner.setDecimals(6)
        self.l_spinner.setValue(1)

        # Max current
        self.i_spinner = QDoubleSpinBox()
        self.i_spinner.setMinimum(0)
        self.i_spinner.setMaximum(9999999)
        self.i_spinner.setDecimals(2)
        self.i_spinner.setValue(I)

        # R
        self.r_spinner = QDoubleSpinBox()
        self.r_spinner.setMinimum(0)
        self.r_spinner.setMaximum(9999999)
        self.r_spinner.setDecimals(6)
        self.r_spinner.setValue(R)

        # X
        self.x_spinner = QDoubleSpinBox()
        self.x_spinner.setMinimum(0)
        self.x_spinner.setMaximum(9999999)
        self.x_spinner.setDecimals(6)
        self.x_spinner.setValue(X)

        # G
        self.g_spinner = QDoubleSpinBox()
        self.g_spinner.setMinimum(0)
        self.g_spinner.setMaximum(9999999)
        self.g_spinner.setDecimals(6)
        self.g_spinner.setValue(G)

        # B
        self.b_spinner = QDoubleSpinBox()
        self.b_spinner.setMinimum(0)
        self.b_spinner.setMaximum(9999999)
        self.b_spinner.setDecimals(6)
        self.b_spinner.setValue(B)

        # accept button
        self.accept_btn = QPushButton()
        self.accept_btn.setText('Accept')
        self.accept_btn.clicked.connect(self.accept_click)

        # labels

        # add all to the GUI
        self.layout.addWidget(QLabel("L: Line length [Km]"))
        self.layout.addWidget(self.l_spinner)

        self.layout.addWidget(QLabel("Imax: Max. current [KA] @" + str(int(Vf)) + " [KV]"))
        self.layout.addWidget(self.i_spinner)

        self.layout.addWidget(QLabel("R: Resistance [Ohm/Km]"))
        self.layout.addWidget(self.r_spinner)

        self.layout.addWidget(QLabel("X: Inductance [Ohm/Km]"))
        self.layout.addWidget(self.x_spinner)

        self.layout.addWidget(QLabel("G: Conductance [S/Km]"))
        self.layout.addWidget(self.g_spinner)

        self.layout.addWidget(QLabel("B: Susceptance [S/Km]"))
        self.layout.addWidget(self.b_spinner)

        self.layout.addWidget(self.accept_btn)

        self.setLayout(self.layout)

        self.setWindowTitle('Line editor')

    def accept_click(self):
        """
        Set the values
        :return:
        """
        l = self.l_spinner.value()
        I = self.i_spinner.value()
        R = self.r_spinner.value() * l
        X = self.x_spinner.value() * l
        G = self.g_spinner.value() * l
        B = self.b_spinner.value() * l

        Vf = self.branch.bus_from.Vnom
        Vt = self.branch.bus_to.Vnom

        Sn = np.round(I * Vf, 2)  # nominal power in MVA = kA * kV

        Zbase = self.Sbase / (Vf * Vf)
        Ybase = 1.0 / Zbase

        self.branch.R = np.round(R / Zbase, 6)
        self.branch.X = np.round(X / Zbase, 6)
        self.branch.G = np.round(G / Ybase, 6)
        self.branch.B = np.round(B / Ybase, 6)
        self.branch.rate = Sn

        self.accept()


class TransformerEditor(QDialog):

    def __init__(self, branch: Branch, Sbase=100, modify_on_accept=True):
        """
        Transformer
        :param branch:
        :param Sbase:
        """
        super(TransformerEditor, self).__init__()

        # keep pointer to the line object
        self.branch = branch

        self.Sbase = Sbase

        self.modify_on_accept = modify_on_accept

        self.setObjectName("self")

        self.setContextMenuPolicy(QtCore.Qt.NoContextMenu)

        self.layout = QVBoxLayout(self)

        # ------------------------------------------------------------------------------------------
        # Set the object values
        # ------------------------------------------------------------------------------------------
        self.Vf = self.branch.bus_from.Vnom
        self.Vt = self.branch.bus_to.Vnom

        R = self.branch.R
        X = self.branch.X
        G = self.branch.G
        B = self.branch.B
        Sn = self.branch.rate

        zsc = np.sqrt(R * R + X * X)
        Vsc = 100.0 * zsc
        Pcu = R * Sn * 1000.0

        if abs(G) > 0.0 and abs(B) > 0.0:
            zl = 1.0 / complex(G, B)
            rfe = zl.real
            xm = zl.imag

            Pfe = 1000.0 * Sn / rfe

            k = 1 / (rfe * rfe) + 1 / (xm * xm)
            I0 = 100.0 * np.sqrt(k)
        else:
            Pfe = 0
            I0 = 0

        # ------------------------------------------------------------------------------------------

        # Sn
        self.sn_spinner = QDoubleSpinBox()
        self.sn_spinner.setMinimum(0)
        self.sn_spinner.setMaximum(9999999)
        self.sn_spinner.setDecimals(6)
        self.sn_spinner.setValue(Sn)

        # Pcu
        self.pcu_spinner = QDoubleSpinBox()
        self.pcu_spinner.setMinimum(0)
        self.pcu_spinner.setMaximum(9999999)
        self.pcu_spinner.setDecimals(6)
        self.pcu_spinner.setValue(Pcu)

        # Pfe
        self.pfe_spinner = QDoubleSpinBox()
        self.pfe_spinner.setMinimum(0)
        self.pfe_spinner.setMaximum(9999999)
        self.pfe_spinner.setDecimals(6)
        self.pfe_spinner.setValue(Pfe)

        # I0
        self.I0_spinner = QDoubleSpinBox()
        self.I0_spinner.setMinimum(0)
        self.I0_spinner.setMaximum(9999999)
        self.I0_spinner.setDecimals(6)
        self.I0_spinner.setValue(I0)

        # Vsc
        self.vsc_spinner = QDoubleSpinBox()
        self.vsc_spinner.setMinimum(0)
        self.vsc_spinner.setMaximum(9999999)
        self.vsc_spinner.setDecimals(6)
        self.vsc_spinner.setValue(Vsc)

        # accept button
        self.accept_btn = QPushButton()
        self.accept_btn.setText('Accept')
        self.accept_btn.clicked.connect(self.accept_click)

        # labels

        # add all to the GUI
        self.layout.addWidget(QLabel("Sn: Nominal power [MVA]"))
        self.layout.addWidget(self.sn_spinner)

        self.layout.addWidget(QLabel("Pcu: Copper losses [kW]"))
        self.layout.addWidget(self.pcu_spinner)

        self.layout.addWidget(QLabel("Pfe: Iron losses [kW]"))
        self.layout.addWidget(self.pfe_spinner)

        self.layout.addWidget(QLabel("I0: No load current [%]"))
        self.layout.addWidget(self.I0_spinner)

        self.layout.addWidget(QLabel("Vsc: Short circuit voltage [%]"))
        self.layout.addWidget(self.vsc_spinner)

        self.layout.addWidget(self.accept_btn)

        self.setLayout(self.layout)

        self.setWindowTitle('Transformer editor')

    def get_template(self):
        """
        Fabricate template values from the branch values
        :return: TransformerType instance
        """
        eps = 1e-20
        Vf = self.branch.bus_from.Vnom  # kV
        Vt = self.branch.bus_to.Vnom  # kV
        Sn = self.sn_spinner.value() + eps  # MVA
        Pcu = self.pcu_spinner.value() + eps  # kW
        Pfe = self.pfe_spinner.value() + eps  # kW
        I0 = self.I0_spinner.value() + eps  # %
        Vsc = self.vsc_spinner.value()  # %

        Pfe = eps if Pfe == 0.0 else Pfe
        I0 = eps if I0 == 0.0 else I0

        tpe = TransformerType(hv_nominal_voltage=Vf,
                              lv_nominal_voltage=Vt,
                              nominal_power=Sn,
                              copper_losses=Pcu,
                              iron_losses=Pfe,
                              no_load_current=I0,
                              short_circuit_voltage=Vsc,
                              gr_hv1=0.5,
                              gx_hv1=0.5)

        return tpe

    def accept_click(self):
        """
        Create transformer type and get the impedances
        :return:
        """

        if self.modify_on_accept:
            tpe = self.get_template()
            self.branch.apply_template(tpe, Sbase=self.Sbase)

        self.accept()


class LineUpdateMixin(object):

    def __init__(self, parent):
        super(LineUpdateMixin, self).__init__(parent)
        self.setFlag(QGraphicsItem.ItemSendsScenePositionChanges)

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemScenePositionHasChanged:
            self.parentItem().update_line(value)
        return super(LineUpdateMixin, self).itemChange(change, value)


class Polygon(LineUpdateMixin, QGraphicsPolygonItem):
    pass


class Square(LineUpdateMixin, QGraphicsRectItem):
    pass


class Circle(LineUpdateMixin, QGraphicsEllipseItem):
    pass


class QLine(LineUpdateMixin, QGraphicsLineItem):
    pass


class GeneralItem(object):

    def __init__(self):
        self.color = ACTIVE['color']
        self.width = 2
        self.style = ACTIVE['style']
        self.setBrush(QBrush(Qt.darkGray))
        self.setPen(QPen(self.color, self.width, self.style))

    def editParameters(self):
        pd = ParameterDialog(self.window())
        pd.exec_()

    def contextMenuEvent(self, event):
        menu = QMenu()

        ra3 = menu.addAction('Delete all the connections')
        ra3.triggered.connect(self.delete_all_connections)

        da = menu.addAction('Delete')
        da.triggered.connect(self.remove_)

        menu.exec_(event.screenPos())

    def rotate_clockwise(self):
        self.rotate(90)

    def rotate_counterclockwise(self):
        self.rotate(-90)

    def rotate(self, angle):

        pass

    def delete_all_connections(self):

        self.terminal.remove_all_connections()

    def remove_(self):
        """

        @return:
        """
        self.delete_all_connections()


class BranchGraphicItem(QGraphicsLineItem):

    def __init__(self, fromPort, toPort, diagramScene, width=5, branch: Branch = None):
        """

        @param fromPort:
        @param toPort:
        @param diagramScene:
        """
        QGraphicsLineItem.__init__(self, None)

        self.api_object = branch
        if self.api_object is not None:
            if self.api_object.active:
                self.style = ACTIVE['style']
                self.color = ACTIVE['color']
            else:
                self.style = DEACTIVATED['style']
                self.color = DEACTIVATED['color']
        else:
            self.style = OTHER['style']
            self.color = OTHER['color']
        self.width = width
        self.pen_width = width
        self.setPen(QPen(self.color, self.width, self.style))
        self.setFlag(self.ItemIsSelectable, True)
        self.setCursor(QCursor(Qt.PointingHandCursor))

        self.pos1 = None
        self.pos2 = None
        self.fromPort = None
        self.toPort = None
        self.diagramScene = diagramScene

        if fromPort:
            self.setFromPort(fromPort)

        if toPort:
            self.setToPort(toPort)

        # add transformer circles
        self.symbol_type = BranchType.Line
        self.symbol = None
        self.c0 = None
        self.c1 = None
        self.c2 = None
        if self.api_object is not None:
            self.update_symbol()

        # add the line and it possible children to the scene
        self.diagramScene.addItem(self)

        if fromPort and toPort:
            self.redraw()

    def remove_symbol(self):

        for elm in [self.symbol, self.c1, self.c2, self.c0]:
            if elm is not None:
                try:
                    self.diagramScene.removeItem(elm)
                    # sip.delete(elm)
                    elm = None
                except:
                    pass

    def update_symbol(self):
        """
        Make the branch symbol
        :return:
        """

        # remove the symbol of the branch
        self.remove_symbol()

        if self.api_object.branch_type == BranchType.Transformer:
            self.make_transformer_symbol()
            self.symbol_type = BranchType.Transformer

        elif self.api_object.branch_type == BranchType.Switch:
            self.make_switch_symbol()
            self.symbol_type = BranchType.Switch

        elif self.api_object.branch_type == BranchType.Reactance:
            self.make_reactance_symbol()
            self.symbol_type = BranchType.Switch

        else:
            self.symbol = None
            self.c0 = None
            self.c1 = None
            self.c2 = None
            self.symbol_type = BranchType.Line
            pass  # It is a line

    def make_transformer_symbol(self):
        """
        create the transformer simbol
        :return:
        """
        h = 80.0
        w = h
        d = w/2
        self.symbol = QGraphicsRectItem(QRectF(0, 0, w, h), parent=self)
        self.symbol.setPen(QtGui.QPen(Qt.transparent))

        self.c0 = QGraphicsEllipseItem(0, 0, d, d, parent=self.symbol)
        self.c1 = QGraphicsEllipseItem(0, 0, d, d, parent=self.symbol)
        self.c2 = QGraphicsEllipseItem(0, 0, d, d, parent=self.symbol)

        self.c0.setPen(QPen(Qt.transparent, self.width, self.style))
        self.c2.setPen(QPen(self.color, self.width, self.style))
        self.c1.setPen(QPen(self.color, self.width, self.style))

        self.c0.setBrush(QtGui.QBrush(Qt.white))
        self.c2.setBrush(QtGui.QBrush(Qt.white))

        self.c0.setPos(w * 0.35 - d / 2, h * 0.5 - d / 2)
        self.c1.setPos(w * 0.35 - d / 2, h * 0.5 - d / 2)
        self.c2.setPos(w * 0.65 - d / 2, h * 0.5 - d / 2)

        self.c0.setZValue(0)
        self.c1.setZValue(2)
        self.c2.setZValue(1)

    def make_switch_symbol(self):
        """
        Mathe the switch symbol
        :return:
        """
        h = 40.0
        w = h
        self.symbol = QGraphicsRectItem(QRectF(0, 0, w, h), parent=self)
        self.symbol.setPen(QPen(self.color, self.width, self.style))
        if self.api_object.active:
            self.symbol.setBrush(self.color)
        else:
            self.symbol.setBrush(QtGui.QBrush(Qt.white))

    def make_reactance_symbol(self):
        """
        Make the reactance symbol
        :return:
        """
        h = 40.0
        w = 2 * h
        self.symbol = QGraphicsRectItem(QRectF(0, 0, w, h), parent=self)
        self.symbol.setPen(QPen(self.color, self.width, self.style))
        self.symbol.setBrush(self.color)

    def setToolTipText(self, toolTip: str):
        """
        Set branch tool tip text
        Args:
            toolTip: text
        """
        self.setToolTip(toolTip)

        if self.symbol is not None:
            self.symbol.setToolTip(toolTip)

        if self.c0 is not None:
            self.c0.setToolTip(toolTip)
            self.c1.setToolTip(toolTip)
            self.c2.setToolTip(toolTip)

    def contextMenuEvent(self, event):
        """
        Show context menu
        @param event:
        @return:
        """
        if self.api_object is not None:
            menu = QMenu()

            pe = menu.addAction('Enable/Disable')
            pe.triggered.connect(self.enable_disable_toggle)

            menu.addSeparator()

            ra2 = menu.addAction('Delete')
            ra2.triggered.connect(self.remove)

            menu.addSeparator()

            ra3 = menu.addAction('Edit')
            ra3.triggered.connect(self.edit)

            menu.addSeparator()

            ra6 = menu.addAction('Plot profiles')
            ra6.triggered.connect(self.plot_profiles)

            if self.api_object.branch_type == BranchType.Transformer:

                ra3 = menu.addAction('Add to catalogue')
                ra3.triggered.connect(self.add_to_templates)

                menu.addSeparator()

                ra4 = menu.addAction('Tap up')
                ra4.triggered.connect(self.tap_up)

                ra5 = menu.addAction('Tap down')
                ra5.triggered.connect(self.tap_down)

            menu.addSeparator()

            re = menu.addAction('Reduce')
            re.triggered.connect(self.reduce)

            menu.exec_(event.screenPos())
        else:
            pass

    def mousePressEvent(self, QGraphicsSceneMouseEvent):
        """
        mouse press: display the editor
        :param QGraphicsSceneMouseEvent:
        :return:
        """

        mdl = BranchObjectModel([self.api_object], self.api_object.editable_headers,
                                parent=self.diagramScene.parent().object_editor_table,
                                editable=True, transposed=True,
                                non_editable_attributes=self.api_object.non_editable_attributes)

        self.diagramScene.parent().object_editor_table.setModel(mdl)

    def mouseDoubleClickEvent(self, event):
        """
        On double click, edit
        :param event:
        :return:
        """

        if self.api_object.branch_type in [BranchType.Transformer, BranchType.Line]:
            # trigger the editor
            self.edit()
        elif self.api_object.branch_type is BranchType.Switch:
            # change state
            self.enable_disable_toggle()

    def remove(self):
        """
        Remove this object in the diagram and the API
        @return:
        """
        self.diagramScene.circuit.delete_branch(self.api_object)
        self.diagramScene.removeItem(self)

    def reduce(self):
        """
        Reduce this branch
        """

        # get the index of the branch
        br_idx = self.diagramScene.circuit.branches.index(self.api_object)

        # call the reduction routine
        removed_branch, removed_bus, \
            updated_bus, updated_branches = reduce_grid_brute(self.diagramScene.circuit, br_idx)

        # remove the reduced branch
        removed_branch.graphic_obj.remove_symbol()
        self.diagramScene.removeItem(removed_branch.graphic_obj)

        # update the buses (the deleted one and the updated one)
        if removed_bus is not None:
            # merge the removed bus with the remaining one
            updated_bus.graphic_obj.merge(removed_bus.graphic_obj)

            # remove the updated bus children
            for g in updated_bus.graphic_obj.shunt_children:
                self.diagramScene.removeItem(g.nexus)
                self.diagramScene.removeItem(g)
            # re-draw the children
            updated_bus.graphic_obj.create_children_icons()

            # remove bus
            for g in removed_bus.graphic_obj.shunt_children:
                self.diagramScene.removeItem(g.nexus)  # remove the links between the bus and the children
            self.diagramScene.removeItem(removed_bus.graphic_obj)  # remove the bus and all the children contained

            #
            # updated_bus.graphic_obj.update()

        for br in updated_branches:
            # remove the branch from the schematic
            self.diagramScene.removeItem(br.graphic_obj)
            # add the branch to the schematic with the rerouting and all
            self.diagramScene.parent_.add_branch(br)
            # update both buses
            br.bus_from.graphic_obj.update()
            br.bus_to.graphic_obj.update()

    def remove_widget(self):
        """
        Remove this object in the diagram
        @return:
        """
        self.diagramScene.removeItem(self)

    def enable_disable_toggle(self):
        """

        @return:
        """
        if self.api_object is not None:
            if self.api_object.active:
                self.set_enable(False)
            else:
                self.set_enable(True)

    def set_enable(self, val=True):
        """
        Set the enable value, graphically and in the API
        @param val:
        @return:
        """
        self.api_object.active = val
        if self.api_object is not None:
            if self.api_object.active:
                self.style = ACTIVE['style']
                self.color = ACTIVE['color']
            else:
                self.style = DEACTIVATED['style']
                self.color = DEACTIVATED['color']
        else:
            self.style = OTHER['style']
            self.color = OTHER['color']

        # Switch coloring
        if self.symbol_type == BranchType.Switch:
            if self.api_object.active:
                self.symbol.setBrush(self.color)
            else:
                self.symbol.setBrush(Qt.white)

        # Set pen for everyone
        self.set_pen(QPen(self.color, self.width, self.style))

    def plot_profiles(self):
        """
        Plot the time series profiles
        @return:
        """
        # Ridiculously large call to get the main GUI that hosts this bus graphic
        # time series object from the last simulation
        ts = self.diagramScene.parent().parent().parent().parent().parent().parent().parent().parent().parent().parent().parent().parent().time_series

        # get the index of this object
        i = self.diagramScene.circuit.branches.index(self.api_object)

        # plot the profiles
        self.api_object.plot_profiles(time_series=ts, my_index=i)

    def setFromPort(self, fromPort):
        """
        Set the From terminal in a connection
        @param fromPort:
        @return:
        """
        self.fromPort = fromPort
        if self.fromPort:
            self.pos1 = fromPort.scenePos()
            self.fromPort.posCallbacks.append(self.setBeginPos)
            self.fromPort.parent.setZValue(0)

    def setToPort(self, toPort):
        """
        Set the To terminal in a connection
        @param toPort:
        @return:
        """
        self.toPort = toPort
        if self.toPort:
            self.pos2 = toPort.scenePos()
            self.toPort.posCallbacks.append(self.setEndPos)
            self.toPort.parent.setZValue(0)

    def setEndPos(self, endpos):
        """
        Set the starting position
        @param endpos:
        @return:
        """
        self.pos2 = endpos
        self.redraw()

    def setBeginPos(self, pos1):
        """
        Set the starting position
        @param pos1:
        @return:
        """
        self.pos1 = pos1
        self.redraw()

    def redraw(self):
        """
        Redraw the line with the given positions
        @return:
        """
        if self.pos1 is not None and self.pos2 is not None:

            # Set position
            self.setLine(QLineF(self.pos1, self.pos2))

            # set Z-Order (to the back)
            self.setZValue(-1)

            if self.api_object is not None:

                # if the object branch type is different from the current displayed type, change it
                if self.symbol_type != self.api_object.branch_type:
                    self.update_symbol()

                if self.api_object.branch_type == BranchType.Line:
                    pass

                elif self.api_object.branch_type == BranchType.Branch:
                    pass

                else:

                    # if the branch has a moveable symbol, move it
                    try:
                        h = self.pos2.y() - self.pos1.y()
                        b = self.pos2.x() - self.pos1.x()
                        ang = np.arctan2(h, b)
                        h2 = self.symbol.rect().height() / 2.0
                        w2 = self.symbol.rect().width() / 2.0
                        a = h2 * np.cos(ang) - w2 * np.sin(ang)
                        b = w2 * np.sin(ang) + h2 * np.cos(ang)

                        center = (self.pos1 + self.pos2) * 0.5 - QPointF(a, b)

                        transform = QTransform()
                        transform.translate(center.x(), center.y())
                        transform.rotate(np.rad2deg(ang))
                        self.symbol.setTransform(transform)

                    except Exception as ex:
                        print(ex)

    def set_pen(self, pen):
        """
        Set pen to all objects
        Args:
            pen:
        """
        self.setPen(pen)

        # Color the symbol only for switches
        if self.api_object.branch_type == BranchType.Switch:
            if self.symbol is not None:
                self.symbol.setPen(pen)

        elif self.api_object.branch_type == BranchType.Transformer:
            if self.c1 is not None:
                self.c1.setPen(pen)
                self.c2.setPen(pen)

    def edit(self):
        """
        Open the appropriate editor dialogue
        :return:
        """
        Sbase = self.diagramScene.circuit.Sbase

        if self.api_object.branch_type == BranchType.Transformer:
            dlg = TransformerEditor(self.api_object, Sbase, modify_on_accept=True)
            if dlg.exec_():
                pass

        elif self.api_object.branch_type == BranchType.Line:
            dlg = LineEditor(self.api_object, Sbase)
            if dlg.exec_():
                pass

    def add_to_templates(self):
        """
        Open the appropriate editor dialogue
        :return:
        """
        Sbase = self.diagramScene.circuit.Sbase

        if self.api_object.branch_type == BranchType.Transformer:

            if self.api_object.template is not None:
                # automatically pick the template
                if isinstance(self.api_object.template, TransformerType):
                    self.diagramScene.circuit.add_transformer_type(self.api_object.template)
                else:
                    # raise dialogue to set the template
                    dlg = TransformerEditor(self.api_object, Sbase, modify_on_accept=False)
                    if dlg.exec_():
                        tpe = dlg.get_template()
                        self.diagramScene.circuit.add_transformer_type(tpe)
            else:
                # raise dialogue to set the template
                dlg = TransformerEditor(self.api_object, Sbase, modify_on_accept=False)
                if dlg.exec_():
                    tpe = dlg.get_template()
                    self.diagramScene.circuit.add_transformer_type(tpe)

        elif self.api_object.branch_type == BranchType.Line:
            dlg = LineEditor(self.api_object, Sbase)
            if dlg.exec_():
                pass

    def tap_up(self):
        """
        Set one tap up
        """
        self.api_object.tap_up()

    def tap_down(self):
        """
        Set one tap down
        """
        self.api_object.tap_down()


class ParameterDialog(QDialog):

    def __init__(self, parent=None):
        super(ParameterDialog, self).__init__(parent)
        self.button = QPushButton('Ok', self)
        l = QVBoxLayout(self)
        l.addWidget(self.button)
        self.button.clicked.connect(self.OK)

    def OK(self):
        self.close()


class TerminalItem(QGraphicsRectItem):
    """
    Represents a connection point to a subsystem
    """

    def __init__(self, name, editor=None, parent=None, h=10, w=10):
        """

        @param name:
        @param editor:
        @param parent:
        """

        QGraphicsRectItem.__init__(self, QRectF(-6, -6, h, w), parent)
        self.setCursor(QCursor(QtCore.Qt.CrossCursor))

        # Properties:
        self.color = ACTIVE['color']
        self.pen_width = 2
        self.style = ACTIVE['style']
        self.setBrush(Qt.darkGray)
        self.setPen(QPen(self.color, self.pen_width, self.style))

        # terminal parent object
        self.parent = parent

        self.hosting_connections = list()

        self.editor = editor

        # Name:
        self.name = name
        self.posCallbacks = list()
        self.setFlag(self.ItemSendsScenePositionChanges, True)

    def process_callbacks(self, value):

        w = self.rect().width()
        h2 = self.rect().height() / 2.0
        n = len(self.posCallbacks)
        dx = w / (n + 1)
        for i, call_back in enumerate(self.posCallbacks):
            call_back(value + QPointF((i + 1) * dx, h2))

    def itemChange(self, change, value):
        """

        @param change:
        @param value: This is a QPointF object with the coordinates of the upper left corner of the TerminalItem
        @return:
        """
        if change == self.ItemScenePositionHasChanged:

            self.process_callbacks(value)

            return value

        else:
            return super(TerminalItem, self).itemChange(change, value)

    def mousePressEvent(self, event):
        """
        Start a connection
        Args:
            event:

        Returns:

        """
        self.editor.startConnection(self)
        self.hosting_connections.append(self.editor.started_branch)

    def remove_all_connections(self):
        """
        Removes all the terminal connections
        Returns:

        """
        n = len(self.hosting_connections)
        for i in range(n - 1, -1, -1):
            self.hosting_connections[i].remove_widget()
            self.hosting_connections.pop(i)


class HandleItem(QGraphicsEllipseItem):
    """
    A handle that can be moved by the mouse: Element to resize the boxes
    """

    def __init__(self, parent=None):
        """

        @param parent:
        """
        QGraphicsEllipseItem.__init__(self, QRectF(-4, -4, 8, 8), parent)

        self.posChangeCallbacks = []
        self.setBrush(Qt.red)
        self.setFlag(self.ItemIsMovable, True)
        self.setFlag(self.ItemSendsScenePositionChanges, True)
        self.setCursor(QCursor(Qt.SizeFDiagCursor))

    def itemChange(self, change, value):
        """

        @param change:
        @param value:
        @return:
        """
        if change == self.ItemPositionChange:
            x, y = value.x(), value.y()
            # TODO: make this a signal?
            # This cannot be a signal because this is not a QObject
            for cb in self.posChangeCallbacks:
                res = cb(x, y)
                if res:
                    x, y = res
                    value = QPointF(x, y)
            return value

        # Call superclass method:
        return super(HandleItem, self).itemChange(change, value)


class LoadGraphicItem(QGraphicsItemGroup):

    def __init__(self, parent, api_obj, diagramScene):
        """

        :param parent:
        :param api_obj:
        """
        super(LoadGraphicItem, self).__init__(parent)

        self.w = 20.0
        self.h = 20.0

        self.parent = parent

        self.api_object = api_obj

        self.diagramScene = diagramScene

        # Properties of the container:
        self.setFlags(self.ItemIsSelectable | self.ItemIsMovable)
        self.setCursor(QCursor(QtCore.Qt.PointingHandCursor))

        self.width = 4

        if self.api_object is not None:
            if self.api_object.active:
                self.style = ACTIVE['style']
                self.color = ACTIVE['color']
            else:
                self.style = DEACTIVATED['style']
                self.color = DEACTIVATED['color']
        else:
            self.style = OTHER['style']
            self.color = OTHER['color']

        # line to tie this object with the original bus (the parent)
        self.nexus = QGraphicsLineItem()
        self.nexus.setPen(QPen(self.color, self.width, self.style))
        parent.scene().addItem(self.nexus)

        # triangle
        self.glyph = Polygon(self)
        self.glyph.setPolygon(QPolygonF([QPointF(0, 0), QPointF(self.w, 0), QPointF(self.w / 2, self.h)]))
        self.glyph.setPen(QPen(self.color, self.width, self.style))
        self.addToGroup(self.glyph)

        self.setPos(self.parent.x(), self.parent.y() + 100)
        self.update_line(self.pos())

    def update_line(self, pos):
        """
        Update the line that joins the parent and this object
        :param pos: position of this object
        """
        parent = self.parentItem()
        rect = parent.rect()
        self.nexus.setLine(
            pos.x() + self.w / 2,
            pos.y() + 0,
            parent.x() + rect.width() / 2,
            parent.y() + parent.terminal.y() + 5,
        )
        self.setZValue(-1)
        self.nexus.setZValue(-1)

    def contextMenuEvent(self, event):
        """
        Display context menu
        @param event:
        @return:
        """
        menu = QMenu()

        da = menu.addAction('Delete')
        da.triggered.connect(self.remove)

        pe = menu.addAction('Enable/Disable')
        pe.triggered.connect(self.enable_disable_toggle)

        pa = menu.addAction('Plot profiles')
        pa.triggered.connect(self.plot)

        menu.exec_(event.screenPos())

    def remove(self):
        """
        Remove this element
        @return:
        """
        self.diagramScene.removeItem(self.nexus)
        self.diagramScene.removeItem(self)
        self.api_object.bus.loads.remove(self.api_object)

    def enable_disable_toggle(self):
        """

        @return:
        """
        if self.api_object is not None:
            if self.api_object.active:
                self.set_enable(False)
            else:
                self.set_enable(True)

    def set_enable(self, val=True):
        """
        Set the enable value, graphically and in the API
        @param val:
        @return:
        """
        self.api_object.active = val
        if self.api_object is not None:
            if self.api_object.active:
                self.style = ACTIVE['style']
                self.color = ACTIVE['color']
            else:
                self.style = DEACTIVATED['style']
                self.color = DEACTIVATED['color']
        else:
            self.style = OTHER['style']
            self.color = OTHER['color']
        self.glyph.setPen(QPen(self.color, self.width, self.style))

    def plot(self):

        fig = plt.figure(figsize=(10, 8))
        ax1 = fig.add_subplot(321)
        ax2 = fig.add_subplot(322)
        ax3 = fig.add_subplot(323)
        ax4 = fig.add_subplot(324)
        ax5 = fig.add_subplot(325)
        ax6 = fig.add_subplot(326)

        self.api_object.P_prof.plot(ax=ax1, linewidth=1)
        self.api_object.Ir_prof.plot(ax=ax2, linewidth=1)
        self.api_object.G_prof.plot(ax=ax3, linewidth=1)

        self.api_object.Q_prof.plot(ax=ax4, linewidth=1)
        self.api_object.Ii_prof.plot(ax=ax5, linewidth=1)
        self.api_object.B_prof.plot(ax=ax6, linewidth=1)

        ax1.set_title('Active power profile')
        ax2.set_title('Active current profile')
        ax3.set_title('Active impedance profile')
        ax4.set_title('Reactive power profile')
        ax5.set_title('Reactive current profile')
        ax6.set_title('Reactive impedance profile')

        ax1.set_ylabel('MW')
        ax2.set_ylabel('MW at V=1 p.u.')
        ax3.set_ylabel('MW at V=1 p.u.')
        ax4.set_ylabel('MVAr')
        ax5.set_ylabel('MW at V=1 p.u.')
        ax6.set_ylabel('MW at V=1 p.u.')

        plt.subplots_adjust(left=0.12, bottom=0.1, right=0.96, top=0.96, wspace=None, hspace=0.6)

        plt.show()

    def mousePressEvent(self, QGraphicsSceneMouseEvent):
        """
        mouse press: display the editor
        :param QGraphicsSceneMouseEvent:
        :return:
        """
        mdl = ObjectsModel([self.api_object], self.api_object.editable_headers,
                           parent=self.diagramScene.parent().object_editor_table, editable=True, transposed=True)
        self.diagramScene.parent().object_editor_table.setModel(mdl)


class ShuntGraphicItem(QGraphicsItemGroup):

    def __init__(self, parent, api_obj, diagramScene):
        """

        :param parent:
        :param api_obj:
        """
        super(ShuntGraphicItem, self).__init__(parent)

        self.w = 15.0
        self.h = 30.0

        self.parent = parent

        self.api_object = api_obj

        self.diagramScene = diagramScene

        self.width = 4

        if self.api_object is not None:
            if self.api_object.active:
                self.style = ACTIVE['style']
                self.color = ACTIVE['color']
            else:
                self.style = DEACTIVATED['style']
                self.color = DEACTIVATED['color']
        else:
            self.style = OTHER['style']
            self.color = OTHER['color']

        pen = QPen(self.color, self.width, self.style)

        # Properties of the container:
        self.setFlags(self.ItemIsSelectable | self.ItemIsMovable)
        self.setCursor(QCursor(QtCore.Qt.PointingHandCursor))

        # line to tie this object with the original bus (the parent)
        self.nexus = QGraphicsLineItem()
        self.nexus.setPen(QPen(self.color, self.width, self.style))
        parent.scene().addItem(self.nexus)

        self.lines = list()
        self.lines.append(QLineF(QPointF(self.w / 2, 0), QPointF(self.w / 2, self.h * 0.4)))
        self.lines.append(QLineF(QPointF(0, self.h * 0.4), QPointF(self.w, self.h * 0.4)))
        self.lines.append(QLineF(QPointF(0, self.h * 0.6), QPointF(self.w, self.h * 0.6)))
        self.lines.append(QLineF(QPointF(self.w / 2, self.h * 0.6), QPointF(self.w / 2, self.h)))
        self.lines.append(QLineF(QPointF(0, self.h * 1), QPointF(self.w, self.h * 1)))
        self.lines.append(QLineF(QPointF(self.w * 0.15, self.h * 1.1), QPointF(self.w * 0.85, self.h * 1.1)))
        self.lines.append(QLineF(QPointF(self.w * 0.3, self.h * 1.2), QPointF(self.w * 0.7, self.h * 1.2)))
        for l in self.lines:
            l1 = QLine(self)
            l1.setLine(l)
            l1.setPen(pen)
            self.addToGroup(l1)

        self.setPos(self.parent.x(), self.parent.y() + 100)
        self.update_line(self.pos())

    def update_line(self, pos):
        """
        Update the line that joins the parent and this object
        :param pos: position of this object
        """
        parent = self.parentItem()
        rect = parent.rect()
        self.nexus.setLine(
            pos.x() + self.w / 2,
            pos.y() + 0,
            parent.x() + rect.width() / 2,
            parent.y() + parent.terminal.y() + 5,
        )
        self.setZValue(-1)
        self.nexus.setZValue(-1)

    def contextMenuEvent(self, event):
        """
        Display context menu
        @param event:
        @return:
        """
        menu = QMenu()

        da = menu.addAction('Delete')
        da.triggered.connect(self.remove)

        pe = menu.addAction('Enable/Disable')
        pe.triggered.connect(self.enable_disable_toggle)

        pa = menu.addAction('Plot profile')
        pa.triggered.connect(self.plot)

        menu.exec_(event.screenPos())

    def remove(self):
        """
        Remove this element
        @return:
        """
        self.diagramScene.removeItem(self.nexus)
        self.diagramScene.removeItem(self)
        self.api_object.bus.shunts.remove(self.api_object)

    def enable_disable_toggle(self):
        """

        @return:
        """
        if self.api_object is not None:
            if self.api_object.active:
                self.set_enable(False)
            else:
                self.set_enable(True)

    def set_enable(self, val=True):
        """
        Set the enable value, graphically and in the API
        @param val:
        @return:
        """
        self.api_object.active = val
        if self.api_object is not None:
            if self.api_object.active:
                self.style = ACTIVE['style']
                self.color = ACTIVE['color']
            else:
                self.style = DEACTIVATED['style']
                self.color = DEACTIVATED['color']
        else:
            self.style = OTHER['style']
            self.color = OTHER['color']

        pen = QPen(self.color, self.width, self.style)

        for l in self.childItems():
            l.setPen(pen)

    def plot(self):
        """
        Plot API objects profiles
        """
        fig = plt.figure(figsize=(10, 6))
        ax1 = fig.add_subplot(111)

        if self.api_object.Yprof is not None:
            self.api_object.Yprof.plot(ax=ax1, linewidth=1)

        ax1.set_title('Admittance profile')

        ax1.set_ylabel('S (p.u.)')

        plt.subplots_adjust(left=0.12, bottom=0.1, right=0.96, top=0.96, wspace=None, hspace=0.6)

        plt.show()

    def mousePressEvent(self, QGraphicsSceneMouseEvent):
        """
        mouse press: display the editor
        :param QGraphicsSceneMouseEvent:
        :return:
        """
        mdl = ObjectsModel([self.api_object], self.api_object.editable_headers,
                           parent=self.diagramScene.parent().object_editor_table, editable=True, transposed=True)
        self.diagramScene.parent().object_editor_table.setModel(mdl)


class GeneratorGraphicItem(QGraphicsItemGroup):

    def __init__(self, parent, api_obj, diagramScene):
        """

        :param parent:
        :param api_obj:
        """
        super(GeneratorGraphicItem, self).__init__(parent)

        self.parent = parent

        self.api_object = api_obj

        self.diagramScene = diagramScene

        self.w = 40
        self.h = 40

        # Properties of the container:
        self.setFlags(self.ItemIsSelectable | self.ItemIsMovable)
        self.setCursor(QCursor(QtCore.Qt.PointingHandCursor))

        self.width = 4
        if self.api_object is not None:
            if self.api_object.active:
                self.style = ACTIVE['style']
                self.color = ACTIVE['color']
            else:
                self.style = DEACTIVATED['style']
                self.color = DEACTIVATED['color']
        else:
            self.style = OTHER['style']
            self.color = OTHER['color']

        # line to tie this object with the original bus (the parent)
        self.nexus = QGraphicsLineItem()
        self.nexus.setPen(QPen(self.color, self.width, self.style))
        parent.scene().addItem(self.nexus)

        pen = QPen(self.color, self.width, self.style)

        self.glyph = Circle(self)
        self.glyph.setRect(0, 0, self.h, self.w)
        self.glyph.setPen(pen)
        self.addToGroup(self.glyph)

        self.label = QGraphicsTextItem('G', parent=self.glyph)
        self.label.setDefaultTextColor(self.color)
        self.label.setPos(self.h / 4, self.w / 5)

        self.setPos(self.parent.x(), self.parent.y() + 100)
        self.update_line(self.pos())

    def update_line(self, pos):
        """
        Update the line that joins the parent and this object
        :param pos: position of this object
        """
        parent = self.parentItem()
        rect = parent.rect()
        self.nexus.setLine(
            pos.x() + self.w / 2,
            pos.y() + 0,
            parent.x() + rect.width() / 2,
            parent.y() + parent.terminal.y() + 5,
        )
        self.setZValue(-1)
        self.nexus.setZValue(-1)

    def contextMenuEvent(self, event):
        """
        Display context menu
        @param event:
        @return:
        """
        menu = QMenu()

        da = menu.addAction('Delete')
        da.triggered.connect(self.remove)

        pe = menu.addAction('Enable/Disable')
        pe.triggered.connect(self.enable_disable_toggle)

        pa = menu.addAction('Plot profiles')
        pa.triggered.connect(self.plot)

        menu.exec_(event.screenPos())

    def remove(self):
        """
        Remove this element
        @return:
        """
        self.diagramScene.removeItem(self.nexus)
        self.diagramScene.removeItem(self)
        self.api_object.bus.controlled_generators.remove(self.api_object)

    def enable_disable_toggle(self):
        """

        @return:
        """
        if self.api_object is not None:
            if self.api_object.active:
                self.set_enable(False)
            else:
                self.set_enable(True)

    def set_enable(self, val=True):
        """
        Set the enable value, graphically and in the API
        @param val:
        @return:
        """
        self.api_object.active = val
        if self.api_object is not None:
            if self.api_object.active:
                self.style = ACTIVE['style']
                self.color = ACTIVE['color']
            else:
                self.style = DEACTIVATED['style']
                self.color = DEACTIVATED['color']
        else:
            self.style = OTHER['style']
            self.color = OTHER['color']
        self.glyph.setPen(QPen(self.color, self.width, self.style))
        self.label.setDefaultTextColor(self.color)

    def plot(self):
        """
        Plot API objects profiles
        """
        fig = plt.figure(figsize=(10, 8))
        ax1 = fig.add_subplot(211)
        ax2 = fig.add_subplot(212)

        self.api_object.P_prof.plot(ax=ax1, linewidth=1)
        self.api_object.Vset_prof.plot(ax=ax2, linewidth=1)

        ax1.set_title('Active power profile')
        ax2.set_title('Set voltage profile')

        ax1.set_ylabel('MW')
        ax2.set_ylabel('V (p.u.)')

        plt.subplots_adjust(left=0.12, bottom=0.1, right=0.96, top=0.96, wspace=None, hspace=0.6)

        plt.show()

    def mousePressEvent(self, QGraphicsSceneMouseEvent):
        """
        mouse press: display the editor
        :param QGraphicsSceneMouseEvent:
        :return:
        """
        mdl = ObjectsModel([self.api_object], self.api_object.editable_headers,
                           parent=self.diagramScene.parent().object_editor_table, editable=True, transposed=True)
        self.diagramScene.parent().object_editor_table.setModel(mdl)


class StaticGeneratorGraphicItem(QGraphicsItemGroup):

    def __init__(self, parent, api_obj, diagramScene):
        """

        :param parent:
        :param api_obj:
        """
        super(StaticGeneratorGraphicItem, self).__init__(parent)

        self.parent = parent

        self.api_object = api_obj

        self.diagramScene = diagramScene

        self.w = 40
        self.h = 40

        # Properties of the container:
        self.setFlags(self.ItemIsSelectable | self.ItemIsMovable)
        self.setCursor(QCursor(QtCore.Qt.PointingHandCursor))

        self.width = 4
        if self.api_object is not None:
            if self.api_object.active:
                self.style = ACTIVE['style']
                self.color = ACTIVE['color']
            else:
                self.style = DEACTIVATED['style']
                self.color = DEACTIVATED['color']
        else:
            self.style = OTHER['style']
            self.color = OTHER['color']

        # line to tie this object with the original bus (the parent)
        self.nexus = QGraphicsLineItem()
        self.nexus.setPen(QPen(self.color, self.width, self.style))
        parent.scene().addItem(self.nexus)

        pen = QPen(self.color, self.width, self.style)

        self.glyph = Square(parent)
        self.glyph.setRect(0, 0, self.h, self.w)
        self.glyph.setPen(pen)
        self.addToGroup(self.glyph)

        self.label = QGraphicsTextItem('S', parent=self.glyph)
        self.label.setDefaultTextColor(self.color)
        self.label.setPos(self.h / 4, self.w / 5)

        self.setPos(self.parent.x(), self.parent.y() + 100)
        self.update_line(self.pos())

    def update_line(self, pos):
        """
        Update the line that joins the parent and this object
        :param pos: position of this object
        """
        parent = self.parentItem()
        rect = parent.rect()
        self.nexus.setLine(
            pos.x() + self.w / 2,
            pos.y() + 0,
            parent.x() + rect.width() / 2,
            parent.y() + parent.terminal.y() + 5,
        )
        self.setZValue(-1)
        self.nexus.setZValue(-1)

    def contextMenuEvent(self, event):
        """
        Display context menu
        @param event:
        @return:
        """
        menu = QMenu()

        da = menu.addAction('Delete')
        da.triggered.connect(self.remove)

        pe = menu.addAction('Enable/Disable')
        pe.triggered.connect(self.enable_disable_toggle)

        pa = menu.addAction('Plot profile')
        pa.triggered.connect(self.plot)

        menu.exec_(event.screenPos())

    def remove(self):
        """
        Remove this element
        @return:
        """
        self.diagramScene.removeItem(self.nexus)
        self.diagramScene.removeItem(self)
        self.api_object.bus.static_generators.remove(self.api_object)

    def enable_disable_toggle(self):
        """

        @return:
        """
        if self.api_object is not None:
            if self.api_object.active:
                self.set_enable(False)
            else:
                self.set_enable(True)

    def set_enable(self, val=True):
        """
        Set the enable value, graphically and in the API
        @param val:
        @return:
        """
        self.api_object.active = val
        if self.api_object is not None:
            if self.api_object.active:
                self.style = ACTIVE['style']
                self.color = ACTIVE['color']
            else:
                self.style = DEACTIVATED['style']
                self.color = DEACTIVATED['color']
        else:
            self.style = OTHER['style']
            self.color = OTHER['color']
        self.glyph.setPen(QPen(self.color, self.width, self.style))
        self.label.setDefaultTextColor(self.color)

    def plot(self):
        """
        Plot API objects profiles
        """
        fig = plt.figure(figsize=(10, 6))
        ax1 = fig.add_subplot(211)
        ax2 = fig.add_subplot(212)

        self.api_object.P_prof.plot(ax=ax1, linewidth=1)
        self.api_object.Q_prof.plot(ax=ax2, linewidth=1)

        ax1.set_title('Active power profile')
        ax1.set_ylabel('MW')

        ax1.set_title('Reactive power profile')
        ax1.set_ylabel('MVAr')

        plt.subplots_adjust(left=0.12, bottom=0.1, right=0.96, top=0.96, wspace=None, hspace=0.6)

        plt.show()

    def mousePressEvent(self, QGraphicsSceneMouseEvent):
        """
        mouse press: display the editor
        :param QGraphicsSceneMouseEvent:
        :return:
        """
        mdl = ObjectsModel([self.api_object], self.api_object.editable_headers,
                           parent=self.diagramScene.parent().object_editor_table, editable=True, transposed=True)
        self.diagramScene.parent().object_editor_table.setModel(mdl)


class BatteryGraphicItem(QGraphicsItemGroup):

    def __init__(self, parent, api_obj, diagramScene):
        """

        :param parent:
        :param api_obj:
        """
        super(BatteryGraphicItem, self).__init__(parent)

        self.parent = parent

        self.api_object = api_obj

        self.diagramScene = diagramScene

        self.w = 40
        self.h = 40

        # Properties of the container:
        self.setFlags(self.ItemIsSelectable | self.ItemIsMovable)
        self.setCursor(QCursor(QtCore.Qt.PointingHandCursor))

        self.width = 4
        if self.api_object is not None:
            if self.api_object.active:
                self.style = ACTIVE['style']
                self.color = ACTIVE['color']
            else:
                self.style = DEACTIVATED['style']
                self.color = DEACTIVATED['color']
        else:
            self.style = OTHER['style']
            self.color = OTHER['color']

        # line to tie this object with the original bus (the parent)
        self.nexus = QGraphicsLineItem()
        self.nexus.setPen(QPen(self.color, self.width, self.style))
        parent.scene().addItem(self.nexus)

        pen = QPen(self.color, self.width, self.style)

        self.glyph = Square(self)
        self.glyph.setRect(0, 0, self.h, self.w)
        self.glyph.setPen(pen)
        self.addToGroup(self.glyph)

        self.label = QGraphicsTextItem('B', parent=self.glyph)
        self.label.setDefaultTextColor(self.color)
        self.label.setPos(self.h / 4, self.w / 5)

        self.setPos(self.parent.x(), self.parent.y() + 100)
        self.update_line(self.pos())

    def update_line(self, pos):
        """
        Update the line that joins the parent and this object
        :param pos: position of this object
        """
        parent = self.parentItem()
        rect = parent.rect()
        self.nexus.setLine(
            pos.x() + self.w / 2,
            pos.y() + 0,
            parent.x() + rect.width() / 2,
            parent.y() + parent.terminal.y() + 5,
        )
        self.setZValue(-1)
        self.nexus.setZValue(-1)

    def contextMenuEvent(self, event):
        """
        Display context menu
        @param event:
        @return:
        """
        menu = QMenu()

        da = menu.addAction('Delete')
        da.triggered.connect(self.remove)

        pe = menu.addAction('Enable/Disable')
        pe.triggered.connect(self.enable_disable_toggle)

        pa = menu.addAction('Plot profiles')
        pa.triggered.connect(self.plot)

        menu.exec_(event.screenPos())

    def remove(self):
        """
        Remove this element
        @return:
        """
        self.diagramScene.removeItem(self.nexus)
        self.diagramScene.removeItem(self)
        self.api_object.bus.batteries.remove(self.api_object)

    def enable_disable_toggle(self):
        """

        @return:
        """
        if self.api_object is not None:
            if self.api_object.active:
                self.set_enable(False)
            else:
                self.set_enable(True)

    def set_enable(self, val=True):
        """
        Set the enable value, graphically and in the API
        @param val:
        @return:
        """
        self.api_object.active = val
        if self.api_object is not None:
            if self.api_object.active:
                self.style = ACTIVE['style']
                self.color = ACTIVE['color']
            else:
                self.style = DEACTIVATED['style']
                self.color = DEACTIVATED['color']
        else:
            self.style = OTHER['style']
            self.color = OTHER['color']
        self.glyph.setPen(QPen(self.color, self.width, self.style))
        self.label.setDefaultTextColor(self.color)

    def plot(self):
        """
        Plot API objects profiles
        """
        fig = plt.figure(figsize=(10, 8))
        ax1 = fig.add_subplot(411)
        ax2 = fig.add_subplot(412)
        ax3 = fig.add_subplot(413)
        ax4 = fig.add_subplot(414)

        self.api_object.P_prof.plot(ax=ax1, linewidth=1)
        self.api_object.Vset_prof.plot(ax=ax2, linewidth=1)
        self.api_object.power_array.plot(ax=ax3, linewidth=1)
        self.api_object.energy_array.plot(ax=ax4, linewidth=1)

        ax1.set_title('Active power profile')
        ax2.set_title('Set voltage profile')
        ax3.set_title('Active power profile')
        ax4.set_title('Energy profile')

        ax1.set_ylabel('MW')
        ax2.set_ylabel('V (p.u.)')
        ax3.set_ylabel('MW')
        ax4.set_ylabel('MWh')

        plt.subplots_adjust(left=0.12, bottom=0.1, right=0.96, top=0.96, wspace=None, hspace=0.6)

        plt.show()

    def mousePressEvent(self, QGraphicsSceneMouseEvent):
        """
        mouse press: display the editor
        :param QGraphicsSceneMouseEvent:
        :return:
        """
        mdl = ObjectsModel([self.api_object], self.api_object.editable_headers,
                           parent=self.diagramScene.parent().object_editor_table, editable=True, transposed=True)
        self.diagramScene.parent().object_editor_table.setModel(mdl)


class BusGraphicItem(QGraphicsRectItem):
    """
      Represents a block in the diagram
      Has an x and y and width and height
      width and height can only be adjusted with a tip in the lower right corner.

      - in and output ports
      - parameters
      - description
    """

    def __init__(self, diagramScene, name='Untitled', parent=None, index=0, editor=None,
                 bus: Bus = None, pos: QPoint = None):
        """

        @param diagramScene:
        @param name:
        @param parent:
        @param index:
        @param editor:
        """
        super(BusGraphicItem, self).__init__(parent)

        self.min_w = 180.0
        self.min_h = 20.0
        self.offset = 10
        self.h = bus.h if bus.h >= self.min_h else self.min_h
        self.w = bus.w if bus.w >= self.min_w else self.min_w

        self.api_object = bus

        self.diagramScene = diagramScene  # this is the parent that hosts the pointer to the circuit

        self.editor = editor

        # loads, shunts, generators, etc...
        self.shunt_children = list()

        # Enabled for short circuit
        self.sc_enabled = False
        self.pen_width = 4

        # index
        self.index = index

        if pos is not None:
            self.setPos(pos)

        # color
        if self.api_object is not None:
            if self.api_object.active:
                self.color = ACTIVE['color']
                self.style = ACTIVE['style']
            else:
                self.color = DEACTIVATED['color']
                self.style = DEACTIVATED['style']
        else:
            self.color = ACTIVE['color']
            self.style = ACTIVE['style']

        # Label:
        self.label = QGraphicsTextItem(bus.name, self)
        # self.label.setDefaultTextColor(QtCore.Qt.white)
        self.label.setDefaultTextColor(QtCore.Qt.black)
        self.label.setScale(FONT_SCALE)

        # square
        self.tile = QGraphicsRectItem(0, 0, self.min_h, self.min_h, self)
        self.tile.setOpacity(0.7)

        # connection terminals the block
        self.terminal = TerminalItem('s', parent=self, editor=self.editor)  # , h=self.h))
        self.terminal.setPen(QPen(Qt.transparent, self.pen_width, self.style))
        self.hosting_connections = list()

        # Create corner for resize:
        self.sizer = HandleItem(self.terminal)
        self.sizer.setPos(self.w, self.h)
        self.sizer.posChangeCallbacks.append(self.change_size)  # Connect the callback
        self.sizer.setFlag(self.ItemIsMovable)
        self.adapt()

        self.big_marker = None

        self.set_tile_color(self.color)

        self.setPen(QPen(Qt.transparent, self.pen_width, self.style))
        self.setBrush(Qt.transparent)
        self.setFlags(self.ItemIsSelectable | self.ItemIsMovable)
        self.setCursor(QCursor(QtCore.Qt.PointingHandCursor))

        # Update size:
        self.change_size(self.w, self.h)

    def mouseMoveEvent(self, event: 'QGraphicsSceneMouseEvent'):
        """
        On mouse move of this object...
        Args:
            event: QGraphicsSceneMouseEvent inherited
        """
        super().mouseMoveEvent(event)

        self.api_object.retrieve_graphic_position()

    def add_big_marker(self, color=Qt.red):
        """
        Add a big marker to the bus
        Args:
            color: Qt Color ot the marker
        """
        if self.big_marker is None:
            self.big_marker = QGraphicsEllipseItem(0, 0, 180, 180, parent=self)
            self.big_marker.setBrush(color)
            self.big_marker.setOpacity(0.5)

    def delete_big_marker(self):
        """
        Delete the big marker
        """
        if self.big_marker is not None:
            self.diagramScene.removeItem(self.big_marker)
            self.big_marker = None

    def set_tile_color(self, brush):
        """
        Set the color of the title
        Args:
            brush:  Qt Color
        """
        self.tile.setBrush(brush)
        self.terminal.setBrush(brush)

    def merge(self, other_bus_graphic):

        self.shunt_children += other_bus_graphic.shunt_children

    def update(self):
        """
        Update the object
        :return:
        """
        self.change_size(self.w, self.h)

    def change_size(self, w, h):
        """
        Resize block function
        @param w:
        @param h:
        @return:
        """
        # Limit the block size to the minimum size:
        h = self.min_h
        if w < self.min_w:
            w = self.min_w

        self.setRect(0.0, 0.0, w, h)
        self.h = h
        self.w = w

        # center label:
        rect = self.label.boundingRect()
        lw, lh = rect.width(), rect.height()
        lx = (w - lw) / 2
        ly = (h - lh) / 2 - lh * (FONT_SCALE - 1)
        self.label.setPos(lx, ly)

        # lower
        y0 = h + self.offset
        x0 = 0
        self.terminal.setPos(x0, y0)
        self.terminal.setRect(0.0, 0.0, w, 10)

        # Set text
        if self.api_object is not None:
            self.label.setPlainText(self.api_object.name)

        # rearrange children
        self.arrange_children()

        return w, h

    def arrange_children(self):
        """
        This function sorts the load and generators icons
        Returns:
            Nothing
        """
        y0 = self.h + 40
        n = len(self.shunt_children)
        inc_x = self.w / (n + 1)
        x = inc_x
        for elm in self.shunt_children:
            elm.setPos(x - elm.w / 2, y0)
            x += inc_x

        # Arrange line positions
        self.terminal.process_callbacks(self.pos() + self.terminal.pos())

    def create_children_icons(self):
        """
        Create the icons of the elements that are attached to the API bus object
        Returns:
            Nothing
        """
        for elm in self.api_object.loads:
            self.add_load(elm)

        for elm in self.api_object.static_generators:
            self.add_static_generator(elm)

        for elm in self.api_object.controlled_generators:
            self.add_generator(elm)

        for elm in self.api_object.shunts:
            self.add_shunt(elm)

        for elm in self.api_object.batteries:
            self.add_battery(elm)

        self.arrange_children()

    def contextMenuEvent(self, event):
        """
        Display context menu
        @param event:
        @return:
        """
        menu = QMenu()

        pe = menu.addAction('Enable/Disable')
        pe.triggered.connect(self.enable_disable_toggle)

        pl = menu.addAction('Plot profiles')
        pl.triggered.connect(self.plot_profiles)

        menu.addSeparator()

        ra3 = menu.addAction('Delete all the connections')
        ra3.triggered.connect(self.delete_all_connections)

        da = menu.addAction('Delete')
        da.triggered.connect(self.remove)

        re = menu.addAction('Reduce')
        re.triggered.connect(self.reduce)

        menu.addSeparator()

        al = menu.addAction('Add load')
        al.triggered.connect(self.add_load)

        ash = menu.addAction('Add shunt')
        ash.triggered.connect(self.add_shunt)

        acg = menu.addAction('Add generator')
        acg.triggered.connect(self.add_generator)

        asg = menu.addAction('Add static generator')
        asg.triggered.connect(self.add_static_generator)

        ab = menu.addAction('Add battery')
        ab.triggered.connect(self.add_battery)

        menu.addSeparator()

        arr = menu.addAction('Arrange')
        arr.triggered.connect(self.arrange_children)

        menu.addSeparator()

        sc = menu.addAction('Enable/Disable \nShort circuit')
        sc.triggered.connect(self.enable_disable_sc)

        menu.exec_(event.screenPos())

    def delete_all_connections(self):

        self.terminal.remove_all_connections()

    def reduce(self):
        """
        Reduce this bus
        :return:
        """
        reduce_buses(self.diagramScene.circuit, [self.api_object])

        self.remove()

    def remove(self):
        """
        Remove this element
        @return:
        """
        self.delete_all_connections()

        for g in self.shunt_children:
            self.diagramScene.removeItem(g.nexus)

        self.diagramScene.removeItem(self)
        self.diagramScene.circuit.delete_bus(self.api_object)

    def enable_disable_toggle(self):
        """
        Toggle bus element state
        @return:
        """
        if self.api_object is not None:
            self.api_object.active = not self.api_object.active
            # print('Enabled:', self.api_object.active)

            if self.api_object.active:

                self.set_tile_color(QBrush(ACTIVE['color']))

                for host in self.terminal.hosting_connections:
                    host.set_enable(val=True)
            else:
                self.set_tile_color(QBrush(DEACTIVATED['color']))

                for host in self.terminal.hosting_connections:
                    host.set_enable(val=False)

    def enable_disable_sc(self):
        """

        Returns:

        """
        if self.sc_enabled is True:
            # self.tile.setPen(QPen(QColor(ACTIVE['color']), self.pen_width))
            self.tile.setPen(QPen(Qt.transparent, self.pen_width))
            self.sc_enabled = False

        else:
            self.sc_enabled = True
            self.tile.setPen(QPen(QColor(EMERGENCY['color']), self.pen_width))

    def plot_profiles(self):
        """

        @return:
        """
        # Ridiculously large call to get the main GUI that hosts this bus graphic
        # time series object from the last simulation
        ts = self.diagramScene.parent().parent().parent().parent().parent().parent().parent().parent().parent().parent().parent().parent().time_series

        # get the index of this object
        i = self.diagramScene.circuit.buses.index(self.api_object)

        # get the time
        t = self.diagramScene.circuit.time_profile

        # plot the profiles
        if t is not None:
            self.api_object.plot_profiles(time_profile=t,
                                          ax_load=None,
                                          ax_voltage=None,
                                          time_series_driver=ts,
                                          my_index=i)

    def mousePressEvent(self, event):
        """
        mouse press: display the editor
        :param QGraphicsSceneMouseEvent:
        :return:
        """
        mdl = ObjectsModel([self.api_object], self.api_object.editable_headers,
                           parent=self.diagramScene.parent().object_editor_table, editable=True, transposed=True)
        self.diagramScene.parent().object_editor_table.setModel(mdl)

    def mouseDoubleClickEvent(self, event):
        """
        Mouse double click
        :param event: event object
        """
        self.adapt()

    def adapt(self):
        """
        Set the bus width according to the label text
        """
        # Todo: fix the resizing on double click
        h = self.terminal.boundingRect().height()
        w = len(self.api_object.name) * 8 + 10
        self.change_size(w=w, h=h)
        self.sizer.setPos(w, self.h)

    def add_load(self, api_obj=None):
        """

        Returns:

        """
        if api_obj is None or type(api_obj) is bool:
            api_obj = self.diagramScene.circuit.add_load(self.api_object)

        _grph = LoadGraphicItem(self, api_obj, self.diagramScene)
        api_obj.graphic_obj = _grph
        self.shunt_children.append(_grph)
        self.arrange_children()

    def add_shunt(self, api_obj=None):
        """

        Returns:

        """
        if api_obj is None or type(api_obj) is bool:
            api_obj = self.diagramScene.circuit.add_shunt(self.api_object)

        _grph = ShuntGraphicItem(self, api_obj, self.diagramScene)
        api_obj.graphic_obj = _grph
        self.shunt_children.append(_grph)
        self.arrange_children()

    def add_generator(self, api_obj=None):
        """

        Returns:

        """
        if api_obj is None or type(api_obj) is bool:
            api_obj = self.diagramScene.circuit.add_generator(self.api_object)

        _grph = GeneratorGraphicItem(self, api_obj, self.diagramScene)
        api_obj.graphic_obj = _grph
        self.shunt_children.append(_grph)
        self.arrange_children()

    def add_static_generator(self, api_obj=None):
        """

        Returns:

        """
        if api_obj is None or type(api_obj) is bool:
            api_obj = self.diagramScene.circuit.add_static_generator(self.api_object)

        _grph = StaticGeneratorGraphicItem(self, api_obj, self.diagramScene)
        api_obj.graphic_obj = _grph
        self.shunt_children.append(_grph)
        self.arrange_children()

    def add_battery(self, api_obj=None):
        """

        Returns:

        """
        if api_obj is None or type(api_obj) is bool:
            api_obj = self.diagramScene.circuit.add_battery(self.api_object)

        _grph = BatteryGraphicItem(self, api_obj, self.diagramScene)
        api_obj.graphic_obj = _grph
        self.shunt_children.append(_grph)
        self.arrange_children()


class MapWidget(QGraphicsRectItem):

    def __init__(self, scene: QGraphicsScene, view: QGraphicsView, lat0=42, lon0=55, zoom=3):
        super(MapWidget, self).__init__(None)

        self.scene = scene
        self.view = view

        self.setFlags(self.ItemIsMovable)
        self.image = None
        self.img = None

        self.pen_width = 4
        # Properties of the rectangle:
        self.color = ACTIVE['color']
        self.style = ACTIVE['style']
        self.setBrush(QBrush(Qt.darkGray))
        self.setPen(QPen(self.color, self.pen_width, self.style))
        self.setBrush(self.color)

        self.scene.addItem(self)

        self.h = view.size().height()
        self.w = view.size().width()

        self.lat0 = lat0
        self.lon0 = lon0
        self.zoom = zoom

        # Create corner for resize:
        self.sizer = HandleItem(self)
        self.sizer.setPos(self.w, self.h)
        self.sizer.posChangeCallbacks.append(self.change_size)  # Connect the callback
        # self.sizer.setFlag(self.sizer.ItemIsSelectable, True)

        self.change_size(self.w, self.h)
        self.setPos(0, self.h)

        # self.load_map()

    def change_size(self, w, h):
        """
        Resize block function
        @param w:
        @param h:
        @return:
        """

        self.setRect(0.0, 0.0, w, h)
        self.h = h
        self.w = w
        self.repaint()

        return w, h

    def load_map(self, lat0=42, lon0=55, zoom=3):
        """
        Load a map image into the widget
        :param lat0:
        :param lon0:
        :param zoom: 1~14
        """
        # store coordinates
        self.lat0 = lat0
        self.lon0 = lon0
        self.zoom = zoom

    def repaint(self):
        """
        Reload with the last parameters
        """
        self.load_map(self.lat0, self.lon0, self.zoom)

    def paint(self, painter, option, widget=None):
        """
        Action that happens on widget repaint
        :param painter:
        :param option:
        :param widget:
        """
        if self.image is not None:
            painter.drawPixmap(QPoint(0, 0), self.image)
            self.scene.update()


class EditorGraphicsView(QGraphicsView):

    def __init__(self, scene, parent=None, editor=None, lat0=42, lon0=55, zoom=3):
        """
        Editor where the diagram is displayed
        @param scene: DiagramScene object
        @param parent:
        @param editor:
        """
        QGraphicsView.__init__(self, scene, parent)

        self.setDragMode(QGraphicsView.RubberBandDrag)
        self.setRubberBandSelectionMode(Qt.IntersectsItemShape)
        self.setMouseTracking(True)
        self.setInteractive(True)
        self.scene_ = scene
        self.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)
        self.editor = editor
        self.last_n = 1
        self.setAlignment(Qt.AlignCenter)

        self.map = MapWidget(self.scene_, self, lat0, lon0, zoom)

    def adapt_map_size(self):
        w = self.size().width()
        h = self.size().height()
        print('EditorGraphicsView size: ', w, h)
        self.map.change_size(w, h)

    def view_map(self, flag=True):
        """

        :param flag:
        :return:
        """
        self.map.setVisible(flag)

    def dragEnterEvent(self, event):
        """

        @param event:
        @return:
        """
        if event.mimeData().hasFormat('component/name'):
            event.accept()

    def dragMoveEvent(self, event):
        """
        Move element
        @param event:
        @return:
        """
        if event.mimeData().hasFormat('component/name'):
            event.accept()

    def dropEvent(self, event):
        """
        Create an element
        @param event:
        @return:
        """
        if event.mimeData().hasFormat('component/name'):
            obj_type = event.mimeData().data('component/name')
            elm = None
            data = QByteArray()
            stream = QDataStream(data, QIODevice.WriteOnly)
            stream.writeQString('Bus')
            if obj_type == data:
                name = 'Bus ' + str(self.last_n)
                self.last_n += 1
                obj = Bus(name=name)
                elm = BusGraphicItem(diagramScene=self.scene(), name=name, editor=self.editor, bus=obj)
                obj.graphic_obj = elm
                self.scene_.circuit.add_bus(obj)  # weird but it's the only way to have graphical-API communication

            if elm is not None:
                elm.setPos(self.mapToScene(event.pos()))
                self.scene_.addItem(elm)

    def wheelEvent(self, event):
        """
        Zoom
        @param event:
        @return:
        """
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)

        # Scale the view / do the zoom
        scale_factor = 1.15
        # print(event.angleDelta().x(), event.angleDelta().y(), event.angleDelta().manhattanLength() )
        if event.angleDelta().y() > 0:
            # Zoom in
            self.scale(scale_factor, scale_factor)

        else:
            # Zooming out
            self.scale(1.0 / scale_factor, 1.0 / scale_factor)

    def add_bus(self, bus: Bus, explode_factor=1.0):
        """
        Add bus
        Args:
            bus: GridCal Bus object
            explode_factor: factor to position the node
        """
        elm = BusGraphicItem(diagramScene=self.scene(), name=bus.name, editor=self.editor, bus=bus)
        elm.setPos(self.mapToScene(QPoint(bus.x * explode_factor, bus.y * explode_factor)))
        self.scene_.addItem(elm)
        return elm


class LibraryModel(QStandardItemModel):
    """
    Items model to host the draggable icons
    """

    def __init__(self, parent=None):
        """
        Items model to host the draggable icons
        @param parent:
        """
        QStandardItemModel.__init__(self, parent)

    def mimeTypes(self):
        """

        @return:
        """
        return ['component/name']

    def mimeData(self, idxs):
        """

        @param idxs:
        @return:
        """
        mimedata = QMimeData()
        for idx in idxs:
            if idx.isValid():
                txt = self.data(idx, Qt.DisplayRole)

                data = QByteArray()
                stream = QDataStream(data, QIODevice.WriteOnly)
                stream.writeQString(txt)

                mimedata.setData('component/name', data)
        return mimedata


class DiagramScene(QGraphicsScene):

    def __init__(self, parent=None, circuit: MultiCircuit = None):
        """

        @param parent:
        """
        super(DiagramScene, self).__init__(parent)
        self.parent_ = parent
        self.circuit = circuit
        # self.setBackgroundBrush(QtCore.Qt.red)

    def mouseMoveEvent(self, mouseEvent):
        """

        @param mouseEvent:
        @return:
        """
        self.parent_.sceneMouseMoveEvent(mouseEvent)
        super(DiagramScene, self).mouseMoveEvent(mouseEvent)

    def mouseReleaseEvent(self, mouseEvent):
        """

        @param mouseEvent:
        @return:
        """
        self.parent_.sceneMouseReleaseEvent(mouseEvent)
        super(DiagramScene, self).mouseReleaseEvent(mouseEvent)


class ObjectFactory(object):

    def get_box(self):
        """

        @return:
        """
        pixmap = QPixmap(40, 40)
        pixmap.fill()
        painter = QPainter(pixmap)
        painter.fillRect(0, 0, 40, 40, Qt.black)
        painter.end()

        return QIcon(pixmap)

    def get_circle(self):
        """

        @return:
        """
        pixmap = QPixmap(40, 40)
        pixmap.fill()
        painter = QPainter(pixmap)

        painter.setBrush(Qt.red)
        painter.drawEllipse(0, 0, 40, 40)

        painter.end()

        return QIcon(pixmap)


class GridEditor(QSplitter):

    def __init__(self, circuit: MultiCircuit, lat0=42, lon0=55, zoom=3):
        """
        Creates the Diagram Editor
        Args:
            circuit: Circuit that is handling
        """
        QSplitter.__init__(self)

        # store a reference to the multi circuit instance
        self.circuit = circuit

        # nodes distance "explosion" factor
        self.expand_factor = 1.5

        self.branch_editor_count = 1

        # Widget layout and child widgets:
        self.horizontalLayout = QHBoxLayout(self)
        self.object_editor_table = QTableView(self)
        self.libraryBrowserView = QListView(self)
        self.libraryModel = LibraryModel(self)
        self.libraryModel.setColumnCount(1)

        # Create an icon with an icon:
        object_factory = ObjectFactory()

        # initialize library of items
        self.libItems = list()
        self.libItems.append(QStandardItem(object_factory.get_box(), 'Bus'))
        for i in self.libItems:
            self.libraryModel.appendRow(i)

        # set the objects list
        self.object_types = ['Buses', 'Branches', 'Loads', 'Static Generators',
                             'Generators', 'Batteries', 'Shunts']

        self.catalogue_types = ['Wires', 'Overhead lines', 'Underground lines', 'Sequence lines', 'Transformers']

        # Actual libraryView object
        self.libraryBrowserView.setModel(self.libraryModel)
        self.libraryBrowserView.setViewMode(self.libraryBrowserView.ListMode)
        self.libraryBrowserView.setDragDropMode(self.libraryBrowserView.DragOnly)

        # create all the schematic objects and replace the existing ones
        self.diagramScene = DiagramScene(self, circuit)  # scene to add to the QGraphicsView
        self.diagramView = EditorGraphicsView(self.diagramScene, parent=self, editor=self,
                                              lat0=lat0, lon0=lon0, zoom=zoom)

        # create the grid name editor
        self.frame1 = QFrame()
        self.frame1_layout = QVBoxLayout()
        self.frame1_layout.setContentsMargins(0, 0, 0, 0)

        self.name_editor_frame = QFrame()
        self.name_layout = QHBoxLayout()
        self.name_layout.setContentsMargins(0, 0, 0, 0)

        self.name_label = QLineEdit()
        self.name_label.setText(self.circuit.name)
        self.name_layout.addWidget(self.name_label)
        self.name_editor_frame.setLayout(self.name_layout)

        self.frame1_layout.addWidget(self.name_editor_frame)
        self.frame1_layout.addWidget(self.libraryBrowserView)
        self.frame1.setLayout(self.frame1_layout)

        # Add the two objects into a layout
        splitter2 = QSplitter(self)
        splitter2.addWidget(self.frame1)
        splitter2.addWidget(self.object_editor_table)
        splitter2.setOrientation(Qt.Vertical)
        self.addWidget(splitter2)
        self.addWidget(self.diagramView)

        # factor 1:10
        splitter2.setStretchFactor(0, 1)
        splitter2.setStretchFactor(1, 10)

        self.started_branch = None

        self.setStretchFactor(0, 1)
        self.setStretchFactor(1, 10)

    def startConnection(self, port: TerminalItem):
        """
        Start the branch creation
        @param port:
        @return:
        """
        self.started_branch = BranchGraphicItem(port, None, self.diagramScene)
        self.started_branch.bus_from = port.parent
        port.setZValue(0)
        # if self.diagramView.map.isVisible():
        #     self.diagramView.map.setZValue(-1)
        port.process_callbacks(port.parent.pos() + port.pos())

    def sceneMouseMoveEvent(self, event):
        """

        @param event:
        @return:
        """
        if self.started_branch:
            pos = event.scenePos()
            self.started_branch.setEndPos(pos)

    def sceneMouseReleaseEvent(self, event):
        """
        Finalize the branch creation if its drawing ends in a terminal
        @param event:
        @return:
        """
        # Clear or finnish the started connection:
        if self.started_branch:
            pos = event.scenePos()
            items = self.diagramScene.items(pos)  # get the item (the terminal) at the mouse position

            for item in items:
                if type(item) is TerminalItem:  # connect only to terminals
                    if item.parent is not self.started_branch.fromPort.parent:  # forbid connecting to itself

                        # if type(item.parent) is not type(self.startedConnection.fromPort.parent):
                        #  forbid same type connections

                        self.started_branch.setToPort(item)
                        item.hosting_connections.append(self.started_branch)
                        # self.started_branch.setZValue(-1)
                        self.started_branch.bus_to = item.parent
                        name = 'Branch ' + str(self.branch_editor_count)
                        v1 = self.started_branch.bus_from.api_object.Vnom
                        v2 = self.started_branch.bus_to.api_object.Vnom

                        if abs(v1 - v2) > 1.0:
                            branch_type = BranchType.Transformer
                        else:
                            branch_type = BranchType.Line

                        obj = Branch(bus_from=self.started_branch.bus_from.api_object,
                                     bus_to=self.started_branch.bus_to.api_object,
                                     name=name,
                                     branch_type=branch_type)
                        obj.graphic_obj = self.started_branch
                        self.started_branch.api_object = obj
                        self.circuit.add_branch(obj)
                        item.process_callbacks(item.parent.pos() + item.pos())

                        self.started_branch.setZValue(-1)
                        # if self.diagramView.map.isVisible():
                        #     self.diagramView.map.setZValue(-1)

            if self.started_branch.toPort is None:
                self.started_branch.remove_widget()

        # release this pointer
        self.started_branch = None

    def bigger_nodes(self):
        """
        Expand the grid
        @return:
        """
        min_x = sys.maxsize
        min_y = sys.maxsize
        max_x = -sys.maxsize
        max_y = -sys.maxsize

        if len(self.diagramScene.selectedItems()) > 0:

            # expand selection
            for item in self.diagramScene.selectedItems():
                if type(item) is BusGraphicItem:
                    x = item.pos().x() * self.expand_factor
                    y = item.pos().y() * self.expand_factor
                    item.setPos(QPointF(x, y))

                    # apply changes to the API objects
                    if item.api_object is not None:
                        item.api_object.x = x
                        item.api_object.y = y

                    max_x = max(max_x, x)
                    min_x = min(min_x, x)
                    max_y = max(max_y, y)
                    min_y = min(min_y, y)

        else:

            # expand all
            for item in self.diagramScene.items():
                if type(item) is BusGraphicItem:
                    x = item.pos().x() * self.expand_factor
                    y = item.pos().y() * self.expand_factor
                    item.setPos(QPointF(x, y))

                    max_x = max(max_x, x)
                    min_x = min(min_x, x)
                    max_y = max(max_y, y)
                    min_y = min(min_y, y)

                    # apply changes to the API objects
                    if item.api_object is not None:
                        item.api_object.x = x
                        item.api_object.y = y

        # set the limits of the view
        self.set_limits(min_x, max_x, min_y, max_y)

    def smaller_nodes(self):
        """
        Contract the grid
        @return:
        """
        min_x = sys.maxsize
        min_y = sys.maxsize
        max_x = -sys.maxsize
        max_y = -sys.maxsize

        if len(self.diagramScene.selectedItems()) > 0:

            # shrink selection only
            for item in self.diagramScene.selectedItems():
                if type(item) is BusGraphicItem:
                    x = item.pos().x() / self.expand_factor
                    y = item.pos().y() / self.expand_factor
                    item.setPos(QPointF(x, y))

                    # apply changes to the API objects
                    if item.api_object is not None:
                        item.api_object.x = x
                        item.api_object.y = y

                    max_x = max(max_x, x)
                    min_x = min(min_x, x)
                    max_y = max(max_y, y)
                    min_y = min(min_y, y)
        else:

            # shrink all
            for item in self.diagramScene.items():
                if type(item) is BusGraphicItem:
                    x = item.pos().x() / self.expand_factor
                    y = item.pos().y() / self.expand_factor
                    item.setPos(QPointF(x, y))

                    # apply changes to the API objects
                    if item.api_object is not None:
                        item.api_object.x = x
                        item.api_object.y = y

                    max_x = max(max_x, x)
                    min_x = min(min_x, x)
                    max_y = max(max_y, y)
                    min_y = min(min_y, y)

        # set the limits of the view
        self.set_limits(min_x, max_x, min_y, max_y)

    def set_limits(self, min_x, max_x, min_y, max_y, margin_factor=0.1):
        """
        Set the picture limits
        :param min_x: Minimum x value of the buses location
        :param max_x: Maximum x value of the buses location
        :param min_y: Minimum y value of the buses location
        :param max_y: Maximum y value of the buses location
        :param margin_factor: factor of separation between the buses
        """
        dx = max_x - min_x
        dy = max_y - min_y
        mx = margin_factor * dx
        my = margin_factor * dy
        h = dy + 2 * my
        w = dx + 2 * mx
        self.diagramScene.setSceneRect(min_x - mx, min_y - my, w, h)

    def center_nodes(self):
        """
        Center the view in the nodes
        @return: Nothing
        """
        self.diagramView.fitInView(self.diagramScene.sceneRect(), Qt.KeepAspectRatio)
        self.diagramView.scale(1.0, 1.0)

    def auto_layout(self):
        """
        Automatic layout of the nodes
        """

        if self.circuit.graph is None:
            self.circuit.compile()

        pos = nx.spectral_layout(self.circuit.graph, scale=2, weight='weight')

        pos = nx.fruchterman_reingold_layout(self.circuit.graph, dim=2, k=None, pos=pos, fixed=None, iterations=500,
                                             weight='weight', scale=20.0, center=None)

        # assign the positions to the graphical objects of the nodes
        for i, bus in enumerate(self.circuit.buses):
            try:
                x, y = pos[i] * 500
                bus.graphic_obj.setPos(QPoint(x, y))

                # apply changes to the API objects
                bus.x = x
                bus.y = y

            except KeyError as ex:
                warn('Node ' + str(i) + ' not in graph!!!! \n' + str(ex))

        self.center_nodes()

    def export(self, filename, w=1920, h=1080):
        """
        Save the grid to a png file
        :return:
        """

        name, extension = os.path.splitext(filename.lower())

        if extension == '.png':
            image = QImage(w, h, QImage.Format_ARGB32_Premultiplied)
            image.fill(Qt.transparent)
            painter = QPainter(image)
            painter.setRenderHint(QPainter.Antialiasing)
            self.diagramScene.render(painter)
            image.save(filename)
            painter.end()

        elif extension == '.svg':
            svg_gen = QSvgGenerator()
            svg_gen.setFileName(filename)
            svg_gen.setSize(QSize(w, h))
            svg_gen.setViewBox(QRect(0, 0, w, h))
            svg_gen.setTitle("Electrical grid schematic")
            svg_gen.setDescription("An SVG drawing created by GridCal")

            painter = QPainter(svg_gen)
            self.diagramScene.render(painter)
            painter.end()
        else:
            pass

    def add_branch(self, branch):
        """
        Add branch to the schematic
        :param branch: Branch object
        """
        terminal_from = branch.bus_from.graphic_obj.terminal
        terminal_to = branch.bus_to.graphic_obj.terminal
        graphic_obj = BranchGraphicItem(terminal_from, terminal_to, self.diagramScene, branch=branch)
        graphic_obj.diagramScene.circuit = self.circuit  # add pointer to the circuit
        terminal_from.hosting_connections.append(graphic_obj)
        terminal_to.hosting_connections.append(graphic_obj)
        graphic_obj.redraw()
        branch.graphic_obj = graphic_obj

    def add_api_bus(self, bus: Bus, explode_factor=1.0):
        """
        Add API bus to the diagram
        :param bus: Bus instance
        :param explode_factor: explode factor
        """
        # add the graphic object to the diagram view
        graphic_obj = self.diagramView.add_bus(bus=bus, explode_factor=explode_factor)

        # add circuit pointer to the bus graphic element
        graphic_obj.diagramScene.circuit = self.circuit  # add pointer to the circuit

        # create the bus children
        graphic_obj.create_children_icons()

        # arrange the children
        graphic_obj.arrange_children()

        return graphic_obj

    def add_api_branch(self, branch: Branch):
        """

        :param branch:
        :return:
        """
        terminal_from = branch.bus_from.graphic_obj.terminal
        terminal_to = branch.bus_to.graphic_obj.terminal

        graphic_obj = BranchGraphicItem(terminal_from, terminal_to, self.diagramScene, branch=branch)

        graphic_obj.diagramScene.circuit = self.circuit  # add pointer to the circuit

        terminal_from.hosting_connections.append(graphic_obj)
        terminal_to.hosting_connections.append(graphic_obj)

        graphic_obj.redraw()

        return graphic_obj

    def schematic_from_api(self, explode_factor=1.0):
        """
        Generate schematic from the API
        :param explode_factor: factor to separate the nodes
        :return: Nothing
        """
        # clear all
        self.diagramView.scene_.clear()

        # first create the buses
        for bus in self.circuit.buses:
            bus.graphic_obj = self.add_api_bus(bus, explode_factor)

        for branch in self.circuit.branches:
            branch.graphic_obj = self.add_api_branch(branch)

        # figure limits
        min_x = sys.maxsize
        min_y = sys.maxsize
        max_x = -sys.maxsize
        max_y = -sys.maxsize

        # Align lines
        for bus in self.circuit.buses:
            bus.graphic_obj.arrange_children()
            # get the item position
            x = bus.graphic_obj.pos().x()
            y = bus.graphic_obj.pos().y()

            # compute the boundaries of the grid
            max_x = max(max_x, x)
            min_x = min(min_x, x)
            max_y = max(max_y, y)
            min_y = min(min_y, y)

        # set the figure limits
        self.set_limits(min_x, max_x, min_y, max_y)
        #  center the view
        self.center_nodes()


class AddObjectsThreaded(QThread):

    def __init__(self, editor: GridEditor, explode_factor=1.0):
        QThread.__init__(self)

        self.editor = editor

        self.explode_factor = explode_factor

    def run(self):
        """
        run the file open procedure
        """
        # clear all
        self.editor.diagramView.scene_.clear()

        # first create the buses
        for bus in self.editor.circuit.buses:
            bus.graphic_obj = self.editor.add_api_bus(bus, self.explode_factor)

        for branch in self.editor.circuit.branches:
            branch.graphic_obj = self.editor.add_api_branch(branch)

        # figure limits
        min_x = sys.maxsize
        min_y = sys.maxsize
        max_x = -sys.maxsize
        max_y = -sys.maxsize

        # Align lines
        for bus in self.editor.circuit.buses:
            bus.graphic_obj.arrange_children()
            # get the item position
            x = bus.graphic_obj.pos().x()
            y = bus.graphic_obj.pos().y()

            # compute the boundaries of the grid
            max_x = max(max_x, x)
            min_x = min(min_x, x)
            max_y = max(max_y, y)
            min_y = min(min_y, y)

        # set the figure limits
        self.editor.set_limits(min_x, max_x, min_y, max_y)
        #  center the view
        self.editor.center_nodes()


if __name__ == '__main__':

    from GridCal.Engine.IO.file_handler import FileOpen
    app = QApplication(sys.argv)

    fname = r'C:\Users\PENVERSA\Documents\Git\GridCal\Grids_and_profiles\grids\1354 Pegase.xlsx'
    circuit = FileOpen(fname).open()

    view = GridEditor(circuit)
    view.resize(600, 400)
    view.show()

    thr = AddObjectsThreaded(editor=view)
    thr.run()

    sys.exit(app.exec_())
