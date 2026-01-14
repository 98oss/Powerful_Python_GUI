
import PyQt5
import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtCore as QtCore
import speedtest_logger
import weather
from speedometer_gauge import SpeedometerGauge

class SpeedTestThread(QtCore.QThread):
    speedTestCompleted = QtCore.pyqtSignal(str, str, float, float)
    progressUpdate = QtCore.pyqtSignal(str)
    testingDownload = QtCore.pyqtSignal()  # Signal when download starts
    testingUpload = QtCore.pyqtSignal()    # Signal when upload starts

    def run(self):
        print("Thread run() started!")
        try:
            print("Emitting first progress...")
            self.progressUpdate.emit("Starting WIFI speed test...")

            print("Calling download...")
            self.progressUpdate.emit("Running download test...")
            self.testingDownload.emit()
            download_result = speedtest_logger.download()
            download_mbps = 0
            try:
                if "error" not in download_result.lower():
                    download_mbps = float(download_result.split(":")[1].strip().split()[0])
            except:
                pass
            print(f"Download done: {download_result}")

            print("Calling upload...")
            self.progressUpdate.emit("Running upload test...")
            self.testingUpload.emit()
            upload_result = speedtest_logger.upload()
            upload_mbps = 0
            try:
                if "error" not in upload_result.lower():
                    upload_mbps = float(upload_result.split(":")[1].strip().split()[0])
            except:
                pass
            print(f"Upload done: {upload_result}")

            self.progressUpdate.emit("WIFI speed test completed.")
            self.speedTestCompleted.emit(download_result, upload_result, download_mbps, upload_mbps)
            print("Signals emitted!")
        except Exception as e:
            print(f"Exception in thread: {e}")
            self.progressUpdate.emit(f"Error during speed test: {e}")
    

######################MAIN WINDOW#####################
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Morti GUI")
        self.setGeometry(100, 100, 800, 600)
        
        # Track current theme
        self.is_dark_mode = True
        
        # Define themes
        self.dark_theme = """
            QMainWindow {
                background-color: #1e1e1e;
            }
            QWidget {
                background-color: #1e1e1e;
                color: #ffffff;
            }
            QPushButton {
                background-color: #0d7377;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #14a085;
            }
            QPushButton:pressed {
                background-color: #0a5f63;
            }
            QPushButton:disabled {
                background-color: #555555;
                color: #888888;
            }
            QTextEdit {
                background-color: #252525;
                color: #ffffff;
                border: 1px solid #3a3a3a;
                border-radius: 5px;
                padding: 5px;
            }
            QLineEdit {
                background-color: #252525;
                color: #ffffff;
                border: 1px solid #3a3a3a;
                border-radius: 5px;
                padding: 5px;
            }
            QLabel {
                color: #ffffff;
            }
            QDockWidget {
                background-color: #2d2d2d;
                color: #ffffff;
                titlebar-close-icon: url(close.png);
                titlebar-normal-icon: url(float.png);
            }
            """
    
        self.light_theme = """
            QMainWindow {
                background-color: #f5f5f5;
            }
            QWidget {
                background-color: #f5f5f5;
                color: #000000;
            }
            QPushButton {
                background-color: #0d7377;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #14a085;
            }
            QPushButton:pressed {
                background-color: #0a5f63;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
            QTextEdit {
                background-color: #ffffff;
                color: #000000;
                border: 1px solid #cccccc;
                border-radius: 5px;
                padding: 5px;
            }
            QLineEdit {
                background-color: #ffffff;
                color: #000000;
                border: 1px solid #cccccc;
                border-radius: 5px;
                padding: 5px;
            }
            QLabel {
                color: #000000;
            }
            QDockWidget {
                background-color: #e0e0e0;
                color: #000000;
            }
        """
    
        # Apply dark theme by default
        self.setStyleSheet(self.dark_theme)
        

        self.stacked_widget = QtWidgets.QStackedWidget()

                #Create Different Pages
        self.home_page = self.create_home_page()
        self.wifi_speed_page = self.create_speedtest_page()
        self.weather_page = self.create_weather_page()
        self.settings_page = self.create_settings_page()



        #Add pages to stacked widget
        self.stacked_widget.addWidget(self.home_page)          # Index 0
        self.stacked_widget.addWidget(self.wifi_speed_page)    # Index 1
        self.stacked_widget.addWidget(self.weather_page)       # Index 2
        self.stacked_widget.addWidget(self.settings_page)      # Index 3

            
        #Setting as central widget
        self.setCentralWidget(self.stacked_widget)




            #sidebar widgets and input
        sidebar = QtWidgets.QDockWidget("Menu", self)
        sidebar_content = QtWidgets.QWidget()
        sidebar_layout = QtWidgets.QVBoxLayout()




            #Create sidebar dock
        home_btn = QtWidgets.QPushButton("Home") 
        home_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        sidebar_layout.addWidget(home_btn)


        speed_btn = QtWidgets.QPushButton("Wifi Speed")
        speed_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        sidebar_layout.addWidget(speed_btn)

        weather_btn = QtWidgets.QPushButton("Weather")
        weather_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        sidebar_layout.addWidget(weather_btn)

        settings_btn = QtWidgets.QPushButton("Settings")
        settings_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(3))
        sidebar_layout.addWidget(settings_btn)


        sidebar_content.setLayout(sidebar_layout)
        sidebar.setWidget(sidebar_content)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, sidebar)

    def create_home_page(self):
        page = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()




        #Home page content
        title = QtWidgets.QLabel("Welcome to Morti GUI")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        title.setAlignment(QtCore.Qt.AlignCenter) 

        subtitle = QtWidgets.QLabel("Select an option from the sidebar to get started.")
        subtitle.setAlignment(QtCore.Qt.AlignCenter)

        #Status display

        info = QtWidgets.QTextEdit()
        info.setReadOnly(True)
        info.append("Features:\n - Wifi Speed Test\n - Weather Information\n - Settings")


        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(info)
        layout.addStretch()

        page.setLayout(layout)
        return page
    
