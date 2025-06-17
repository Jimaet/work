import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QGridLayout
from PyQt5.QtGui import QFont


class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Калькулятор")
        self.setFixedSize(300, 400)
        self.init_ui()

    def init_ui(self):
        # Главное поле ввода
        self.input_field = QLineEdit()
        self.input_field.setFont(QFont("Arial", 24))
        self.input_field.setReadOnly(True)
        self.input_field.setStyleSheet("background-color: white; color: black; padding: 10px;")

        # Разметка
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.input_field)

        # Кнопки
        buttons = {
            '7': (0, 0), '8': (0, 1), '9': (0, 2), '/': (0, 3),
            '4': (1, 0), '5': (1, 1), '6': (1, 2), '*': (1, 3),
            '1': (2, 0), '2': (2, 1), '3': (2, 2), '-': (2, 3),
            '0': (3, 0), 'C': (3, 1), '=': (3, 2), '+': (3, 3)
        }

        grid_layout = QGridLayout()
        for btn_text, pos in buttons.items():
            button = QPushButton(btn_text)
            button.setFont(QFont("Arial", 18))
            button.setFixedSize(60, 60)
            button.clicked.connect(self.on_button_clicked)
            grid_layout.addWidget(button, pos[0], pos[1])

        main_layout.addLayout(grid_layout)
        self.setLayout(main_layout)

    def on_button_clicked(self):
        button = self.sender()
        text = button.text()

        if text == "C":
            self.input_field.setText("")
        elif text == "=":
            try:
                result = str(eval(self.input_field.text()))
                self.input_field.setText(result)
            except Exception:
                self.input_field.setText("Ошибка")
        else:
            self.input_field.setText(self.input_field.text() + text)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    calc = Calculator()
    calc.show()
    sys.exit(app.exec_())
