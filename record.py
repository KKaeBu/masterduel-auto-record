import sys
import psutil as ps
import pygetwindow as gw

import pygetwindow as gw
import pyautogui
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import QTimer

md_ps = () #(masterduel.exe, pid)

for p in ps.process_iter():
    if p.name() == "masterduel.exe":
        md_ps = ('masterduel', p.pid)

class GameMonitor(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("마듀 자동 전적 기록기")
        self.setGeometry(100, 100, 400, 200)

        self.layout = QVBoxLayout()

        self.start_button = QPushButton("Start Monitoring", self)
        self.start_button.clicked.connect(self.start_monitoring)
        self.layout.addWidget(self.start_button)

        self.stop_button = QPushButton("Stop Monitoring", self)
        self.stop_button.clicked.connect(self.stop_monitoring)
        self.stop_button.setEnabled(False)
        self.layout.addWidget(self.stop_button)

        self.status_label = QLabel("", self)
        self.layout.addWidget(self.status_label)

        self.setLayout(self.layout)

        self.game_window = None
        self.monitoring_timer = QTimer(self)
        self.monitoring_timer.timeout.connect(self.check_game_status)

    def start_monitoring(self):
        self.game_window = gw.getWindowsWithTitle(md_ps[0])[0]
        self.monitoring_timer.start(1000)  # Check every second
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.status_label.setText("Monitoring...")

    def stop_monitoring(self):
        self.monitoring_timer.stop()
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.status_label.setText("Monitoring stopped.")

    def check_game_status(self):
        if self.game_window.isActive:
            # Get the position and size of the game window
            x, y, width, height = self.game_window.left, self.game_window.top, self.game_window.width, self.game_window.height

            # Capture only the game window area
            screenshot = pyautogui.screenshot(region=(x, y, width, height))
            screenshot.save("game_screenshot.png")

            self.status_label.setText("Game is active.")
        else:
            self.status_label.setText("Game is not active.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    monitor = GameMonitor()
    monitor.show()
    sys.exit(app.exec_())