###############SPEEDTEST THREAD####################
    def create_speedtest_page(self):
        page = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()

        #Ttile  
        title = QtWidgets.QLabel("WIFI Speed Test")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        title.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(title)


        #meter containers side by side
        meters_layout = QtWidgets.QHBoxLayout()
        meters_layout.setSpacing(50) #change space between meters


        #Left meter - Download
        download_container = QtWidgets.QVBoxLayout()
        
        self.download_gauge = SpeedometerGauge(max_value=1000, label="DOWNLOAD")
        self.download_gauge.setFixedSize(300, 300)
        
        download_container.addWidget(self.download_gauge, alignment=QtCore.Qt.AlignCenter)


        #Right meter - Upload
        upload_container = QtWidgets.QVBoxLayout()
        
        self.upload_gauge = SpeedometerGauge(max_value=500, label="UPLOAD")
        self.upload_gauge.setFixedSize(300, 300)
        
        upload_container.addWidget(self.upload_gauge, alignment=QtCore.Qt.AlignCenter)
        
        #ADD BOTH METERS TO MAIN LAYOUT
        meters_layout.addStretch() #Keep this in centre
        meters_layout.addLayout(download_container)
        meters_layout.addLayout(upload_container)
        meters_layout.addStretch()

        layout.addLayout(meters_layout)

        # Speed button
        self.speedtest_button = QtWidgets.QPushButton("Run Speed Test")
        self.speedtest_button.setFixedSize(200, 50)
        self.speedtest_button.clicked.connect(self.on_button_click)  # ADD THIS
        
        #New button layout
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.speedtest_button)
        button_layout.addStretch()
        layout.addLayout(button_layout)

        #Console widgets
        self.speedtest_console = QtWidgets.QTextEdit()
        self.speedtest_console.setReadOnly(True)
        self.speedtest_console.setMaximumHeight(100)
        self.speedtest_console.append("Click 'Run Speed Test' to begin...\n")
        layout.addWidget(self.speedtest_console)

        page.setLayout(layout)
        return page
    
    def show_results(self, download_result, upload_result, download_mbps, upload_mbps):
        #This method will be called when the speed test is completed
        self.speedtest_console.append(f"{download_result}\n")
        self.speedtest_console.append(f"{upload_result}\n")
        self.speedtest_console.append("Speed tests completed.\n")
        
        # Stop animation and show final results
        if hasattr(self, 'animate_timer'):
            self.animate_timer.stop()
        
        # Update gauges with final values
        self.download_gauge.setValue(download_mbps)
        self.upload_gauge.setValue(upload_mbps)
    
    def animate_download(self):
        # Pulsing animation while downloading
        current = self.download_gauge.value()
        self.download_gauge.setValue((current + 50) % 1000)
    
    def animate_upload(self):
        # Pulsing animation while uploading
        current = self.upload_gauge.value()
        self.upload_gauge.setValue((current + 30) % 500)

    def on_button_click(self):
        # Reset gauges
        self.download_gauge.setValue(0)
        self.upload_gauge.setValue(0)
        
        # Create and start the speed test thread
        self.speedtest_button.setEnabled(False)
        self.speedtest_button.setText("Running...")
        self.speedtest_console.clear()

        # Start thread
        self.thread = SpeedTestThread()
        self.thread.progressUpdate.connect(self.update_progress)
        self.thread.speedTestCompleted.connect(self.show_results)
        self.thread.testingDownload.connect(self.start_download_animation)
        self.thread.testingUpload.connect(self.start_upload_animation)
        self.thread.start()
        self.thread.finished.connect(self.on_test_finished)
    
    def start_download_animation(self):
        # Start animating download bar
        self.animate_timer = QtCore.QTimer()
        self.animate_timer.timeout.connect(self.animate_download)
        self.animate_timer.start(100)  # Update every 100ms
    
    def start_upload_animation(self):
        # Stop download animation, start upload
        if hasattr(self, 'animate_timer'):
            self.animate_timer.stop()
        self.animate_timer = QtCore.QTimer()
        self.animate_timer.timeout.connect(self.animate_upload)
        self.animate_timer.start(100)
    
    def update_progress(self, message):
        # This method will be called to update progress messages
        self.speedtest_console.append(message)

    def on_test_finished(self):
        self.speedtest_button.setEnabled(True)
        self.speedtest_button.setText("Run Speed Test")



