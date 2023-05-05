import os
import serial
import re
import sys
import folium
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl

serial_port = 'COM4'  # Arduino'nun bağlı olduğu seri port
baud_rate = 9600  # Arduino'da ayarladığınız baud hızı

class MapWindow(QWidget):
    def __init__(self, parent=None):
        super(MapWindow, self).__init__(parent)
        self.setWindowTitle("Sensor Map")

        # Harita oluşturun
        self.map = folium.Map(zoom_start=15)

        # Harita için QWebEngineView kullanın
        self.view = QWebEngineView()
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.view)
        self.setLayout(self.layout)

    def update_map(self, latitude, longitude):
        # Haritayı güncelleyin ve yeni konumu ekleyin
        self.map.location = [latitude, longitude]
        folium.Marker([latitude, longitude]).add_to(self.map)

        # Haritayı görüntülemek için HTML dosyasına kaydedin
        self.map.save("map.html")
        # QWebEngineView'da haritayı yükleyin ve görüntüleyin
        self.view.load(QUrl.fromLocalFile(os.path.abspath("map.html")))

def main():
    app = QApplication(sys.argv)
    map_window = MapWindow()
    map_window.show()

    with serial.Serial(serial_port, baud_rate, timeout=1) as ser:        
        while True:
            line = ser.readline().decode('ascii', errors='replace').strip()
            if line:
                process_serial_data(line, map_window)

    sys.exit(app.exec_())

def process_serial_data(line, map_window):
    # Seri bağlantıdan gelen verileri işleyin ve parçalayın
    match = re.match(
        r"Temperature: ([-+]?[0-9]*\.?[0-9]+) C.*"
        r"Pressure: ([-+]?[0-9]*\.?[0-9]+) hPa.*"
        r"Latitude: ([-+]?[0-9]*\.?[0-9]+).*"
        r"Longitude: ([-+]?[0-9]*\.?[0-9]+)",
        line,
        re.DOTALL,
    )

    if match:
        temperature = float(match.group(1))
        pressure = float(match.group(2))
        latitude = float(match.group(3))
        longitude = float(match.group(4))

        # Verileri kullanarak istediğiniz işlemleri yapın, örneğin:
        print(f"Temperature: {temperature} C")
        print(f"Pressure: {pressure} hPa")
        print(f"Latitude: {latitude}")
        print(f"Longitude: {longitude}")

        # Haritayı güncelleyin
        map_window.update_map(latitude, longitude)

if __name__ == "__main__":
    main()
