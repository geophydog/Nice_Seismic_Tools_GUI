from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import (QWidget,
                             QGridLayout,
                             QPushButton,
                             QScrollArea,
                             QMessageBox,
                             QLabel,
                             QLineEdit,
                             QRadioButton,
                             QFileDialog,
                             QComboBox,
                             QApplication,
                             QFrame,
                             QHBoxLayout,
                             QSplitter,
                             QStyleFactory)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt
import folium
from folium.plugins import FastMarkerCluster
import os
import io
import sys
import numpy as np
from branca import colormap as cm
from core_utils.ui_base_setting import UIBaseStyle
from core_utils.map_types import MapChoice
from core_utils.search_tool_thread import SearchingEarthquakeThread
from core_utils.colors import VisualizationColor


class EarthquakeWidgetBlock(QWidget):
    def __init__(self):
        super().__init__()
        bs = UIBaseStyle()
        self.setStyleSheet(bs.btn_style1)
        self.longitude_center = 0
        self.evt = None
        font = QFont('Consolas', 13)

        # Tags of input parameters:
        ew, eh = 180, 40
        self.data_center_tag = QLabel('Data center')
        self.data_center_tag.setFont(font)
        self.data_center_tag.setStyleSheet(bs.label_style5)
        self.data_center_tag.setMaximumSize(ew, eh)

        self.starttime_tag = QLabel('Start time')
        self.starttime_tag.setFont(font)
        self.starttime_tag.setStyleSheet(bs.label_style1)
        self.starttime_tag.setMaximumSize(ew, eh)

        self.endtime_tag = QLabel('End time')
        self.endtime_tag.setFont(font)
        self.endtime_tag.setStyleSheet(bs.label_style1)
        self.endtime_tag.setMaximumSize(ew, eh)

        self.min_magnitude_tag = QLabel('Mmin')
        self.min_magnitude_tag.setFont(font)
        self.min_magnitude_tag.setStyleSheet(bs.label_style4)
        self.min_magnitude_tag.setMaximumSize(ew, eh)

        self.max_magnitude_tag = QLabel('Mmax')
        self.max_magnitude_tag.setFont(font)
        self.max_magnitude_tag.setStyleSheet(bs.label_style4)
        self.max_magnitude_tag.setMaximumSize(ew, eh)

        self.min_depth_tag = QLabel('Dmin (km)')
        self.min_depth_tag.setFont(font)
        self.min_depth_tag.setStyleSheet(bs.label_style4)
        self.min_depth_tag.setMaximumSize(ew, eh)

        self.max_depth_tag = QLabel('Dmax (km)')
        self.max_depth_tag.setFont(font)
        self.max_depth_tag.setStyleSheet(bs.label_style4)
        self.max_depth_tag.setMaximumSize(ew, eh)

        self.mag_type_tag = QLabel('MagType')
        self.mag_type_tag.setFont(font)
        self.mag_type_tag.setStyleSheet(bs.label_style4)
        self.mag_type_tag.setMaximumSize(ew, eh)

        self.lat0_tag = QLabel('Lat0 (deg)')
        self.lat0_tag.setFont(font)
        self.lat0_tag.setStyleSheet(bs.label_style2)
        self.lat0_tag.setMaximumSize(ew, eh)

        self.lon0_tag = QLabel('Lon0(deg)')
        self.lon0_tag.setFont(font)
        self.lon0_tag.setStyleSheet(bs.label_style2)
        self.lon0_tag.setMaximumSize(ew, eh)

        self.min_radius_tag = QLabel('Rmin (deg)')
        self.min_radius_tag.setFont(font)
        self.min_radius_tag.setStyleSheet(bs.label_style2)
        self.min_radius_tag.setMaximumSize(ew, eh)

        self.max_radius_tag = QLabel('Rmax (deg)')
        self.max_radius_tag.setFont(font)
        self.max_radius_tag.setStyleSheet(bs.label_style2)
        self.max_radius_tag.setMaximumSize(ew, eh)

        self.min_lat_tag = QLabel('South (deg)')
        self.min_lat_tag.setFont(font)
        self.min_lat_tag.setStyleSheet(bs.label_style3)
        self.min_lat_tag.setMaximumSize(ew, eh)

        self.max_lat_tag = QLabel('North (deg)')
        self.max_lat_tag.setFont(font)
        self.max_lat_tag.setStyleSheet(bs.label_style3)
        self.max_lat_tag.setMaximumSize(ew, eh)

        self.min_lon_tag = QLabel('West (deg)')
        self.min_lon_tag.setFont(font)
        self.min_lon_tag.setStyleSheet(bs.label_style3)
        self.min_lon_tag.setMaximumSize(ew, eh)

        self.max_lon_tag = QLabel('East (deg)')
        self.max_lon_tag.setFont(font)
        self.max_lon_tag.setStyleSheet(bs.label_style3)
        self.max_lon_tag.setMaximumSize(ew, eh)

        # Input parameters:
        ew, eh = 210, 40
        self.data_center  = QComboBox()
        self.data_center.setFont(font)
        self.data_center.setStyleSheet(bs.editline_style)
        self.data_center.addItems(['EMSC', 'ETHZ', 'INGV',
                                   'IRIS', 'ISC-IRIS', 'ISC-UK',
                                   'NCEDC', 'SCEDC', 'USGS'])
        self.data_center.setCurrentText('IRIS')
        self.data_center.setMaximumSize(ew, eh)

        self.starttime = QLineEdit()
        self.starttime.setFont(font)
        self.starttime.setPlaceholderText('YYYY-MM-DDThh:mm:ss')
        self.starttime.setStyleSheet(bs.editline_style)
        self.starttime.setText('2011-01-01T00:00:00')
        self.starttime.setMaximumSize(ew, eh)

        self.endtime = QLineEdit()
        self.endtime.setFont(font)
        self.endtime.setPlaceholderText('YYYY-MM-DDThh:mm:dd')
        self.endtime.setStyleSheet(bs.editline_style)
        self.endtime.setText('2012-01-01T00:00:00')
        self.endtime.setMaximumSize(ew, eh)

        self.min_magnitude = QLineEdit()
        self.min_magnitude.setFont(font)
        self.min_magnitude.setStyleSheet(bs.editline_style)
        self.min_magnitude.setText('7')
        self.min_magnitude.setMaximumSize(ew, eh)

        self.max_magnitude = QLineEdit()
        self.max_magnitude.setFont(font)
        self.max_magnitude.setStyleSheet(bs.editline_style)
        self.max_magnitude.setText('9.5')
        self.max_magnitude.setMaximumSize(ew, eh)

        self.min_depth = QLineEdit()
        self.min_depth.setFont(font)
        self.min_depth.setStyleSheet(bs.editline_style)
        self.min_depth.setText('-1')
        self.min_depth.setMaximumSize(ew, eh)

        self.max_depth = QLineEdit()
        self.max_depth.setFont(font)
        self.max_depth.setStyleSheet(bs.editline_style)
        self.max_depth.setText('700')
        self.max_depth.setMaximumSize(ew, eh)

        self.lat0 = QLineEdit()
        self.lat0.setFont(font)
        self.lat0.setStyleSheet(bs.editline_style)
        self.lat0.setText('0')
        self.lat0.setMaximumSize(ew, eh)

        self.lon0 = QLineEdit()
        self.lon0.setFont(font)
        self.lon0.setStyleSheet(bs.editline_style)
        self.lon0.setText('0')
        self.lon0.setMaximumSize(ew, eh)

        self.min_radius = QLineEdit()
        self.min_radius.setFont(font)
        self.min_radius.setStyleSheet(bs.editline_style)
        self.min_radius.setText('0')
        self.min_radius.setMaximumSize(ew, eh)

        self.max_radius = QLineEdit()
        self.max_radius.setFont(font)
        self.max_radius.setStyleSheet(bs.editline_style)
        self.max_radius.setText('75')
        self.max_radius.setMaximumSize(ew, eh)

        self.min_lat = QLineEdit()
        self.min_lat.setFont(font)
        self.min_lat.setStyleSheet(bs.editline_style)
        self.min_lat.setText('-90')
        self.min_lat.setMaximumSize(ew, eh)

        self.max_lat = QLineEdit()
        self.max_lat.setFont(font)
        self.max_lat.setStyleSheet(bs.editline_style)
        self.max_lat.setText('90')
        self.max_lat.setMaximumSize(ew, eh)

        self.min_lon = QLineEdit()
        self.min_lon.setFont(font)
        self.min_lon.setStyleSheet(bs.editline_style)
        self.min_lon.setText('-180')
        self.min_lon.setMaximumSize(ew, eh)

        self.max_lon = QLineEdit()
        self.max_lon.setFont(font)
        self.max_lon.setStyleSheet(bs.editline_style)
        self.max_lon.setText('180')
        self.max_lon.setMaximumSize(ew, eh)

        # Searching styles:
        self.rect_search = QRadioButton('Rectangle')
        self.rect_search.setFont(font)
        self.rect_search.setChecked(True)
        self.rect_search.setStyleSheet(bs.checkbox_style)
        self.rect_search.setMaximumSize(ew, eh)

        self.circle_search = QRadioButton('Circle   ')
        self.circle_search.setFont(font)
        self.circle_search.setStyleSheet(bs.checkbox_style)
        self.circle_search.setMaximumSize(ew, eh)

        # Operations:
        ew, eh = 210, 40
        self.find_evt = QPushButton('Search earthquake')
        self.find_evt.setFont(font)
        self.find_evt.setIcon(QIcon('pic/SEARCH.png'))
        self.find_evt.setToolTip('Find seismic events.')
        self.find_evt.setStyleSheet(bs.btn_style2)
        self.find_evt.setFixedSize(397, 40)
        self.find_evt.clicked.connect(self.run_search_event)

        self.save_data = QPushButton('Save earthquake')
        self.save_data.setFont(font)
        self.save_data.setIcon(QIcon('pic/SAVE.jpg'))
        self.save_data.setToolTip('Save event information in file.')
        self.save_data.setStyleSheet(bs.btn_style2)
        self.save_data.setFixedSize(397, 40)
        self.save_data.clicked.connect(self.save_event)

        # -------------------- Panel of event searching ----------------------- #
        self.lay1 = QGridLayout()
        self.lay1.addWidget(self.rect_search, 0, 0, 1, 1)
        self.lay1.addWidget(self.circle_search, 0, 1, 1, 1)
        self.lay1.addWidget(self.find_evt, 1, 0, 1, 2)
        self.lay1.addWidget(self.data_center_tag, 2, 0, 1, 1)
        self.lay1.addWidget(self.data_center, 2, 1, 1, 1)
        self.lay1.addWidget(self.starttime_tag, 3, 0, 1, 1)
        self.lay1.addWidget(self.starttime, 3, 1, 1, 1)
        self.lay1.addWidget(self.endtime_tag, 4, 0, 1, 1)
        self.lay1.addWidget(self.endtime, 4, 1, 1, 1)
        self.lay1.addWidget(self.min_magnitude_tag, 5, 0, 1, 1)
        self.lay1.addWidget(self.min_magnitude, 5, 1, 1, 1)
        self.lay1.addWidget(self.max_magnitude_tag, 6, 0, 1, 1)
        self.lay1.addWidget(self.max_magnitude, 6, 1, 1, 1)
        self.lay1.addWidget(self.min_depth_tag, 7, 0, 1, 1)
        self.lay1.addWidget(self.min_depth, 7, 1, 1, 1)
        self.lay1.addWidget(self.max_depth_tag, 8, 0, 1, 1)
        self.lay1.addWidget(self.max_depth, 8, 1, 1, 1)
        self.lay1.addWidget(self.lat0_tag, 9, 0, 1, 1)
        self.lay1.addWidget(self.lat0, 9, 1, 1, 1)
        self.lay1.addWidget(self.lon0_tag, 10, 0, 1, 1)
        self.lay1.addWidget(self.lon0, 10, 1, 1, 1)
        self.lay1.addWidget(self.min_radius_tag, 11, 0, 1, 1)
        self.lay1.addWidget(self.min_radius, 11, 1, 1, 1)
        self.lay1.addWidget(self.max_radius_tag, 12, 0, 1, 1)
        self.lay1.addWidget(self.max_radius, 12, 1, 1, 1)
        self.lay1.addWidget(self.min_lat_tag, 13, 0, 1, 1)
        self.lay1.addWidget(self.min_lat, 13, 1, 1, 1)
        self.lay1.addWidget(self.max_lat_tag, 14, 0, 1, 1)
        self.lay1.addWidget(self.max_lat, 14, 1, 1, 1)
        self.lay1.addWidget(self.min_lon_tag, 15, 0, 1, 1)
        self.lay1.addWidget(self.min_lon, 15, 1, 1, 1)
        self.lay1.addWidget(self.max_lon_tag, 16, 0, 1, 1)
        self.lay1.addWidget(self.max_lon, 16, 1, 1, 1)
        self.lay1.addWidget(self.save_data, 17, 0, 1, 2)
        self.frame1 = QFrame()
        self.frame1.setFixedWidth(420)
        self.frame1.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame1.setFrameShadow(QFrame.Shadow.Sunken)
        self.frame1.setLayout(self.lay1)

        # ----------------------- Panel of plotting events ---------------------------- #
        self.plot_evt = QPushButton('Plot earthquake')
        self.plot_evt.setFont(font)
        self.plot_evt.setIcon(QIcon('pic/PLOT.jpg'))
        self.plot_evt.setToolTip('Plot earthquakes on geographical map.')
        self.plot_evt.setStyleSheet(bs.btn_style2)
        self.plot_evt.setMaximumSize(ew, eh)
        self.plot_evt.clicked.connect(self.plot_event)

        # event geographical map.
        self.map_view = QWebEngineView()
        self.map_view.setContentsMargins(5, 5, 5, 5)
        # Basic map background options.
        # ew, eh = 210, 40
        self.basemap = QComboBox()
        self.basemap.setFont(font)
        self.basemap.setStyleSheet(bs.editline_style)
        self.basemap.addItems(['GaodeStreet', 'GaodeSatellite',
                               'OpenTopoZhLa', 'Russian',
                               'StamenWaterColor', 'HikeBikeMultiLa',
                               'ArcgisChinaEnLa', 'ArcgisOnlineEnLa'])
        self.basemap.setCurrentText('ArcgisChinaEnLa')
        self.basemap.setMaximumSize(ew, eh)

        self.lay2 = QGridLayout()
        self.lay2.addWidget(self.basemap, 0, 0, 1, 1)
        self.lay2.addWidget(self.plot_evt, 0, 1, 1, 1)
        self.lay2.addWidget(self.map_view, 1, 0, 8, 5)
        self.frame2 = QFrame()
        self.frame2.setMinimumHeight(500)
        self.frame2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame2.setFrameShadow(QFrame.Shadow.Sunken)
        self.frame2.setLayout(self.lay2)

        # ----------------- Panel of printting event information ------------------- #
        self.print_evt_into = QPushButton('Print earthquake')
        self.print_evt_into.setFont(font)
        self.print_evt_into.setIcon(QIcon('pic/PRINT.jpg'))
        self.print_evt_into.setToolTip('Print event information in the box.')
        self.print_evt_into.setStyleSheet(bs.btn_style2)
        self.print_evt_into.setMaximumSize(ew, eh)
        self.print_evt_into.clicked.connect(self.print_event)

        # Print evttion information
        self.base_info = QLabel('Information about earthquakes ...')
        self.base_info.setFont(font)
        self.base_info.setMinimumSize(1200, 20)
        # self.base_info.setMinimumSize(1000, 20)
        self.base_info.setWordWrap(True)
        self.scroll = QScrollArea(self)
        self.scroll.setContentsMargins(0, 0, 0, 0)
        self.scroll.setStyleSheet('QScrollArea{border-color: #999999}')
        self.scroll.setWidget(self.base_info)

        # Add tag widgets on UI.
        self.lay3 = QGridLayout()
        self.lay3.addWidget(self.print_evt_into, 0, 0, 1, 1)
        self.lay3.addWidget(self.scroll, 1, 0, 6, 5)
        self.frame3 = QFrame()
        self.frame3.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame3.setFrameShadow(QFrame.Shadow.Sunken)
        self.frame3.setLayout(self.lay3)

        # -------------------------- Setting the whole UI layout -------------------- #
        splitter1 = QSplitter(Qt.Orientation.Vertical)
        splitter1.addWidget(self.frame2)
        splitter1.addWidget(self.frame3)
        splitter2 = QSplitter(Qt.Orientation.Horizontal)
        splitter2.addWidget(self.frame1)
        splitter2.addWidget(splitter1)
        hbox = QHBoxLayout()
        hbox.addWidget(splitter2)
        self.setLayout(hbox)
        QApplication.setStyle(QStyleFactory.create('Cleanlooks'))
        self.setWindowTitle('GeophyDogEye-Earthquake')
        self.setWindowIcon(QIcon('pic/EVT_SEARCH_LOGO.png'))

    def run_search_event(self):
        try:
            para = {}
            para['t1'] = self.starttime.text()
            para['t2'] = self.endtime.text()
            para['m1'] = float(self.min_magnitude.text())
            para['m2'] = float(self.max_magnitude.text())
            para['la0'] = float(self.lat0.text())
            para['lo0'] = float(self.lon0.text())
            para['r1'] = float(self.min_radius.text())
            para['r2'] = float(self.max_radius.text())
            para['la1'] = float(self.min_lat.text())
            para['la2'] = float(self.max_lat.text())
            para['lo1'] = float(self.min_lon.text())
            para['lo2'] = float(self.max_lon.text())
            para['d1'] = -1
            para['d2'] = 1000
            para['dmc'] = self.data_center.currentText()
            para['search_style'] = 'rect'
            if self.circle_search.isChecked():
                para['search_style'] = 'circle'
            self.evt_search = SearchingEarthquakeThread(para)
            self.evt_search.result_signal.connect(self.get_event_info)
            self.evt_search.start()
        except Exception:
            QMessageBox.critical(self, 'Error', 'Error in searching earthquakes!')

    def get_event_info(self, result):
        try:
            self.evt = result
            QMessageBox.about(self, 'Info', '%d earthquake(s) found!'%len(self.evt))
        except Exception:
            QMessageBox.critical(self, 'Error', 'Error in obtaining earthquakes!')

    def print_event(self):
        if hasattr(self, 'evt') and self.evt != None and len(self.evt) > 0:
            s = 'Earthquakes: %d\n' % len(self.evt)
            s += '\n'.join(self.evt)
            self.evt_info = QLabel(s, self)
            self.evt_info.setMinimumSize(1200, 50)
            self.evt_info.setFont(QFont('Consolas', 13))
            self.evt_info.setWordWrap(True)
            self.evt_info.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
            self.evt_info.setText(s)
            self.new_scroll = QScrollArea(self)
            self.new_scroll.setWidget(self.evt_info)
            self.new_scroll.setContentsMargins(0, 0, 0, 0)
            self.new_scroll.setStyleSheet('QScrollArea{border-color: #999999}')
            self.new_scroll.setMinimumSize(1200, 200)
            self.lay3.removeWidget(self.scroll)
            self.lay3.addWidget(self.new_scroll, 1, 0, 6, 5)
        else:
            QMessageBox.critical(self, 'Error', 'No earthquake data or wrong information!')

    def save_event(self):
        if hasattr(self, 'evt') and len(self.evt) > 0:
            s = '\n'.join(self.evt)
            try:
                f_name, _ = QFileDialog.getSaveFileName(self,
                                                        os.getcwd(),
                                                        'All files(*);;*')

                with open(f_name, 'w') as fout:
                    fout.write(s)
                QMessageBox.about(self, 'Message', 'Saved earthquake data in %s!' % f_name)
            except Exception:
                QMessageBox.about(self, 'Message', 'Cancelled to save earthquake data!')
        else:
            QMessageBox.critical(self, 'Error', 'No earthquake data to save!')

    def plot_event(self):
        if hasattr(self, 'evt') and len(self.evt) > 0:
            maps = MapChoice()
            maps = maps.map_url
            c = VisualizationColor()
            colors = c.evt_colors
            self.map = folium.Map(location=[0, 0],
                                  tiles=maps[self.basemap.currentText()],
                                  attr='default',
                                  control_scale=True,
                                  zoom_start=0.5)
            n = len(self.evt)
            if n < 750:
                cn = len(colors)
                evt = []
                for line in self.evt:
                    tmp = line.strip().split('|')
                    d = float(tmp[4])
                    evt.append([float(tmp[3]), float(tmp[2]), float(tmp[10]), d])
                evt = np.array(evt)
                dmax = np.max(evt[:, -1])
                dmin = np.min(evt[:, -1])
                for line in evt:
                    tooltip = 'm: %g depth: %g km %g %g' % (line[2], line[3], line[1], line[0])
                    ci = int((line[3]-dmin)/(dmax-dmin)*cn)
                    if ci >= cn:
                        ci = cn - 1
                    folium.CircleMarker(
                        location=(line[1], line[0]),
                        radius=line[2],
                        tooltip=tooltip,
                        color=colors[ci],
                        fill=True,
                        fill_color=colors[ci],
                        fill_opaticy=0.75,
                        weight=1.5).add_to(self.map)
                cmap = cm.LinearColormap(colors=colors,
                                         vmin=dmin, vmax=dmax,
                                         caption='Source depth (km)')
                self.map.add_child(cmap)
            else:
                data = []
                for line in self.evt:
                    line = line.split('|')
                    data.append([float(line[2]), float(line[3])])
                FastMarkerCluster(data=data).add_to(self.map)
            self.map.add_child(folium.LatLngPopup())
            data = io.BytesIO()
            self.map.save(data, close_file=False)
            self.map_view.setHtml(data.getvalue().decode())
        else:
            QMessageBox.critical(self, 'Error', 'No event data!')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    evt = EarthquakeWidgetBlock()
    evt.show()
    sys.exit(app.exec_())