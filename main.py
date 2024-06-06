import sys
import random
import string
import locale_manager
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QSlider, QCheckBox, QPushButton, QLineEdit, QFrame, QComboBox)
from PyQt5.QtCore import Qt

class PasswordGenerator(QWidget):
    def __init__(self):
        super().__init__()

        # Initialize LocaleManager
        self.manager = locale_manager.LocaleManager(
            language_folder="locales",
            default_language="en_US",
            languages=["en_US", "hu_HU"],
            translations={
                "en_US": {
                    "window_title": "Password Generator",
                    "password_length": "Password length: {length}",
                    "uppercase": "Uppercase",
                    "lowercase": "Lowercase",
                    "digits": "Digits",
                    "special_characters": "Special Characters",
                    "generate_password": "Generate Password",
                    "copy": "Copy",
                    "choose_language": "Choose Language:"
                },
                "hu_HU": {
                    "window_title": "Jelszógenerátor",
                    "password_length": "Jelszó hossza: {length}",
                    "uppercase": "Nagybetűk",
                    "lowercase": "Kisbetűk",
                    "digits": "Számok",
                    "special_characters": "Speciális karakterek",
                    "generate_password": "Jelszó generálása",
                    "copy": "Másolás",
                    "choose_language": "Válassz nyelvet:"
                }
            }
        )

        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.manager.get_translation('window_title'))
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        # Language selection label and combo box
        self.language_label = QLabel(self.manager.get_translation('choose_language'))
        self.language_combo = QComboBox()
        self.language_combo.addItems(self.manager.get_available_languages())
        self.language_combo.currentIndexChanged.connect(self.change_language)

        layout.addWidget(self.language_label)
        layout.addWidget(self.language_combo)

        # Slider for password length
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(6)
        self.slider.setMaximum(255)
        self.slider.setValue(12)
        self.slider.setTickInterval(1)
        self.slider.setTickPosition(QSlider.TicksBelow)

        self.slider_label = QLabel(self.manager.get_translation('password_length', length=self.slider.value()))
        self.slider.valueChanged.connect(self.update_label)

        layout.addWidget(self.slider_label)
        layout.addWidget(self.slider)

        # Checkboxes for password components
        self.uppercase_cb = QCheckBox(self.manager.get_translation('uppercase'))
        self.lowercase_cb = QCheckBox(self.manager.get_translation('lowercase'))
        self.digits_cb = QCheckBox(self.manager.get_translation('digits'))
        self.special_cb = QCheckBox(self.manager.get_translation('special_characters'))

        self.uppercase_cb.setChecked(True)
        self.lowercase_cb.setChecked(True)
        self.digits_cb.setChecked(True)
        self.special_cb.setChecked(True)

        layout.addWidget(self.uppercase_cb)
        layout.addWidget(self.lowercase_cb)
        layout.addWidget(self.digits_cb)
        layout.addWidget(self.special_cb)

        # Generate button
        self.generate_btn = QPushButton(self.manager.get_translation('generate_password'))
        self.generate_btn.clicked.connect(self.generate_password)

        layout.addWidget(self.generate_btn)

        # Output field
        self.output = QLineEdit()
        self.output.setReadOnly(True)
        self.output.setFrame(QFrame.Box)
        self.output.setStyleSheet("QLineEdit { background-color: white; padding: 5px; }")

        self.copy_btn = QPushButton(self.manager.get_translation('copy'))
        self.copy_btn.clicked.connect(self.copy_to_clipboard)

        output_layout = QHBoxLayout()
        output_layout.addWidget(self.output)
        output_layout.addWidget(self.copy_btn)

        layout.addLayout(output_layout)

        self.setLayout(layout)

        # Apply styles
        self.setStyleSheet("""
            QWidget {
                font-family: Arial;
                font-size: 14px;
            }
            QSlider::groove:horizontal {
                height: 8px;
                background: #ddd;
                margin: 2px 0;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #5c6bc0;
                border: 1px solid #5c6bc0;
                width: 18px;
                height: 18px;
                margin: -7px 0;
                border-radius: 9px;
            }
            QPushButton {
                background-color: #5c6bc0;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #3f51b5;
            }
            QCheckBox {
                padding: 5px;
            }
            QLineEdit {
                border: 1px solid #ddd;
                border-radius: 5px;
            }
        """)

    def change_language(self):
        language_code = self.language_combo.currentText()
        self.manager.set_language(language_code)
        self.update_translations()

    def update_label(self, value):
        self.slider_label.setText(self.manager.get_translation('password_length', length=value))

    def update_translations(self):
        self.setWindowTitle(self.manager.get_translation('window_title'))
        self.language_label.setText(self.manager.get_translation('choose_language'))
        self.slider_label.setText(self.manager.get_translation('password_length', length=self.slider.value()))
        self.uppercase_cb.setText(self.manager.get_translation('uppercase'))
        self.lowercase_cb.setText(self.manager.get_translation('lowercase'))
        self.digits_cb.setText(self.manager.get_translation('digits'))
        self.special_cb.setText(self.manager.get_translation('special_characters'))
        self.generate_btn.setText(self.manager.get_translation('generate_password'))
        self.copy_btn.setText(self.manager.get_translation('copy'))

    def generate_password(self):
        length = self.slider.value()
        characters = ''
        if self.uppercase_cb.isChecked():
            characters += string.ascii_uppercase
        if self.lowercase_cb.isChecked():
            characters += string.ascii_lowercase
        if self.digits_cb.isChecked():
            characters += string.digits
        if self.special_cb.isChecked():
            characters += string.punctuation

        if characters:
            password = ''.join(random.choice(characters) for _ in range(length))
            self.output.setText(password)

    def copy_to_clipboard(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.output.text())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PasswordGenerator()
    window.show()
    sys.exit(app.exec_())
