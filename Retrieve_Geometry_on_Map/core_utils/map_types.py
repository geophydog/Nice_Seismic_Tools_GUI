class MapChoice:
    def __init__(self):
        map_url = {}
        map_url['GaodeStreet']      = 'http://webrd02.is.autonavi.com/appmaptile?lang=zh_cn' + \
                                      '&size=1&scale=1&style=7&x={x}&y={y}&z={z}'
        map_url['GaodeSatellite']   = 'http://webst02.is.autonavi.com/appmaptile?style=6' + \
                                      '&x={x}&y={y}&z={z}'
        map_url['OpenTopoZhLa']     = 'https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png'
        map_url['Russian']          = 'http://{s}.tiles.maps.sputnik.ru/{z}/{x}/{y}.png'
        map_url['StamenWaterColor'] = 'http://{s}.tile.stamen.com/watercolor/{z}/{x}/{y}.jpg'
        map_url['HikeBikeMultiLa']  = 'http://{s}.tiles.wmflabs.org/hikebike/{z}/{x}/{y}.png'
        map_url['ArcgisChinaEnLa']  = 'https://map.geoq.cn/arcgis/rest/services/ChinaOnline' + \
                                      'CommunityENG/MapServer/tile/{z}/{y}/{x}'
        map_url['ArcgisChinaZhLa']  = 'https://map.geoq.cn/arcgis/rest/services/ChinaOnline' + \
                                      'Community_Mobile/MapServer/tile/{z}/{y}/{x}'
        map_url['ArcgisOnlineEnLa'] = 'https://server.arcgisonline.com/ArcGIS/rest/services/' + \
                                      'World_Imagery/MapServer/tile/{z}/{y}/{x}.png'
        map_url['WorldStreetMap']   = 'http://services.arcgisonline.com/arcgis/rest/services/' + \
                                      'World_Street_Map/MapServer/tile/{z}/{y}/{x}'
        map_url['WorldTopoMap']     = 'http://services.arcgisonline.com/arcgis/rest/services/' + \
                                      'World_Topo_Map/MapServer/tile/{z}/{y}/{x}'
        self.map_url = map_url