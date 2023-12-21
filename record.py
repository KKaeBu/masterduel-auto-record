import sys
import psutil as ps
import pygetwindow as gw

from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTimer

md_ps = () #(masterduel.exe, pid)

for p in ps.process_iter():
    if p.name() == "masterduel.exe":
        md_ps = ('masterduel', p.pid)

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("마듀 자동 전적 기록기")
        self.setWindowIcon(QIcon('./icon/light.png'))
        self.setGeometry(100, 100, 400, 300)
        self.label = QLabel("현재 창 크기: 400 x 300", self)
        layout = QVBoxLayout()
        layout.addWidget(self.label)

        self.setLayout(layout)

        # 타이머를 사용하여 주기적으로 창 크기 업데이트
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_window_size)
        self.timer.start(500)  # 500ms마다 업데이트
        self.show()

    def update_window_size(self):
        try:
            # 특정 프로그램의 이름을 지정
            program_name = md_ps[0]
            window = gw.getWindowsWithTitle(program_name)[0]
            size = window.size
            position = window.topleft

            # 다른 프로그램의 창 크기를 가져와서 GUI 창 크기 업데이트
            self.setGeometry(position.x, position.y, size.width, size.height)
            self.label.setText(f"현재 창 크기: {size.width} x {size.height}")
        except IndexError:
            pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
