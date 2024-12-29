import sys
import wmi
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QMessageBox
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt
import pyperclip

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Número de Série da Placa-Mãe")
        self.setGeometry(100, 100, 450, 250)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        self.instruction_label = QLabel("Número de Série da Placa-Mãe")
        self.instruction_label.setFont(QFont("Arial", 16, QFont.Bold))
        self.instruction_label.setAlignment(Qt.AlignCenter)
        self.instruction_label.setStyleSheet("color: #2c3e50;")
        layout.addWidget(self.instruction_label)

        self.serial_number = self.get_serial_number_with_wmi()
        self.serial_label = QLabel(self.serial_number)
        self.serial_label.setFont(QFont("Arial", 14, QFont.Bold))
        self.serial_label.setAlignment(Qt.AlignCenter)
        self.serial_label.setStyleSheet("color: #2980b9; background-color: #ecf0f1; padding: 10px; border-radius: 10px;")
        layout.addWidget(self.serial_label)

        self.copy_button = QPushButton("Copiar Número de Série")
        self.copy_button.setFont(QFont("Arial", 12, QFont.Bold))
        self.copy_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #1f618d;
            }
        """)
        self.copy_button.clicked.connect(self.copy_to_clipboard)
        layout.addWidget(self.copy_button)

        self.setLayout(layout)

    def get_serial_number_with_wmi(self):
        try:
            c = wmi.WMI()
            for board in c.Win32_BaseBoard():
                return board.SerialNumber
        except Exception as e:
            return f"Erro ao obter o número de série: {e}"

    def copy_to_clipboard(self):
        pyperclip.copy(self.serial_number)
        QMessageBox.information(self, "Copiado", "O número de série foi copiado para a área de transferência.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setStyleSheet("""
        QWidget {
            background-color: #f7f9fb;
        }
    """)
    window.show()
    sys.exit(app.exec_())
