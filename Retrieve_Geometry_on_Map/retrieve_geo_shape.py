from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtWidgets import (QWidget,
							 QApplication,
							 QGridLayout,
							 QPushButton,
							 QFrame,
							 QSplitter,
							 QHBoxLayout,
							 QScrollArea,
							 QLabel,
							 QComboBox,
							 QFileDialog,
							 QMessageBox)
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont, QIcon
from folium.plugins import Draw
import folium, io, sys, json
from core_utils.map_types import MapChoice
from core_utils.ui_base_style import UIBaseStyle
import os

class InformationWebPageConsole(QWebEnginePage):
	lonlat = pyqtSignal(list)
	def javaScriptConsoleMessage(self, level, msg, line, sourceID):
		coords_dict = json.loads(msg)
		self.coords = coords_dict['geometry']['coordinates']
		self.lonlat.emit(self.coords)

class RetrievingGeoShape(QWidget):
	def __init__(self):
		super().__init__()
		self.lonlat = []
		self.initUI()

	def initUI(self):
		self.font = QFont('Consolas', 13, QFont.Weight.Bold)
		self.base_style = UIBaseStyle()

		# -------------------- Geomap ----------------- #
		self.map_type = QComboBox()
		self.map_type.setFont(self.font)
		self.map_type.setStyleSheet(self.base_style.editline_style)
		self.map_type.setMaximumWidth(200)
		self.map_type.addItems(['GaodeStreet', 'GaodeSatellite',
								'OpenTopoZhLa', 'Russian',
								'StamenWaterColor', 'HikeBikeMultiLa',
								'ArcgisChinaEnLa', 'ArcgisOnlineEnLa',
								'WorldStreetMap', 'WorldTopoMap'])
		self.map_type.setCurrentText('ArcgisOnlineEnLa')
		map_url = MapChoice()
		self.map = folium.Map(location=[0, 0],
              tiles=map_url.map_url[self.map_type.currentText()],
              attr='default',
              control_scale=True,
              zoom_start=0.5)
		self.show_map = QPushButton('Show background map')
		self.show_map.setFont(self.font)
		self.show_map.setMaximumWidth(300)
		self.show_map.setStyleSheet(self.base_style.btn_style1)
		self.show_map.clicked.connect(self.showGeoMap)
		self.show_map.setIcon(QIcon('pic/PLOT.jpg'))
		draw = Draw(
				draw_options={
					'polyline': True,
					'rectangle': True,
					'polygon': True,
					'circle': False,
					'marker': False,
					'circlemarker': False},
				edit_options={'edit': False})
		self.map.add_child(draw)
		folium.Rectangle([[-90, -180], [90, -180], [90, 180], [-90, 180], [-90, -180]]).add_to(self.map)
		# self.map.add_child(folium.LatLngPopup())
		data = io.BytesIO()
		self.map.save(data, close_file=False)
		self.map_view = QWebEngineView()
		self.page = InformationWebPageConsole(self.map_view)
		self.page.lonlat.connect(self.getLonLat)
		self.map_view.setPage(self.page)
		self.map_view.setHtml(data.getvalue().decode())

		# -------------------- print and save data ---------------------- #
		self.print_data = QPushButton('Print geometry info.')
		self.print_data.setFont(self.font)
		self.print_data.setMaximumWidth(300)
		self.print_data.setStyleSheet(self.base_style.btn_style1)
		self.print_data.clicked.connect(self.printLonLat)
		self.print_data.setIcon(QIcon('pic/PRINT.jpg'))

		self.save_data = QPushButton('Save geometry data')
		self.save_data.setFont(self.font)
		self.save_data.setMaximumWidth(300)
		self.save_data.setStyleSheet(self.base_style.btn_style1)
		self.save_data.clicked.connect(self.saveLonLat)
		self.save_data.setIcon(QIcon('pic/SAVE.jpg'))

		# ------------------ Print lonlat information ------------------- #
		self.base_info = QLabel('Information about retrieved data ...')
		self.base_info.setFont(self.font)
		self.base_info.setWordWrap(True)
		self.scroll = QScrollArea()
		self.scroll.setContentsMargins(0, 0, 0, 0)
		self.scroll.setStyleSheet('QScrollArea{border-color: #999999}')
		self.scroll.setWidget(self.base_info)

		# ------------------ Layout of the whole GUI ------------ #
		self.lay1 = QGridLayout()
		self.lay2 = QGridLayout()

		self.lay1.addWidget(self.show_map, 0, 0, 1, 3)
		self.lay1.addWidget(self.map_type, 0, 3, 1, 3)
		self.lay1.addWidget(self.save_data, 0, 6, 1, 3)
		self.lay1.addWidget(self.map_view, 1, 0, 10, 10)

		self.lay2.addWidget(self.print_data, 0, 0, 1, 10)
		self.lay2.addWidget(self.scroll, 1, 0, 5, 10)

		self.frame1 = QFrame()
		self.frame1.setFrameShape(QFrame.Shape.StyledPanel)
		self.frame1.setFrameShadow(QFrame.Shadow.Sunken)
		self.frame1.setLayout(self.lay1)

		self.frame2 = QFrame()
		self.frame2.setFrameShape(QFrame.Shape.StyledPanel)
		self.frame2.setFrameShadow(QFrame.Shadow.Sunken)
		self.frame2.setLayout(self.lay2)


		splitter1 = QSplitter(Qt.Orientation.Horizontal)
		splitter1.addWidget(self.frame1)
		splitter2 = QSplitter(Qt.Orientation.Vertical)
		splitter2.addWidget(self.frame2)

		splitter3 = QSplitter(Qt.Orientation.Horizontal)
		splitter3.addWidget(splitter1)
		splitter3.addWidget(splitter2)
		hbox = QHBoxLayout()
		hbox.addWidget(splitter3)
		self.setLayout(hbox)
		self.setGeometry(50, 75, 1500, 750)
		self.setWindowTitle('Geo Data')
		self.setWindowIcon(QIcon('pic/LOGO.png'))

	def getLonLat(self, lonlat):
		self.lonlat = lonlat

	def printLonLat(self):
		if len(self.lonlat) > 0:
			data = self.lonlat.copy()
			if len(data) == 1:
				data = data[0]
			s = '\n'.join([str(data[i][0])+' '+str(data[i][1]) for i in range(len(data))])
			self.data_info = QLabel(s, self)
			self.data_info.setFixedWidth(1200)
			self.data_info.setFont(QFont('Consolas', 13, QFont.Weight.ExtraLight))
			self.data_info.setWordWrap(True)
			self.data_info.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
			self.data_info.setText(s)
			self.new_scroll = QScrollArea(self)
			self.new_scroll.setWidget(self.data_info)
			self.new_scroll.setContentsMargins(0, 0, 0, 0)
			self.new_scroll.setStyleSheet('QScrollArea{border-color: #999999}')
			self.lay2.removeWidget(self.scroll)
			self.lay2.addWidget(self.new_scroll, 1, 0, 5, 10)
		else:
			QMessageBox.critical(self, 'Error', 'No data! Retrieve data first!')

	def saveLonLat(self):
		if len(self.lonlat) > 0:
			data = self.lonlat.copy()
			if len(data) == 1:
				data = data[0]
			try:
				f_name, _ = QFileDialog.getSaveFileName(self, os.getcwd(), 'All files(*);;*')
				s = '\n'.join([str(data[i][0]) + ' ' + str(data[i][1]) for i in range(len(data))])
				with open(f_name, 'w') as fout:
					fout.write(s)
				QMessageBox.about(self, 'Message', 'Data was saved in %s!' % f_name)

			except Exception:
				QMessageBox.critical(self, 'Message', 'Cancelled to save data!')
		else:
			QMessageBox.critical(self, 'Error', 'No data! Retrieve data first!')

	def showGeoMap(self):
		maps = MapChoice()
		maps = maps.map_url
		self.map = folium.Map(location=[0, 0],
							  tiles=maps[self.map_type.currentText()],
							  attr='default',
							  control_scale=True,
							  zoom_start=0.5)
		draw = Draw(
			draw_options={
				'polyline': True,
				'rectangle': True,
				'polygon': True,
				'circle': False,
				'marker': False,
				'circlemarker': False},
			edit_options={'edit': False})
		self.map.add_child(draw)
		folium.Rectangle([[-90, -180], [90, -180], [90, 180], [-90, 180], [-90, -180]]).add_to(self.map)
		data = io.BytesIO()
		self.map.save(data, close_file=False)
		self.new_map_view = QWebEngineView()
		self.page = InformationWebPageConsole(self.new_map_view)
		self.page.lonlat.connect(self.getLonLat)
		self.new_map_view.setPage(self.page)
		self.new_map_view.setHtml(data.getvalue().decode())
		self.lay1.removeWidget(self.map_view)
		self.lay1.addWidget(self.new_map_view, 1, 0, 10, 10)

if __name__ == '__main__':
	app = QApplication(sys.argv)
	r = RetrievingGeoShape()
	r.show()
	sys.exit(app.exec_())