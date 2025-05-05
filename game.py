from PyQt6.QtWidgets import QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

class CookieClicker(QMainWindow):
    switch_to_chat = pyqtSignal()

    def __init__(self, main_window=None):
        super().__init__()
        self.main_window = main_window
        self.score = 0
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle('Cookie Clicker')
        self.setMinimumSize(600, 400)
        self.setStyleSheet("background-color: #0D0D0D;")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()

        self.score_label = QLabel('Cookies: 0')
        self.score_label.setStyleSheet("color: #C084FC; font-size: 24px;")
        self.score_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.cookie_btn = QPushButton()
        self.cookie_btn.setStyleSheet(
            """
            QPushButton {
                background-color: transparent;
                border: none;
                qproperty-icon: url('cookie.png');
                icon-size: 200px;
            }
            QPushButton:hover {
                qproperty-icon: url('cookie_hover.png');
            }
            """
        )
        self.cookie_btn.clicked.connect(self.increment_score)

        layout.addWidget(self.score_label)
        layout.addWidget(self.cookie_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        central_widget.setLayout(layout)

    def increment_score(self):
        self.score += 1
        self.score_label.setText(f'Cookies: {self.score}')

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_1 and (event.modifiers() & Qt.KeyboardModifier.ControlModifier):
            self.hide()
            if self.main_window:
                self.main_window.show()
        super().keyPressEvent(event)