
import PyQt5
import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtCore as QtCore
import speedtest_logger  # Assuming speedtest-logger.py is in the same directory
import weather

class SpeedTestThread(QtCore.QThread):


################DEBUG SECTION####################
    speedTestCompleted = QtCore.pyqtSignal(str, str)
    progressUpdate = QtCore.pyqtSignal(str) # Signal to emit progress updates

    def run(self):
        print("Thread run() started!")  # Debug
        try:
            print("Emitting first progress...")  # Debug
            self.progressUpdate.emit("Starting WIFI speed test...")

            print("Calling download...")  # Debug
            self.progressUpdate.emit("Running download test...")
            download_result = speedtest_logger.download()
            print(f"Download done: {download_result}")  # Debug

            print("Calling upload...")  # Debug
            self.progressUpdate.emit("Running upload test...")
            upload_result = speedtest_logger.upload()
            print(f"Upload done: {upload_result}")  # Debug

            self.progressUpdate.emit("WIFI speed test completed.")
            self.speedTestCompleted.emit(download_result, upload_result)
            print("Signals emitted!")  # Debug
        except Exception as e:
            print(f"Exception in thread: {e}")  # Debug
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

        # Speed button
        self.speedtest_button = QtWidgets.QPushButton("Run Speed Test")
        self.speedtest_button.setFixedSize(200, 50)
        self.speedtest_button.clicked.connect(self.on_button_click)  # ADD THIS
        
        self.speedtest_console = QtWidgets.QTextEdit()
        self.speedtest_console.setReadOnly(True)
        self.speedtest_console.append("Welcome! Click 'Run Speed Test' to start.\n")

        layout.addWidget(self.speedtest_button)
        layout.addWidget(self.speedtest_console)
        page.setLayout(layout)
        return page
    
    def show_results(self, download_result, upload_result):
        #This method will be called when the speed test is completed
        self.speedtest_console.append(f"{download_result}\n")
        self.speedtest_console.append(f"{upload_result}\n")
        self.speedtest_console.append("Speed tests completed.\n")

    
    def on_button_click(self):
        # Create and start the speed test thread
        self.speedtest_button.setEnabled(False)
        self.speedtest_button.setText("Running...")
        self.speedtest_console.clear()


            # Start thread
        self.thread = SpeedTestThread()
        self.thread.progressUpdate.connect(self.update_progress)  # ADD THIS
        self.thread.speedTestCompleted.connect(self.show_results)
        self.thread.start()
        self.thread.finished.connect(self.on_test_finished)
    
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