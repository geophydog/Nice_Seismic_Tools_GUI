class StationDataCenter():
    def __init__(self):
        dmc = {}
        dmc['AUSPASS']    = 'http://auspass.edu.au:80/fdsnws/'
        dmc['BATS']       = 'http://batsws.earth.sinica.edu.tw/fdsnws/'
        dmc['BGR']        = 'http://eida.bgr.de/fdsnws/'
        dmc['ETH']        = 'http://eida.ethz.ch/fdsnws/'
        dmc['GEONET']     = 'http://service.geonet.org.nz/fdsnws/'
        dmc['GFZ']        = 'http://geofon.gfz-potsdam.de/fdsnws/'
        dmc['ICGC']       = 'hhttp://ws.icgc.cat/fdsnws/'
        dmc['INGV']       = 'http://webservices.ingv.it/fdsnws/'
        dmc['IPGP']       = 'http://ws.ipgp.fr/fdsnws/'
        dmc['IRIS']       = 'http://service.iris.edu/fdsnws/'
        dmc['IRISPH5']    = 'http://service.iris.edu/ph5ws/'
        dmc['KNMI']       = 'http://rdsa.knmi.nl/fdsnws/'
        dmc['KOERI']      = 'http://eida-service.koeri.boun.edu.tr/fdsnws/'
        dmc['LMU']        = 'http://erde.geophysik.uni-muenchen.de/fdsnws/'
        dmc['NCEDC']      = 'http://service.ncedc.org/fdsnws/'
        dmc['NIEP']       = 'http://eida-sc3.infp.ro/fdsnws/'
        dmc['NOA']        = 'http://eida.gein.noa.gr/fdsnws/'
        dmc['ODC']        = 'http://www.orfeus-eu.org/'
        dmc['ORFEUS']     = 'http://www.orfeus-eu.org/fdsnws/'
        dmc['RASPISHAKE'] = 'https://fdsnws.raspberryshakedata.com/fdsnws/'
        dmc['RESIF']      = 'http://ws.resif.fr/fdsnws/'
        dmc['SCEDC']      = 'http://service.scedc.caltech.edu/fdsnws/'
        dmc['SED']        = 'http://eida.ethz.ch/fdsnws/'
        dmc['TEXNET']     = 'http://rtserve.beg.utexas.edu/fdsnws/'
        dmc['UIB-NORSAR'] = 'http://eida.geo.uib.no/fdsnws/'
        dmc['USGS']       = 'http://earthquake.usgs.gov/'
        dmc['USP']        = 'http://seisrequest.iag.usp.br/fdsnws/'
        self.datacenter   = dmc