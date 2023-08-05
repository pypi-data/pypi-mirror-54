import sys
import os
from PySide2.QtWidgets import *
from PySide2.QtWebEngineWidgets import QWebEngineView as QWebView, QWebEnginePage as QWebPage
import folium

from GridCal.Gui.GIS.gui import *
from GridCal.Engine.IO.file_system import get_create_gridcal_folder


class GISWindow(QMainWindow):

    def __init__(self, parent=None):
        """

        :param parent:
        """
        QMainWindow.__init__(self)
        self.ui = Ui_GisWindow()
        self.ui.setupUi(self)
        self.setWindowTitle('GridCal - GIS')

        # create web browser for the map
        self.web_layout = QtWidgets.QVBoxLayout(self.ui.webFrame)
        self.webView = QWebView()
        self.web_layout.addWidget(self.webView)
        file_path = self.generate_blank_map_html(lon_avg=40.430, lat_avg=3.56)
        self.webView.setUrl(QtCore.QUrl.fromLocalFile(file_path))

        # # action linking
        # self.ui.actionNight_mode.triggered.connect(self.map_.toggle_night_mode)
        # self.ui.actionZoom_in.triggered.connect(self.map_.zoom_increase)
        # self.ui.actionZoom_out.triggered.connect(self.map_.zoom_decrease)

    def msg(self, text, title="Warning"):
        """
        Message box
        :param text: Text to display
        :param title: Name of the window
        """
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(text)
        # msg.setInformativeText("This is additional information")
        msg.setWindowTitle(title)
        # msg.setDetailedText("The details are as follows:")
        msg.setStandardButtons(QMessageBox.Ok)
        retval = msg.exec_()

    @staticmethod
    def generate_blank_map_html(lon_avg, lat_avg):
        """
        Generate a blank HTML map file
        :param lon_avg: center longitude
        :param lat_avg: center latitude
        :return: file name
        """
        my_map = folium.Map(location=[lon_avg, lat_avg], zoom_start=5)

        gc_path = get_create_gridcal_folder()

        path = os.path.join(gc_path, 'map.html')

        my_map.save(path)

        return path


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    window = GISWindow()
    window.resize(1.61 * 700.0, 600.0)  # golden ratio
    window.show()
    sys.exit(app.exec_())

