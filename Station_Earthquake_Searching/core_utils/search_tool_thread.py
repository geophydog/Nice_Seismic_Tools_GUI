from PyQt5.QtCore import QThread, pyqtSignal
from core_utils.stations import FDSNStation as Station
from core_utils.events import FDSNEvent as Event

class SearchingStationThread(QThread):
	result_signal = pyqtSignal(list)
	def __init__(self, para):
		super(SearchingStationThread, self).__init__()
		self.para = para

	def run(self):
		para = self.para
		t1 = para['t1']
		t2 = para['t2']
		net = para['net']
		sta = para['sta']
		ch = para['ch']
		loc = para['loc']
		la0 = para['la0']
		lo0 = para['lo0']
		r1 = para['r1']
		r2 = para['r2']
		la1 = para['la1']
		la2 = para['la2']
		lo1 =  para['lo1']
		lo2 = para['lo2']
		dmc_k = para['dmc_k']
		search_style = para['search_style']
		sta_search = Station(la1=la1, la2=la2, lo1=lo1, lo2=lo2,
							 t1=t1, t2=t2, net=net, sta=sta, loc=loc, ch=ch,
							 la0=la0, lo0=lo0, r1=r1, r2=r2, dmc=dmc_k)
		if search_style == 'rect':
			result = sta_search.sta_rect_search()
		else:
			result = sta_search.sta_circle_search()
		self.result_signal.emit(result)

# Sub-thread of searching earthquakes.
class SearchingEarthquakeThread(QThread):
	result_signal = pyqtSignal(list)
	def __init__(self, para):
		super(SearchingEarthquakeThread, self).__init__()
		self.para = para

	def run(self):
		para = self.para
		evt_search = Event(la1=para['la1'], la2=para['la2'],
						   lo1=para['lo1'], lo2=para['lo2'],
						   t1=para['t1'], t2=para['t2'],
						   m1=para['m1'], m2=para['m2'],
						   la0=para['la0'], lo0=para['lo0'],
						   r1=para['r1'], r2=para['r2'],
						   d1=para['d1'], d2=para['d2'],
						   dmc=para['dmc'])
		if para['search_style'] == 'rect':
			result = evt_search.evt_rect_search()
		else:
			result = evt_search.evt_circle_search()
		self.result_signal.emit(result)