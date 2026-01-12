from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QInputDialog, QWidget
import pyqtgraph as pg
from PySide6.QtCore import QTimer

class MainWindow(QMainWindow):

    def __init__(self, backend):
        super().__init__()
        self.backend = backend

        self.setWindowTitle("Oscilloscope")
        self.graphWidget = pg.PlotWidget()

        # Config initial plot
        self.graphWidget.showGrid(x=True, y=True, alpha=0.3)
        self.graphWidget.setLabel('bottom', 'Time', units='S')

        self.showing_voltage = True

        # Data
        self.running = False
        self.ms_list = []
        self.volts_list = []
        self.amps_list = []
        self.points_stored = 1000 # Stores last x number of points
        self.update_interval = 10 # Update every 10 ms default (100 times/sec)

        # Timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(10) # Refresh page every 50 ms

        # Buttons
        self.start_button = QPushButton("Start/Stop")
        self.start_button.clicked.connect(self.toggle_run)

        self.toggle_button = QPushButton("Show Current")
        self.toggle_button.clicked.connect(self.toggle_plot)

        self.rate_button = QPushButton("Update Sampling Rate")
        self.rate_button.clicked.connect(self.set_update_interval)

        self.record_button = QPushButton("Update Record Length")
        self.record_button.clicked.connect(self.set_record_length)

        # Window Layout
        central = QWidget()
        layout = QVBoxLayout(central)
        layout.addWidget(self.graphWidget)
        layout.addWidget(self.start_button)
        layout.addWidget(self.toggle_button)
        layout.addWidget(self.rate_button)
        layout.addWidget(self.record_button)
        self.setCentralWidget(central)

        self.voltage_curve = self.graphWidget.plot([], [], pen='y', name="Voltage")
        self.amps_curve = self.graphWidget.plot([], [], pen='c', name="Current")

        self.show_voltage()

    # Update graph

    def update_plot(self):
        samples = self.backend.read_data()
        if not samples:
            return
        for timestamp, voltage, current in samples:
            self.ms_list.append(timestamp/1000)
            self.volts_list.append(voltage)
            self.amps_list.append(current)

        # Keep only last N points
        if len(self.ms_list) > self.points_stored:
            self.ms_list = self.ms_list[-self.points_stored:]
            self.volts_list = self.volts_list[-self.points_stored:]
            self.amps_list = self.amps_list[-self.points_stored:]

        if self.showing_voltage:
            self.voltage_curve.setData(self.ms_list, self.volts_list)
        else:
            self.amps_curve.setData(self.ms_list, self.amps_list)

    def clear_plot_data(self):
        self.ms_list.clear()
        self.volts_list.clear()
        self.amps_list.clear()

        self.voltage_curve.clear()
        self.amps_curve.clear()

    # Button Functionalities

    def toggle_run(self):
        if self.running:
            self.running = False
            self.start_button.setText("Start")
            self.backend.stop_sampling()
            self.clear_plot_data()
        else:
            self.running = True
            self.start_button.setText("Stop")
            self.clear_plot_data()
            self.backend.start_sampling()


    def set_update_interval(self):
        self.update_interval, ok = QInputDialog.getInt(self, "Update Interval", "Update interval (ms):", self.update_interval, 5, 1000000, 1) # Arduino cannot reliably output quicker than 5 ms tick

        if ok:
            self.backend.set_update_interval(self.update_interval)

    def set_record_length(self):
        self.points_stored, ok = QInputDialog.getInt(self, "Record Length", "Points stored:", self.points_stored, 1, 1000000, 1)

    def toggle_plot(self):
        self.clear_plot_data()
        self.showing_voltage = not self.showing_voltage

        if self.showing_voltage:
            self.show_voltage()
        else:
            self.show_amps()

    def show_voltage(self):
        self.amps_curve.hide()
        self.voltage_curve.show()
        self.graphWidget.setTitle("Voltage vs Time")
        self.graphWidget.setLabel('left', 'Voltage', units='V')
        self.toggle_button.setText("Show Current")

    def show_amps(self):
        self.voltage_curve.hide()
        self.amps_curve.show()
        self.graphWidget.setTitle("Current vs Time")
        self.graphWidget.setLabel('left', 'Current', units='A')
        self.toggle_button.setText("Show Voltage")