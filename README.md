## :one: Station and earthquake searching based on the FDSN web services ([FDSNWS](http://www.fdsn.org/webservices/datacenters/)).
The motivation of developing these FDSNWS-based searching tools is that the internet may go wrong when showing data on web page.
The slow network speed in some regions also urges us to build some graphical user interface (GUI) to help us to conduct the furture work of processing seismic data.

In folder `Station_Earthquake_Searching`, someone can find two searching tools:
	`widget_earthquake.py` and `widget_station.py`, and we can use them to search earthquakes and seismic stations from different data centers.

### Dependencies tested on Windows 10:
- Python3.7 (Anaconda-3.5.3.0)
- PyQt-5.15.4
- matplotlib-3.2.2
- folium-0.12.1
- numpy-1.20.1

### Examples:
`earthquake searching`
![earthquake](https://github.com/geophydog/Nice_Seismic_Tools_GUI/blob/main/images/earthquake_example.png)

`station searching`
![station](https://github.com/geophydog/Nice_Seismic_Tools_GUI/blob/main/images/station_example.png)
