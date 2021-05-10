## :one: Station and earthquake searching based on the FDSN web services ([FDSNWS](http://www.fdsn.org/webservices/datacenters/)).
The motivation of developing these FDSNWS-based searching tools is that the internet may go wrong when showing data on web page.
The slow network speed in some regions also urges us to build some graphical user interface (GUI) to help us to conduct the furture work of processing seismic data.

In folder `Station_Earthquake_Searching`, someone can find two searching tools:
	`widget_earthquake.py` and `widget_station.py`, and we can use them to search earthquakes and seismic stations from different data centers.

### 1.1 Dependencies tested on Windows 10:
- Python3.7 (Anaconda-3.5.3.0)
- PyQt-5.15.4
- matplotlib-3.2.2
- folium-0.12.1
- numpy-1.20.1

### 1.2 Examples:
#### 1.2.1 `earthquake searching`
Run the script `widget_earthquake.py` to keep going.
![earthquake](https://github.com/geophydog/Nice_Seismic_Tools_GUI/blob/main/images/earthquake_example.png)

***
#### 1.2.2 `station searching`
Run the script `widget_station.py` and set some searching parametersyou to see the following GUI.
![station](https://github.com/geophydog/Nice_Seismic_Tools_GUI/blob/main/images/station_example.png)

### 1.3 Combining widgets
You can follow the codes to combine these searching tools in single one GUI.
```python
from PyQt5.QtWidgets import (QTabWidget,
                            QApplication)
from PyQt5.QtGui import (QIcon,
                         QFont)
import sys
from widget_station import StationWidgetBlock
from widget_earthquake import EarthquakeWidgetBlock

class FDSNSearchingService(QTabWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        font = QFont('Consolas', 14, QFont.Weight.Bold)
        self.widget1 = StationWidgetBlock()
        self.widget2 = EarthquakeWidgetBlock()

        self.addTab(self.widget1, 'Station')
        self.addTab(self.widget2, 'Earthquake')

        self.setStyleSheet('QTabBar::tab{width:200}')
        self.setFont(font)
        self.setGeometry(300, 100, 1500, 900)
        self.setWindowTitle('FDSN-based Searching')
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mt = FDSNSearchingService()
    sys.exit(app.exec_())
```


### Contributor
`Geophydog`

`geophydogvon AT gmai.com`