#####################WEATHER THREAD#####################





    def create_weather_page(self):
        page = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()

        # Weather Input and button
        self.location_input = QtWidgets.QLineEdit()
        self.location_input.setPlaceholderText("Enter city name...")
        self.location_input.setFixedHeight(30)
        
        self.weather_button = QtWidgets.QPushButton("Get Weather")
        self.weather_button.setFixedSize(200, 50)
        self.weather_button.clicked.connect(self.on_weather_click)
        
        self.console = QtWidgets.QTextEdit()
        self.console.setReadOnly(True)
        self.console.append("Enter a city name and click 'Get Weather'\n")
        
        layout.addWidget(self.location_input)
        layout.addWidget(self.weather_button)
        layout.addWidget(self.console)
        
        page.setLayout(layout)
        return page

    def on_weather_click(self):
        location = self.location_input.text().strip()
        if not location:
            self.console.append(f"Please enter a city name.\n")
            return
            
        self.weather_button.setEnabled(False)
        self.weather_button.setText("Fetching...")
        self.console.append(f"Fetching weather for {location}...\n")

        #Create and start the weather thread

        self.weather_thread = WeatherThread(location)
        self.weather_thread.weathercompleted.connect(self.show_weather)
        self.weather_thread.start()
        self.weather_thread.finished.connect(self.on_weather_finished)


    def show_weather(self, weather_data):
        if "error" in weather_data:
            self.console.append(f"Error: {weather_data['error']}\n")
        else:
            self.console.append(f"Weather in {weather_data['location']}:\n")
            self.console.append(f"Temperature: {weather_data['temperature']} °C\n")
            self.console.append(f"Description: {weather_data['description']}\n")
            self.console.append(f"Humidity: {weather_data['humidity']}%\n")
            self.console.append(f"Wind Speed: {weather_data['wind_speed']} m/s\n")

    def on_weather_finished(self):
        self.weather_button.setEnabled(True)
        self.weather_button.setText("Get Weather")

###########DARK/LIHT MODE TOGGLE##############
    def toggle_theme(self):
        self.is_dark_mode = not self.is_dark_mode
        if self.is_dark_mode:
            self.setStyleSheet(self.dark_theme)
        else:
            self.setStyleSheet(self.light_theme)


################SETTINGS PAGE##############
    def create_settings_page(self):
        page = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()
        
        label = QtWidgets.QLabel("Settings")
        label.setStyleSheet("font-size: 20px; font-weight: bold;")
        
        # Theme toggle
        theme_label = QtWidgets.QLabel("Appearance:")
        theme_toggle = QtWidgets.QPushButton("Switch to Light Mode" if self.is_dark_mode else "Switch to Dark Mode")
        theme_toggle.clicked.connect(self.toggle_theme)
        
        layout.addWidget(label)
        layout.addWidget(theme_label)
        layout.addWidget(theme_toggle)
        layout.addStretch()
        
        page.setLayout(layout)
        return page


class WeatherThread(QtCore.QThread):
    weathercompleted = QtCore.pyqtSignal(dict) # Signal to emit weather data

    def __init__(self, location):
        super().__init__()
        self.location = location    

    def run(self):
        try:
            print(f"Fetching weather for {self.location}...")  # Debug
            weather_data = weather.get_current_weather(self.location)
            print(f"Weather data fetched: {weather_data}")  # Debug
            self.weathercompleted.emit(weather_data)
        except Exception as e:
            print(f"Error fetching weather data: {e}")  # See what's failing
            self.weathercompleted.emit({"error": str(e)})


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())