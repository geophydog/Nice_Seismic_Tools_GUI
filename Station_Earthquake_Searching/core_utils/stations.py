from urllib import request
from core_utils.station_data_centers import StationDataCenter


class FDSNStation:
    def __init__(self, la1=-90, la2=90,
                 lo1=-180, lo2=180,
                 t1='2010-01-01T00:00:00',
                 t2='2020-01-01T00:00:00',
                 net='IC,II,IU,G', sta='*',
                 loc='*', ch='LHZ',
                 la0=0, lo0=0,
                 r1=0, r2=50,
                 dmc='IRIS'):
        s = StationDataCenter()
        dc = s.datacenter
        self.la1 = la1
        self.la2 = la2
        self.lo1 = lo1
        self.lo2 = lo2
        self.t1 = t1
        self.t2 = t2
        self.net = net
        self.ch = ch
        self.loc = loc
        self.sta = sta
        self.la0 = la0
        self.lo0 = lo0
        self.r1 = r1
        self.r2 = r2
        self.url = ''
        if dmc in dc.keys():
            tmp = dc[dmc]
        else:
            tmp = dc['IRIS']
        self.base = '%sstation/1/query?' % tmp

    def __sta_request(self, url):
        try:
            req = request.Request(url)
            resp = request.urlopen(req)
            html = resp.read().decode().strip()
            lines = html.split('\n')[1:]
            return lines
        except Exception:
            print('Error in downloading station data!')
            return []

    def sta_rect_search(self):
        url = '%sstarttime=%s&endtime=%s&minlatitude=%g&maxlatitude=%g' % (self.base,
                                                                           self.t1,
                                                                           self.t2,
                                                                           self.la1,
                                                                           self.la2)
        url = '%s&minlongitude=%g&maxlongitude=%g' % (url, self.lo1, self.lo2)
        self.url = url
        self.url = '%s&network=%s&station=%s&location=%s&channel=%s&format=text' % (self.url,
                                                                                    self.net,
                                                                                    self.sta,
                                                                                    self.loc,
                                                                                    self.ch)
        return self.__sta_request(self.url)


    def sta_circle_search(self):
        url = '%sstarttime=%s&endtime=%s&latitude=%g&longitude=%g' % (self.base,
                                                                      self.t1,
                                                                      self.t2,
                                                                      self.la0,
                                                                      self.lo0)
        url = '%s&minradius=%g&maxradius=%g'%(url, self.r1, self.r2)
        self.url = '%s&network=%s&station=%s&location=%s&channel=%s&format=text' % (url,
                                                                                    self.net,
                                                                                    self.sta,
                                                                                    self.loc,
                                                                                    self.ch)
        return self.__sta_request(self.url)