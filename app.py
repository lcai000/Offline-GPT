import sys
import threading
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QLineEdit, QPushButton, QCheckBox
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt, QTimer
from backend import Interact
from game import CookieClicker


class App(QMainWindow):
    def __init__(self):
        super().__init__()

        self.backend = Interact()
        self.verbose = False

        self.game_window = CookieClicker(main_window=self)
        self.game_window.hide()

        self.setWindowTitle("game")
        self.setMinimumSize(800, 600)
        self.setStyleSheet("background-color: #0D0D0D;")

        self.chat_area = QTextEdit(self)
        self.chat_area.setGeometry(20, 20, 760, 460)
        self.chat_area.setReadOnly(True)
        self.chat_area.setStyleSheet("""
            background-color: #1A1A1A;
            color: #C084FC;
            font-family: 'Segoe UI', sans-serif;
            font-size: 13pt;
            border: none;
            padding: 10px;
            border-radius: 12px;
        """)

        # Input Field
        self.input_field = QLineEdit(self)
        self.input_field.setGeometry(20, 500, 700, 50)
        self.input_field.setPlaceholderText("Type something...")
        self.input_field.setStyleSheet("""
            background-color: #262626;
            color: #C084FC;
            font-size: 12pt;
            border: 1px solid #C084FC;
            border-radius: 25px;
            padding-left: 15px;
        """)
        self.input_field.returnPressed.connect(self.send_message)

        # Send Button (Up Arrow)
        self.button = QPushButton("↑", self)
        self.button.setGeometry(730, 500, 50, 50)
        self.button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.button.setStyleSheet("""
            QPushButton {
                background-color: #C084FC;
                color: black;
                font-size: 18pt;
                font-weight: bold;
                border: none;
                border-radius: 25px;
            }
            QPushButton:hover {
                background-color: #E9D5FF;
            }
        """)
        self.button.clicked.connect(self.send_message)

        # Verbose Toggle Button
        self.verbose_toggle = QCheckBox("Verbose", self)
        self.verbose_toggle.setGeometry(20, 560, 150, 30)
        self.verbose_toggle.setStyleSheet("""
            QCheckBox {
                color: #C084FC;
                font-size: 11pt;
                padding-left: 5px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
            }
        """)
        self.verbose_toggle.stateChanged.connect(self.toggle_verbosity)

        # Typing Indicator
        self.typing_text = "Typing"
        self.typing_indicator = ""
        self.typing_label = QTextEdit(self)
        self.typing_label.setGeometry(180, 560, 600, 30)
        self.typing_label.setStyleSheet("""
            background-color: transparent;
            color: #C084FC;
            font-size: 11pt;
            border: none;
        """)
        self.typing_label.setReadOnly(True)
        self.typing_label.hide()

        self.dot_count = 0
        self.dot_timer = QTimer()
        self.dot_timer.timeout.connect(self.update_typing_indicator)

        self.show()

    def toggle_verbosity(self):
        self.verbose = self.verbose_toggle.isChecked()

    def send_message(self):
        user_input = self.input_field.text().strip()
        if not user_input:
            return

        user_box = f"""
        <div style='border: 1px solid #C084FC; border-radius: 10px; padding: 8px; margin: 8px 0; color:#C084FC;'>
            <b>You:</b> {user_input}
        </div>
        """
        self.chat_area.append(user_box)
        self.input_field.clear()

        self.typing_label.show()
        self.dot_count = 0
        self.typing_label.setText("Typing")
        self.dot_timer.start(500)

        thread = threading.Thread(target=self.get_response, args=(user_input,))
        thread.start()

    def update_typing_indicator(self):
        self.dot_count = (self.dot_count + 1) % 4
        self.typing_label.setText(self.typing_text + "." * self.dot_count)

    def get_response(self, user_input):
        response = self.backend.call(user_input, verbose=self.verbose)

        self.dot_timer.stop()
        self.typing_label.hide()

        bot_response = f"""
        <div style='margin: 8px 0; color: #C084FC;'>
            <b>local:</b> {response.replace(chr(10), "<br>")}
        </div>
        """
        self.chat_area.append(bot_response)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_1 and (event.modifiers() & Qt.KeyboardModifier.ControlModifier):
            self.hide()
            self.game_window.show()
        super().keyPressEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = App()
    sys.exit(app.exec())
