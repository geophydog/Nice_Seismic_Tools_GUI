from urllib import request
from core_utils.event_data_centers import EventDataCenter


class FDSNEvent:
    def __init__(self, la1=-90, la2=90,
                 lo1=-180, lo2=180,
                 t1='2010-01-01T00:00:00',
                 t2='2020-01-01T00:00:00',
                 m1=7, m2=8,
                 la0=0, lo0=0,
                 r1=10, r2=25,
                 d1=-1, d2=1000,
                 dmc='USGS'):
        e = EventDataCenter()
        dc = e.datacenter
        self.la1 = la1
        self.la2 = la2
        self.lo1 = lo1
        self.lo2 = lo2
        self.t1 = t1
        self.t2 = t2
        self.m1 = m1
        self.m2 = m2
        self.d1 = d1
        self.d2 = d2
        self.la0 = la0
        self.lo0 = lo0
        self.r1 = r1
        self.r2 = r2
        self.url = ''
        self.dmc = dmc
        self.out_format = 'text'
        if self.dmc in ['ISC-UK', 'ISC-IRIS']:
            self.out_format = 'isf'
        if dmc in dc.keys():
            tmp = dc[dmc]
        else:
            tmp = dc['USGS']
        self.base = '%sevent/1/query?' % tmp

    def __evt_request(self, url):
        try:
            req = request.Request(url)
            resp = request.urlopen(req)
            res = resp.read().decode().strip().split('\n')
            if self.dmc in ['ISC-UK', 'ISC-IRIS']:
                lines = []
                html = res[2:]
                index = 0
                n = len(html)
                while index < n and len(html[index:]) > 7:
                    tmp = html[index].split()
                    eid = tmp[1]
                    region = ' '.join(tmp[2:])
                    tmp = html[index + 2].split()
                    date_time = '-'.join(tmp[0].split('/')) + 'T' + tmp[1]
                    la = tmp[4]
                    lo = tmp[5]
                    depth = tmp[9]
                    ori_id = tmp[-1]
                    mb = html[index + 5].split()[1]
                    MS = html[index + 6].split()[1]
                    s = [eid, date_time, la, lo, depth, 'ISC', 'ISC', 'ISC', ori_id, 'mb', mb, 'MS', MS, 'ISC',
                         html[index], region]
                    out = '|'.join(s)
                    lines.append(out)
                    index += 8
                return lines
            return res[1:]
        except Exception:
            print('Error in downloading event data!')
            return []
    def evt_rect_search(self):
        url = '%sstarttime=%s&endtime=%s&minlatitude=%g&maxlatitude=%g' % (self.base,
                                                                           self.t1,
                                                                           self.t2,
                                                                           self.la1,
                                                                           self.la2)
        url = '%s&minlongitude=%g&maxlongitude=%g' % (url, self.lo1, self.lo2)
        url = '%s&minmagnitude=%g&maxmagnitude=%g' % (url,
                                                      self.m1,
                                                      self.m2)
        self.url = '%s&mindepth=%g&maxdepth=%g&format=%s' % (url,
                                                             self.d1,
                                                             self.d2,
                                                             self.out_format)
        return self.__evt_request(self.url)

    def evt_circle_search(self):
        url = '%sstarttime=%s&endtime=%s&latitude=%g&longitude=%g' % (self.base,
                                                                      self.t1,
                                                                      self.t2,
                                                                      self.la0,
                                                                      self.lo0)
        url = '%s&minradius=%g&maxradius=%g&minmagnitude=%g&maxmagnitude=%g' % (url,
                                                                                self.r1,
                                                                                self.r2,
                                                                                self.m1,
                                                                                self.m2)
        self.url = '%s&mindepth=%g&maxdepth=%g&format=%s' % (url,
                                                             self.d1,
                                                             self.d2,
                                                             self.out_format)
        return self.__evt_request(self.url)