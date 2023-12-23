import sys
import os
import psutil as ps
import pygetwindow as gw

import pygetwindow as gw
import pyautogui
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import QTimer

#마듀 프로세스 이름 및 pid 저장
md_ps = () #(masterduel.exe, pid)

#마듀 프로세스 찾기
for p in ps.process_iter():
    if p.name() == "masterduel.exe":
        md_ps = ('masterduel', p.pid)

#GUI 클래스
class GameMonitor(QWidget):
    def __init__(self):
        '''
        gui 초기화 함수
        '''
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
        '''
        모니터링 시작 함
        '''
        self.game_window = gw.getWindowsWithTitle(md_ps[0])[0]
        self.monitoring_timer.start(1000)  # Check every second
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.status_label.setText("Monitoring...")

    
    def stop_monitoring(self):
        '''
        모니터링 중지 함수
        '''
        self.monitoring_timer.stop()
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.status_label.setText("Monitoring stopped.")

    def check_game_status(self):
        '''
        해당 게임 창이 활성화 상태인지 아닌지를 판별하는 함수
        (해당 화면에 마우스가 focus되어있는지를 판단)
        '''
        if self.game_window.isActive:
            #마듀 창 화면 좌표 및 크기를 가져옴
            x, y, width, height = self.game_window.left, self.game_window.top, self.game_window.width, self.game_window.height
            
            #마듀 게임 창 화면 캡쳐
            screenshot = pyautogui.screenshot(region=(x, y, width, height))

            #여기서 이미지 화면별로 나눠주고 이를 ai돌리는게 필요
            screenshot.save("game_screenshot.png")

            self.status_label.setText("Game is active.")
        else:
            self.status_label.setText("Game is not active.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    monitor = GameMonitor()
    monitor.show()
    sys.exit(app.exec_())
