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
							 QDoubleSpinBox,
							 QFrame,
							 QSplitter,
							 QHBoxLayout,
							 QApplication,
							 QStyleFactory)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import folium
from folium.plugins import FastMarkerCluster
import os
import io
import sys
import numpy as np
from core_utils.ui_base_setting import UIBaseStyle
from core_utils.search_tool_thread import SearchingStationThread
from core_utils.map_types import MapChoice
from core_utils.SeisArrayPy import ArrayResponse
from core_utils.colors import VisualizationColor



class StationWidgetBlock(QWidget):
	def __init__(self):
		super().__init__()
		bs = UIBaseStyle()
		self.sta = []
		font = QFont('Consolas', 13, QFont.Weight.Bold)

		# Tags of input parameters:
		ew, eh = 180, 40
		self.data_center_tag = QLabel('Data center')
		self.data_center_tag.setFont(font)
		self.data_center_tag.setStyleSheet(bs.label_style5)
		self.data_center_tag.setFixedSize(ew, eh)

		self.starttime_tag = QLabel('Start time')
		self.starttime_tag.setFont(font)
		self.starttime_tag.setStyleSheet(bs.label_style1)
		self.starttime_tag.setFixedSize(ew, eh)

		self.endtime_tag = QLabel('End time')
		self.endtime_tag.setFont(font)
		self.endtime_tag.setStyleSheet(bs.label_style1)
		self.endtime_tag.setFixedSize(ew, eh)

		self.network_tag = QLabel('Network')
		self.network_tag.setFont(font)
		self.network_tag.setStyleSheet(bs.label_style1)
		self.network_tag.setFixedSize(ew, eh)

		self.station_tag = QLabel('Station')
		self.station_tag.setFont(font)
		self.station_tag.setStyleSheet(bs.label_style1)
		self.station_tag.setFixedSize(ew, eh)

		self.channel_tag = QLabel('Channel')
		self.channel_tag.setFont(font)
		self.channel_tag.setStyleSheet(bs.label_style1)
		self.channel_tag.setFixedSize(ew, eh)

		self.location_tag = QLabel('Location')
		self.location_tag.setFont(font)
		self.location_tag.setStyleSheet(bs.label_style1)
		self.location_tag.setFixedSize(ew, eh)

		self.lat0_tag = QLabel('Lat0 (deg)')
		self.lat0_tag.setFont(font)
		self.lat0_tag.setStyleSheet(bs.label_style2)
		self.lat0_tag.setFixedSize(ew, eh)

		self.lon0_tag = QLabel('Lon0 (deg)')
		self.lon0_tag.setFont(font)
		self.lon0_tag.setStyleSheet(bs.label_style2)
		self.lon0_tag.setFixedSize(ew, eh)

		self.min_radius_tag = QLabel('Rmin (deg)')
		self.min_radius_tag.setFont(font)
		self.min_radius_tag.setStyleSheet(bs.label_style2)
		self.min_radius_tag.setFixedSize(ew, eh)

		self.max_radius_tag = QLabel('Rmax (deg)')
		self.max_radius_tag.setFont(font)
		self.max_radius_tag.setStyleSheet(bs.label_style2)
		self.max_radius_tag.setFixedSize(ew, eh)

		self.min_lat_tag = QLabel('South (deg)')
		self.min_lat_tag.setFont(font)
		self.min_lat_tag.setStyleSheet(bs.label_style3)
		self.min_lat_tag.setFixedSize(ew, eh)

		self.max_lat_tag = QLabel('North (deg)')
		self.max_lat_tag.setFont(font)
		self.max_lat_tag.setStyleSheet(bs.label_style3)
		self.max_lat_tag.setFixedSize(ew, eh)

		self.min_lon_tag = QLabel('West (deg)')
		self.min_lon_tag.setFont(font)
		self.min_lon_tag.setStyleSheet(bs.label_style3)
		self.min_lon_tag.setFixedSize(ew, eh)

		self.max_lon_tag = QLabel('East (deg)')
		self.max_lon_tag.setFont(font)
		self.max_lon_tag.setStyleSheet(bs.label_style3)
		self.max_lon_tag.setFixedSize(ew, eh)

		# Input parameters:
		ew, eh = 210, 40
		self.data_center = QComboBox()
		self.data_center.setFont(font)
		self.data_center.setStyleSheet(bs.editline_style)
		self.data_center.addItems(['AUSPASS', 'BATS', 'BGR', 'ETH', 'GEONET',
								   'GFZ', 'ICGC', 'INGV', 'IPGP', 'IRIS',
								   'IRISPH5', 'KNMI', 'KOERI', 'LMU', 'NCEDC',
								   'NIEP', 'NOA', 'ODC', 'ORFEUS', 'RASPISHAKE',
								   'RESIF', 'SCEDC', 'SED', 'TEXNET', 'UIB-NORSAR',
								   'USGS', 'USP'])
		self.data_center.setCurrentText('IRIS')
		self.data_center.setFixedSize(ew, eh)

		self.starttime = QLineEdit()
		self.starttime.setFont(font)
		self.starttime.setPlaceholderText('YYYY-MM-DDThh:mm:ss')
		self.starttime.setStyleSheet(bs.editline_style)
		self.starttime.setText('2010-01-01T00:00:00')
		self.starttime.setFixedSize(ew, eh)

		self.endtime = QLineEdit()
		self.endtime.setFont(font)
		self.endtime.setPlaceholderText('YYYY-MM-DDThh:mm:dd')
		self.endtime.setStyleSheet(bs.editline_style)
		self.endtime.setText('2012-01-01T00:00:00')
		self.endtime.setFixedSize(ew, eh)

		self.network = QLineEdit()
		self.network.setFont(font)
		self.network.setPlaceholderText('XXX,XXX')
		self.network.setStyleSheet(bs.editline_style)
		self.network.setText('G,II,IU')
		self.network.setFixedSize(ew, eh)

		self.station = QLineEdit()
		self.station.setFont(font)
		self.station.setPlaceholderText('XXX,XXX,...')
		self.station.setStyleSheet(bs.editline_style)
		self.station.setText('*')
		self.station.setFixedSize(ew, eh)

		self.channel = QLineEdit()
		self.channel.setFont(font)
		self.channel.setPlaceholderText('LH?,BHZ')
		self.channel.setStyleSheet(bs.editline_style)
		self.channel.setText('BHZ')
		self.channel.setFixedSize(ew, eh)

		self.location = QLineEdit()
		self.location.setFont(font)
		self.location.setPlaceholderText('00,10,...')
		self.location.setStyleSheet(bs.editline_style)
		self.location.setText('*')
		self.location.setFixedSize(ew, eh)

		self.lat0 = QLineEdit()
		self.lat0.setFont(font)
		self.lat0.setStyleSheet(bs.editline_style)
		self.lat0.setText('0')
		self.lat0.setFixedSize(ew, eh)

		self.lon0 = QLineEdit()
		self.lon0.setFont(font)
		self.lon0.setStyleSheet(bs.editline_style)
		self.lon0.setText('0')
		self.lon0.setFixedSize(ew, eh)

		self.min_radius = QLineEdit()
		self.min_radius.setFont(font)
		self.min_radius.setStyleSheet(bs.editline_style)
		self.min_radius.setText('0')
		self.min_radius.setFixedSize(ew, eh)

		self.max_radius = QLineEdit()
		self.max_radius.setFont(font)
		self.max_radius.setStyleSheet(bs.editline_style)
		self.max_radius.setText('75')
		self.max_radius.setFixedSize(ew, eh)

		self.min_lat = QLineEdit()
		self.min_lat.setFont(font)
		self.min_lat.setStyleSheet(bs.editline_style)
		self.min_lat.setText('-90')
		self.min_lat.setFixedSize(ew, eh)

		self.max_lat = QLineEdit()
		self.max_lat.setFont(font)
		self.max_lat.setStyleSheet(bs.editline_style)
		self.max_lat.setText('90')
		self.max_lat.setFixedSize(ew, eh)

		self.min_lon = QLineEdit()
		self.min_lon.setFont(font)
		self.min_lon.setStyleSheet(bs.editline_style)
		self.min_lon.setText('-180')
		self.min_lon.setFixedSize(ew, eh)

		self.max_lon = QLineEdit()
		self.max_lon.setFont(font)
		self.max_lon.setStyleSheet(bs.editline_style)
		self.max_lon.setText('180')
		self.max_lon.setFixedSize(ew, eh)

		# Searching styles:
		self.rect_search = QRadioButton('Rectangle')
		self.rect_search.setFont(font)
		self.rect_search.setChecked(True)
		self.rect_search.setStyleSheet(bs.checkbox_style)
		self.rect_search.setFixedSize(180, 40)
		self.circle_search = QRadioButton('Circle   ')
		self.circle_search.setFont(font)
		self.circle_search.setStyleSheet(bs.checkbox_style)
		self.circle_search.setFixedSize(210, 40)

		# Operations:
		self.find_sta = QPushButton('Search station')
		self.find_sta.setFont(font)
		self.find_sta.setIcon(QIcon('pic/SEARCH.png'))
		self.find_sta.setToolTip('Find seismic station.')
		self.find_sta.setStyleSheet(bs.btn_style1)
		self.find_sta.clicked.connect(self.search_station)
		self.find_sta.setFixedSize(397, 40)

		self.save_data = QPushButton('Save station')
		self.save_data.setFont(font)
		self.save_data.setIcon(QIcon('pic/SAVE.jpg'))
		self.save_data.setToolTip('Save station information in file.')
		self.save_data.setStyleSheet(bs.btn_style1)
		self.save_data.clicked.connect(self.save_station)
		self.save_data.setFixedSize(397, 40)

		# Add tag widgets on UI.
		self.layout1 = QGridLayout()
		self.layout1.addWidget(self.data_center_tag, 2, 0, 1, 1)

		self.layout1.addWidget(self.starttime_tag, 3, 0, 1, 1)
		self.layout1.addWidget(self.endtime_tag, 4, 0, 1, 1)
		self.layout1.addWidget(self.network_tag, 5, 0, 1, 1)
		self.layout1.addWidget(self.station_tag, 6, 0, 1, 1)
		self.layout1.addWidget(self.channel_tag, 7, 0, 1, 1)
		self.layout1.addWidget(self.location_tag, 8, 0, 1, 1)

		self.layout1.addWidget(self.lat0_tag, 9, 0, 1, 1)
		self.layout1.addWidget(self.lon0_tag, 10, 0, 1, 1)
		self.layout1.addWidget(self.min_radius_tag, 11, 0, 1, 1)
		self.layout1.addWidget(self.max_radius_tag, 12, 0, 1, 1)

		self.layout1.addWidget(self.min_lat_tag, 13, 0, 1, 1)
		self.layout1.addWidget(self.max_lat_tag, 14, 0, 1, 1)
		self.layout1.addWidget(self.min_lon_tag, 15, 0, 1, 1)
		self.layout1.addWidget(self.max_lon_tag, 16, 0, 1, 1)

		# Add edit widgets on UI.
		self.layout1.addWidget(self.data_center, 2, 1, 1, 1)
		self.layout1.addWidget(self.starttime, 3, 1, 1, 1)
		self.layout1.addWidget(self.endtime, 4, 1, 1, 1)
		self.layout1.addWidget(self.network, 5, 1, 1, 1)
		self.layout1.addWidget(self.station, 6, 1, 1, 1)
		self.layout1.addWidget(self.channel, 7, 1, 1, 1)
		self.layout1.addWidget(self.location, 8, 1, 1, 1)

		self.layout1.addWidget(self.lat0, 9, 1, 1, 1)
		self.layout1.addWidget(self.lon0, 10, 1, 1, 1)
		self.layout1.addWidget(self.min_radius, 11, 1, 1, 1)
		self.layout1.addWidget(self.max_radius, 12, 1, 1, 1)

		self.layout1.addWidget(self.min_lat, 13, 1, 1, 1)
		self.layout1.addWidget(self.max_lat, 14, 1, 1, 1)
		self.layout1.addWidget(self.min_lon, 15, 1, 1, 1)
		self.layout1.addWidget(self.max_lon, 16, 1, 1, 1)
		self.layout1.addWidget(self.save_data, 17, 0, 1, 2)
		self.layout1.addWidget(self.rect_search, 0, 0, 1, 1)
		self.layout1.addWidget(self.circle_search, 0, 1, 1, 1)
		self.layout1.addWidget(self.find_sta, 1, 0, 1, 2)

		self.frame1 = QFrame()
		self.frame1.setFrameShape(QFrame.Shape.StyledPanel)
		self.frame1.setFrameShadow(QFrame.Shadow.Sunken)
		self.frame1.setFixedWidth(420)
		self.frame1.setLayout(self.layout1)

		# --------------------------------- Station map panel ---------------------------- #
		self.plot_sta = QPushButton('Show station')
		self.plot_sta.setFont(font)
		self.plot_sta.setIcon(QIcon('pic/PLOT.jpg'))
		self.plot_sta.setToolTip('Plot seismic stations on geographical map.')
		self.plot_sta.setStyleSheet(bs.btn_style1)
		self.plot_sta.clicked.connect(self.plot_station)
		# Station geographical map.
		self.map_view = QWebEngineView()
		self.map_view.setContentsMargins(5, 5, 5, 5)
		# Geo base map.
		self.map_type = QComboBox()
		self.map_type.setFont(font)
		self.map_type.setStyleSheet(bs.editline_style)
		self.map_type.addItems(['GaodeStreet', 'GaodeSatellite',
								'OpenTopoZhLa', 'Russian',
								'StamenWaterColor', 'HikeBikeMultiLa',
								'ArcgisChinaEnLa', 'ArcgisOnlineEnLa'])
		self.map_type.setCurrentText('ArcgisOnlineEnLa')
		self.layout2 = QGridLayout()
		self.layout2.addWidget(self.map_type, 0, 0, 1, 1)
		self.layout2.addWidget(self.plot_sta, 0, 1, 1, 1)
		self.layout2.addWidget(self.map_view, 1, 0, 6, 10)
		self.frame2 = QFrame(self)
		self.frame2.setFrameShape(QFrame.Shape.StyledPanel)
		self.frame2.setFrameShadow(QFrame.Shadow.Sunken)
		self.frame2.setLayout(self.layout2)

		# ----------------------------- Print station information panel ------------------ #
		self.print_sta_into = QPushButton('Station information')
		self.print_sta_into.setFont(font)
		self.print_sta_into.setIcon(QIcon('pic/PRINT.jpg'))
		self.print_sta_into.setToolTip('Print station information in the box.')
		self.print_sta_into.setStyleSheet(bs.btn_style1)
		self.print_sta_into.clicked.connect(self.print_station)
		self.base_info = QLabel('Information about seismic stations ...')
		self.base_info.setFont(font)
		self.base_info.setFixedWidth(1200)
		self.base_info.setWordWrap(True)
		self.scroll = QScrollArea()
		self.scroll.setContentsMargins(0, 0, 0, 0)
		self.scroll.setStyleSheet('QScrollArea{border-color: #999999}')
		self.scroll.setWidget(self.base_info)
		self.layout3 = QGridLayout()
		self.layout3.addWidget(self.print_sta_into, 0, 0, 1, 1)
		self.layout3.addWidget(self.scroll, 1, 0, 6, 10)
		self.frame3 = QFrame()
		self.frame3.setFrameShape(QFrame.Shape.StyledPanel)
		self.frame3.setFrameShadow(QFrame.Shadow.Sunken)
		self.frame3.setFixedHeight(383)
		self.frame3.setLayout(self.layout3)

		# ----------------------------- Array response function panel -------------------------- #
		font2 = QFont('Consolas', 12, QFont.Weight.Bold)
		self.relative_position = QRadioButton('Relative position')
		self.relative_position.setFont(font2)
		self.relative_position.setStyleSheet(bs.checkbox_style)
		self.relative_position.setChecked(True)
		self.cross_position = QRadioButton('Cross position')
		self.cross_position.setFont(font2)
		self.cross_position.setStyleSheet(bs.checkbox_style)

		self.array_response = QPushButton('Array response')
		self.array_response.setFont(font)
		self.array_response.setIcon(QIcon('pic/ARF.png'))
		self.array_response.setToolTip('Show the array response spectra.')
		self.array_response.setStyleSheet(bs.btn_style1)
		self.array_response.setFixedSize(200, 40)
		self.array_response.clicked.connect(self.plot_array_response)

		# Array transfer function.
		self.fig = Figure()
		self.canvas = FigureCanvas(self.fig)
		self.toolbar = NavigationToolbar(self.canvas, self)

		self.slowness_value = QDoubleSpinBox()
		self.slowness_value.setDecimals(5)
		self.slowness_value.setFont(font)
		self.slowness_value.setRange(0, 0.01)
		self.slowness_value.setSingleStep(0.00001)
		self.slowness_value.setValue(0.001)
		self.slowness_label = QLabel('Max slowness (s/km):')
		self.slowness_label.setFont(font)

		self.min_power = QDoubleSpinBox()
		self.min_power.setFont(font)
		self.min_power.setRange(-30, 0)
		self.min_power.setSingleStep(1)
		self.min_power.setValue(-10)
		self.min_power_label = QLabel('Min power (db):')
		self.min_power_label.setFont(font)

		self.frequency_value = QDoubleSpinBox()
		self.frequency_value.setDecimals(4)
		self.frequency_value.setFont(font)
		self.frequency_value.setRange(0, 50)
		self.frequency_value.setSingleStep(0.001)
		self.frequency_value.setValue(1)

		self.frequency_label = QLabel('Frequency (Hz):')
		self.frequency_label.setFont(font)

		self.network_code = QComboBox()
		self.network_code.setFont(font)
		self.network_code.setStyleSheet(bs.editline_style)
		self.network_code.setPlaceholderText('Network code')

		self.layout4 = QGridLayout()
		self.layout4.addWidget(self.relative_position, 0, 0, 1, 1)
		self.layout4.addWidget(self.cross_position, 0, 1, 1, 1)
		self.layout4.addWidget(self.array_response, 1, 0, 1, 1)
		self.layout4.addWidget(self.network_code, 1, 1, 1, 1)
		self.layout4.addWidget(self.frequency_label, 2, 0, 1, 1)
		self.layout4.addWidget(self.frequency_value, 2, 1, 1, 1)
		self.layout4.addWidget(self.slowness_label, 3, 0, 1, 1)
		self.layout4.addWidget(self.slowness_value, 3, 1, 1, 1)
		self.layout4.addWidget(self.min_power_label, 4, 0, 1, 1)
		self.layout4.addWidget(self.min_power, 4, 1, 1, 1)
		self.layout4.addWidget(self.toolbar, 5, 0, 1, 3)
		self.layout4.addWidget(self.canvas, 6, 0, 4, 3)

		self.frame4 = QFrame()
		self.frame4.setFrameShape(QFrame.Shape.StyledPanel)
		self.frame4.setFrameShadow(QFrame.Shadow.Sunken)
		self.frame4.setFixedWidth(400)
		self.frame4.setLayout(self.layout4)

		# ----------------------- The whole layout --------------------------- #
		splitter1 = QSplitter(Qt.Orientation.Horizontal)
		splitter1.addWidget(self.frame2)
		splitter1.addWidget(self.frame4)

		splitter2 = QSplitter(Qt.Orientation.Vertical)
		splitter2.addWidget(splitter1)
		splitter2.addWidget(self.frame3)

		splitter3 = QSplitter(Qt.Orientation.Horizontal)
		splitter3.addWidget(self.frame1)
		splitter3.addWidget(splitter2)

		self.setStyleSheet(bs.btn_style1)
		hbox = QHBoxLayout()
		hbox.addWidget(splitter3)
		self.setLayout(hbox)
		QApplication.setStyle(QStyleFactory.create('Cleanlooks'))
		self.setWindowTitle('GeophyDogEye-Station')
		self.setWindowIcon(QIcon('pic/STA_SEARCH_LOGO.png'))

	def set_frequency(self):
		v = self.frequency_dial.value()
		self.frequency_value.setText('%g' % (v * 1e-3))

	def set_slowness(self):
		v = self.slowness_dial.value()
		self.slowness_value.setText('%g' % (v * 1e-5))

	def search_station(self):
		try:
			para = {}
			para['t1'] = self.starttime.text()
			para['t2'] = self.endtime.text()
			para['net'] = self.network.text()
			para['sta'] = self.station.text()
			para['ch'] = self.channel.text()
			para['loc'] = self.location.text()
			para['la0'] = float(self.lat0.text())
			para['lo0'] = float(self.lon0.text())
			para['r1'] = float(self.min_radius.text())
			para['r2'] = float(self.max_radius.text())
			para['la1'] = float(self.min_lat.text())
			para['la2'] = float(self.max_lat.text())
			para['lo1'] = float(self.min_lon.text())
			para['lo2'] = float(self.max_lon.text())
			para['dmc_k'] = self.data_center.currentText()
			if self.rect_search.isChecked():
				para['search_style'] = 'rect'
			else:
				para['search_style'] = 'circle'
			self.sta_search = SearchingStationThread(para)
			self.sta_search.result_signal.connect(self.get_sta)
			self.sta_search.start()
		except Exception:
			QMessageBox.critical(self, 'Error', 'Error in searching station!')

	def get_sta(self, sta):
		self.sta = sta
		QMessageBox.about(self, 'Info', '%d station(s) found!' % len(self.sta))

	def print_station(self):
		if len(self.sta) > 0:
			s = 'Seismic stations: %d\n' % len(self.sta)
			s += '\n'.join(self.sta)
			self.sta_info = QLabel(s, self)
			self.sta_info.setFixedWidth(1200)
			self.sta_info.setFont(QFont('Consolas', 13, QFont.Weight.ExtraLight))
			self.sta_info.setWordWrap(True)
			self.sta_info.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)  # PyQt-5.15
			# self.sta_info.setTextInteractionFlags(Qt.TextSelectableByMouse) # PyQt-5.9
			self.sta_info.setText(s)
			self.new_scroll = QScrollArea(self)
			self.new_scroll.setWidget(self.sta_info)
			self.new_scroll.setContentsMargins(0, 0, 0, 0)
			self.new_scroll.setStyleSheet('QScrollArea{border-color: #999999}')
			self.layout3.removeWidget(self.scroll)
			self.layout3.addWidget(self.new_scroll, 1, 0, 6, 10)
		else:
			QMessageBox.critical(self, 'Error', 'No station data or wrong information!')

	def save_station(self):
		if len(self.sta) > 0:
			s = '%d seismic stations found!\n' % len(self.sta)
			s += '\n'.join(self.sta)
			try:
				f_name, _ = QFileDialog.getSaveFileName(self, os.getcwd(), 'All files(*);;*')
				with open(f_name, 'w') as fout:
					fout.write(s)
				QMessageBox.about(self, 'Message', 'Saved station data in %s!' % f_name)
			except Exception:
				QMessageBox.critical(self, 'Message', 'Cancelled to save stations!')
		else:
			QMessageBox.critical(self, 'Error', 'Error in saving stations!')

	def get_clean_sta(self):
		if len(self.sta) > 0:
			sta = {}
			for line in self.sta:
				tmp = line.split('|')
				n = tmp[0]
				if n not in sta.keys():
					sta[n] = []
				sta[n].append(tmp[1:5])
				self.clean_sta = sta
			k = list(sta.keys())
			self.network_code.clear()
			self.network_code.addItems(k)
			self.network_code.setCurrentText(k[0])
		else:
			self.clean_sta = {}

	def plot_station(self):
		if len(self.sta) > 0:
			c = VisualizationColor()
			colors = c.sta_colors
			cn = len(colors)
			self.get_clean_sta()
			sta = self.clean_sta
			maps = MapChoice()
			maps = maps.map_url
			self.map = folium.Map(location=[0, 0],
								  tiles=maps[self.map_type.currentText()],
								  attr='default',
								  control_scale=True,
								  zoom_start=0.5)
			for k in sta.keys():
				ci = int(np.random.random() * cn)
				data = sta[k]
				n = len(data)
				if n < 1000:
					for line in data:
						s = line[0]
						y = line[1]
						x = line[2]
						tooltip = k + '.' + s + ' ' + y + ' ' + x
						folium.CircleMarker(
							location=(float(y), float(x)),
							radius=3.5,
							tooltip=tooltip,
							color=colors[ci],
							fill=True,
							fill_color=colors[ci],
							fill_opacity=0.7,
							weight=1.5).add_to(self.map)
				else:
					xy = []
					pops = []
					for line in data:
						pops.append(k+'.'+line[0])
						xy.append([float(line[1]), float(line[2])])
					FastMarkerCluster(data=xy, name=pops).add_to(self.map)
			self.map.add_child(folium.LatLngPopup())
			data = io.BytesIO()
			self.map.save(data, close_file=False)
			self.map_view.setHtml(data.getvalue().decode())
		else:
			QMessageBox.critical(self, 'Error', 'No station data!')

	def plot_array_response(self):
		try:
			net = self.network_code.currentText()
			f = float(self.frequency_value.text())
			s2 = float(self.slowness_value.text())
			sta = self.clean_sta[net]
			xy = []
			for d in sta:
				xy.append([float(d[2]), float(d[1])])
			ptype = 0
			if self.cross_position.isChecked():
				ptype = 1
			arf = ArrayResponse(np.array(xy), sys='degree')
			b, s, p = arf.general_harmonic_response(f=f, s2=s2, ptype=ptype)
			fig = self.fig
			fig.clf()
			P = abs(p) ** 2;
			P /= P.max();
			P = 10 * np.log10(P)
			ax = fig.add_subplot(111, projection='polar')
			im = ax.pcolormesh(b, s * 1e3, P, cmap='magma',
							   vmin=self.min_power.value(), vmax=0)
			cbar = fig.colorbar(im, shrink=0.5, pad=0.12)
			cbar.set_label(r'Beam power (dB)', fontsize=13)
			cbar.ax.tick_params(labelsize=13)
			ax.grid(color='#888888', ls=(2, (10, 5)), lw=1)
			ax.tick_params(axis='x', labelsize=12)
			ax.tick_params(axis='y', colors='#888888', labelsize=12, pad=12)
			ax.set_theta_zero_location('N')
			ax.set_theta_direction(-1)
			ax.plot(b, np.ones(len(b)) * s.min() * 1e3, c='gray', lw=2)
			ax.plot(b, np.ones(len(b)) * s.max() * 1e3, c='gray', lw=2)
			ax.set_xlabel('Slowness (s/km)', fontsize=13)
			self.canvas.draw()
		except Exception:
			QMessageBox.critical(self, 'Error', 'Show station first or check the network code!')

if __name__ == '__main__':
	app = QApplication(sys.argv)
	sta = StationWidgetBlock()
	sta.show()
	sys.exit(app.exec_())
