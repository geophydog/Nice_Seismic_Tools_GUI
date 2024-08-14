from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PyQt5.QtWidgets import (QWidget,
							 QPushButton,
							 QGridLayout,
							 QApplication,
							 QFileDialog,
							 QDoubleSpinBox,
							 QLabel,
							 QMessageBox,
							 QLineEdit)
from PyQt5.QtGui import QFont
import sys
import os
import numpy as np
import matplotlib as mpl
from matplotlib.path import Path
from matplotlib.widgets import Cursor
from scipy.signal import savgol_filter as sgolay
#from colors import Colors

class PickDispersionCurveBlock(QWidget):
	def __init__(self):
		super().__init__()
		self.initUI()

	def initUI(self):
		self.font = QFont('Consolas', 13, QFont.Weight.Bold)

		# Fields of storing data.
		self.file_index = 0
		self.spectrum_files = []
		self.dispersion_curves = {}

		# Frequency and velocity ranges.
		# Values.
		self.fre_1 = QLineEdit()
		self.fre_1.setMaximumWidth(200)
		self.fre_1.setFont(self.font)
		self.fre_1.setText('0')
		self.fre_2 = QLineEdit()
		self.fre_2.setMaximumWidth(200)
		self.fre_2.setFont(self.font)
		self.fre_2.setText('40')

		self.vel_1 = QLineEdit()
		self.vel_1.setMaximumWidth(200)
		self.vel_1.setFont(self.font)
		self.vel_1.setText('1.5')
		self.vel_2 = QLineEdit()
		self.vel_2.setMaximumWidth(200)
		self.vel_2.setFont(self.font)
		self.vel_2.setText('5')

		self.array_size = QLineEdit()
		self.array_size.setMaximumWidth(200)
		self.array_size.setFont(self.font)
		self.array_size.setText('10.0')

		self.smooth_size = QLineEdit()
		self.smooth_size.setMaximumWidth(200)
		self.smooth_size.setFont(self.font)
		self.smooth_size.setText('11')

		# Label tags.
		self.fre_1_tag = QLabel('f1 (Hz)')
		self.fre_1_tag.setMaximumWidth(200)
		self.fre_1_tag.setFont(self.font)
		self.fre_2_tag = QLabel('f2 (Hz)')
		self.fre_2_tag.setMaximumWidth(200)
		self.fre_2_tag.setFont(self.font)
		self.vel_1_tag = QLabel('v1 (km/s)')
		self.vel_1_tag.setMaximumWidth(200)
		self.vel_1_tag.setFont(self.font)
		self.vel_2_tag = QLabel('v2 (km/s)')
		self.vel_2_tag.setMaximumWidth(200)
		self.vel_2_tag.setFont(self.font)
		self.array_size_tag = QLabel('Array size (km)')
		self.array_size_tag.setMaximumWidth(200)
		self.array_size_tag.setFont(self.font)
		self.smooth_size_tag = QLabel('Smooth size (odd no.)')
		self.smooth_size_tag.setMaximumWidth(200)
		self.smooth_size_tag.setFont(self.font)

		# Button of loading f-j spectrum file names.
		self.load_spectrum_file_btn = QPushButton('Load Spectrum Files')
		self.load_spectrum_file_btn.setMaximumWidth(400)
		self.load_spectrum_file_btn.setFont(self.font)
		self.load_spectrum_file_btn.clicked.connect(self.load_spectrum_files_func)

		# Button of picking dispersion curves from f-j spectrum
		self.pick_dispersion_curve_btn = QPushButton('Start Picking')
		self.pick_dispersion_curve_btn.setMaximumWidth(400)
		self.pick_dispersion_curve_btn.setFont(self.font)
		self.pick_dispersion_curve_btn.clicked.connect(self.pick_dispersion_curve_from_spectrum_func)

		# Button ofs going next or previous spectrum file.
		self.next_spectrum_file_btn = QPushButton('Next spectrum')
		self.next_spectrum_file_btn.setMaximumWidth(200)
		self.next_spectrum_file_btn.setFont(self.font)
		self.next_spectrum_file_btn.clicked.connect(self.next_spectrum_file_func)
		self.previous_spectrum_file_btn = QPushButton('Previous spectrum')
		self.previous_spectrum_file_btn.setMaximumWidth(200)
		self.previous_spectrum_file_btn.setFont(self.font)
		self.previous_spectrum_file_btn.clicked.connect(self.previous_spectrum_file_func)

		# Label of the next spectrum file.
		self.spectrum_file_tag = QLabel('')
		self.spectrum_file_tag.setFont(self.font)

		# Mode number of dispersion curve.
		self.mode_value = QDoubleSpinBox()
		self.mode_value.setFont(self.font)
		self.mode_value.setRange(0, 10)
		self.mode_value.setSingleStep(1)
		self.mode_value.setDecimals(0)
		self.mode_value.setValue(0)

		# Mode number label of dispersion curve.
		self.mode_value_tag = QLabel('Mode:')
		self.mode_value_tag.setFont(self.font)

		# Button of saving dispersion curve data.
		self.save_dispersion_curve_btn = QPushButton('Save Dispersion Data')
		self.save_dispersion_curve_btn.setFont(self.font)
		self.save_dispersion_curve_btn.clicked.connect(self.save_dispersion_curve_func)

		# Spectrum figure for picking dispersion curve.
		self.fig = Figure()
		self.canvas = FigureCanvas(self.fig)
		self.toolbar = NavigationToolbar(self.canvas, self)

		# Layout of all buttons, labels, panels and text boxes.
		self.layout1 = QGridLayout()
		self.layout1.addWidget(self.load_spectrum_file_btn, 0, 0, 1, 2)
		self.layout1.addWidget(self.pick_dispersion_curve_btn, 1, 0, 1, 2)
		self.layout1.addWidget(self.mode_value_tag, 2, 0, 1, 1)
		self.layout1.addWidget(self.mode_value, 2, 1, 1, 1)


		self.layout1.addWidget(self.fre_1_tag, 3, 0, 1, 1)
		self.layout1.addWidget(self.fre_1, 3, 1, 1, 1)
		self.layout1.addWidget(self.fre_2_tag, 4, 0, 1, 1)
		self.layout1.addWidget(self.fre_2, 4, 1, 1, 1)
		self.layout1.addWidget(self.vel_1_tag, 5, 0, 1, 1)
		self.layout1.addWidget(self.vel_1, 5, 1, 1, 1)
		self.layout1.addWidget(self.vel_2_tag, 6, 0, 1, 1)
		self.layout1.addWidget(self.vel_2, 6, 1, 1, 1)
		self.layout1.addWidget(self.array_size_tag, 7, 0, 1, 1)
		self.layout1.addWidget(self.array_size, 7, 1, 1, 1)
		self.layout1.addWidget(self.smooth_size_tag, 8, 0, 1, 1)
		self.layout1.addWidget(self.smooth_size, 8, 1, 1, 1)

		self.layout1.addWidget(self.previous_spectrum_file_btn, 9, 0, 1, 1)
		self.layout1.addWidget(self.next_spectrum_file_btn, 9, 1, 1, 1)
		self.layout1.addWidget(self.save_dispersion_curve_btn, 10, 0, 1, 2)

		self.layout1.addWidget(self.spectrum_file_tag, 0, 3, 1, 8)
		self.layout1.addWidget(self.toolbar, 1, 3, 1, 8)
		self.layout1.addWidget(self.canvas, 2, 3, 10, 8)

		self.setLayout(self.layout1)
		self.setWindowTitle('DispPicker')
		self.setGeometry(200, 100, 1500, 700)


	def show_dispersion_spectrum(self):
		file = self.spectrum_files[self.file_index]
		tmp = file.split('_')
		self.array_size.setText(str(float(tmp[-1][:-5])/1e3))
		dc = np.loadtxt(file)
		np.maximum(dc, 0)
		f1 = float(self.fre_1.text())
		f2 = float(self.fre_2.text())
		c1 = float(self.vel_1.text())
		c2 = float(self.vel_2.text())
		sa = float(self.array_size.text())
		nf = len(dc[0])
		nc = len(dc[:, 0])
		f = np.linspace(f1, f2, nf)
		c = np.linspace(c1, c2, nc)
		fig = self.fig
		fig.clf()
		ax = fig.add_subplot(111)
		im = ax.pcolormesh(f, c, dc, cmap=self.cmap)
		cbar = fig.colorbar(im)
		cbar.ax.tick_params(labelsize=11)
		cbar.set_label('Amplitude', fontsize=12)
		ax.plot(f, f * sa, 'w--', lw=1.5)
		ax.tick_params(labelsize=12)
		ax.set_xlabel('Frequency (Hz)', fontsize=13)
		ax.set_ylabel('Phase velocity (km/s)', fontsize=13)
		ax.set_xlim(f1, f2)
		ax.set_ylim(c1, c2)
		self.canvas.draw()
	def load_spectrum_files_func(self):
		try:
			self.dispersion_curves = {}
			f_name, _ = QFileDialog.getOpenFileNames(self, os.getcwd(), filter='All files(*);;*')
			self.spectrum_files= f_name
			self.file_index = 0
			self.spectrum_file_tag.setText(self.spectrum_files[self.file_index])
			self.mode_value.setValue(0)
			#c = Colors()
			# self.cmap = mpl.colors.LinearSegmentedColormap.from_list('cmap', c.color3.split(), 101)
			self.cmap = 'jet'
			self.show_dispersion_spectrum()
		except Exception:
			QMessageBox.critical(self, 'Error!', 'Can not load spectrum files!')

	def pick_dispersion_curve_from_spectrum_func(self):
		try:
			if len(self.spectrum_files) <= self.file_index:
				return
			dc = np.loadtxt(self.spectrum_files[self.file_index])
			np.maximum(dc, 0)
			f1 = float(self.fre_1.text())
			f2 = float(self.fre_2.text())
			c1 = float(self.vel_1.text())
			c2 = float(self.vel_2.text())
			sa = float(self.array_size.text())
			nf = len(dc[0])
			nc = len(dc[:, 0])
			f = np.linspace(f1, f2, nf)
			c = np.linspace(c1, c2, nc)
			ff, cc = np.meshgrid(f, c)

			fig = self.fig
			fig.clf()
			ax = fig.add_subplot(111)
			im = ax.pcolormesh(f, c, dc, cmap=self.cmap)
			cbar = fig.colorbar(im)
			cbar.ax.tick_params(labelsize=11)
			cbar.set_label('Amplitude', fontsize=12)
			ax.plot(f, f*sa, 'w--', lw=1.5)
			ax.tick_params(labelsize=12)
			ax.set_xlabel('Frequency (Hz)', fontsize=13)
			ax.set_ylabel('Phase velocity (km/s)', fontsize=13)
			ax.set_xlim(f1, f2)
			ax.set_ylim(c1, c2)
			cursor = Cursor(ax, useblit=True, color='k', linewidth=1, ls='--')
			polygon = fig.ginput(n=-1, timeout=-1, show_clicks=True)
			polygon = np.array(polygon)
			path = Path(polygon)
			points = np.vstack((ff.flatten(), cc.flatten())).T
			grid = path.contains_points(points)
			grid = grid.reshape((nc, nf))
			disp_region = grid * dc
			ax.plot(polygon[:, 0], polygon[:, 1], 'go-', lw=1)
			fc = []
			mode = self.mode_value.value()
			for i in range(nf):
				if not any(grid[:, i]):
					continue
				ci = np.argmax(disp_region[:, i])
				fc.append([f[i], c[ci], mode])
			fc = np.array(fc)
			sl = int(self.smooth_size.text())
			if not sl%2:
				sl += 1
			fc[:, 1] = sgolay(fc[:, 1], sl, 2)
			self.dispersion_curves[str(mode)] = fc
			self.mode_value.setValue(self.mode_value.value()+1)
			ax.scatter(fc[:, 0], fc[:, 1], marker='.', s=25, color='k', alpha=0.5)
			self.canvas.draw()
		except Exception:
			QMessageBox.critical(self, 'Picking Error', 'Error in picking dispersion data!')

	def next_spectrum_file_func(self):
		self.file_index += 1
		if len(self.spectrum_files) > self.file_index:
			self.spectrum_file_tag.setText(self.spectrum_files[self.file_index])
			self.mode_value.setValue(0)
			self.dispersion_curves = {}
			self.show_dispersion_spectrum()
		else:
			QMessageBox.critical(self, 'Warning!', 'Last file!')

	def previous_spectrum_file_func(self):
		if self.file_index > 0:
			self.file_index -= 1
			self.spectrum_file_tag.setText(self.spectrum_files[self.file_index])
			self.mode_value.setValue(0)
			self.dispersion_curves = {}
			self.show_dispersion_spectrum()
		else:
			QMessageBox.critical(self, 'Warning', 'First file!')

	def save_dispersion_curve_func(self):
		if self.dispersion_curves:
			f_name = self.spectrum_files[self.file_index]
			tmp = f_name.split('/')
			dir_name = '/'.join(tmp[:-1])
			dc_name = dir_name + '/' + 'DC_' + tmp[-1]
			data = np.vstack([self.dispersion_curves[k] for k in self.dispersion_curves.keys()])
			np.savetxt(dc_name, data)
			QMessageBox.about(self, 'Info.', 'Dispersion data saved in'+dc_name)
		else:
			QMessageBox.critical(self, 'Error!!!', 'No dispersion data to save!')


if __name__ == '__main__':
	app = QApplication(sys.argv)
	pdc = PickDispersionCurveBlock()
	pdc.show()
	sys.exit(app.exec_())
