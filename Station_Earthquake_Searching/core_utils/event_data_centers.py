class EventDataCenter():
    def __init__(self):
        dmc = {}
        dmc['EMSC']     = 'http://www.seismicportal.eu/fdsnws/'
        dmc['ETHZ']     = 'http://arclink.ethz.ch/fdsnws/'
        dmc['INGV']     = 'http://webservices.ingv.it/fdsnws/'
        dmc['IRIS']     = 'http://service.iris.edu/fdsnws/'
        dmc['ISC-UK']   = 'http://www.isc.ac.uk/fdsnws/'
        dmc['ISC-IRIS'] = 'http://isc-mirror.iris.washington.edu/fdsnws/'
        dmc['NCEDC']    = 'http://service.ncedc.org/fdsnws/'
        dmc['SCEDC']    = 'http://service.scedc.caltech.edu/fdsnws/'
        dmc['USGS']     = 'http://earthquake.usgs.gov/fdsnws/'
        self.datacenter = dmc