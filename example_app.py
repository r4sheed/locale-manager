import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QComboBox, QHBoxLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import locale_manager

class LocalizationApp(QWidget):
    def __init__(self):
        super().__init__()

        self.manager = locale_manager.LocaleManager(
            languages=["en_US", "hu_HU"],
            translations={
                "en_US": {
                    "welcome": "Welcome",
                    "goodbye": "Goodbye",
                    "greeting": "{welcome} {name}!",
                    "choose_language": "Choose Language:",
                    "choose_color": "Choose a color:",
                    "title": "Localization App",
                    "description": "This is a simple app to demonstrate localization.",
                    "color_selected": "You have selected {color}!",
                    "color_red": "Red",
                    "color_green": "Green",
                    "color_blue": "Blue"
                },
                "hu_HU": {
                    "welcome": "Szia",
                    "goodbye": "Viszlát",
                    "greeting": "{welcome} {name}!",
                    "choose_language": "Válassz nyelvet:",
                    "choose_color": "Válassz egy színt:",
                    "title": "Lokalizációs Alkalmazás",
                    "description": "Ez egy egyszerű alkalmazás a lokalizáció bemutatására.",
                    "color_selected": "A kiválasztott szín: {color}!",
                    "color_red": "Piros",
                    "color_green": "Zöld",
                    "color_blue": "Kék"
                },
            }
        )
        
        self.initUI()
        
    def initUI(self):
        self.layout = QVBoxLayout()

        # Title label
        self.title_label = QLabel(f"<h1 style='text-align:center;'>{self.manager.get_translation('title')}</h1>")
        self.layout.addWidget(self.title_label)

        # Description label
        self.description_label = QLabel(f"<p style='text-align:center;'>{self.manager.get_translation('description')}</p>")
        self.layout.addWidget(self.description_label)

        # Language selection
        self.language_label = QLabel(f"<h2 style='text-align:center;'>{self.manager.get_translation('choose_language')}</h2>")
        self.layout.addWidget(self.language_label)
        
        self.language_combo = QComboBox()
        self.language_combo.addItems(self.manager.get_available_languages())
        self.language_combo.currentIndexChanged.connect(self.change_language)
        self.layout.addWidget(self.language_combo)

        # Welcome label
        self.welcome_label = QLabel(f"<h3 style='text-align:center;'>{self.manager.get_translation('welcome')}</h3>")
        self.layout.addWidget(self.welcome_label)

        # Color selection
        self.color_label = QLabel(f"<h2 style='text-align:center;'>{self.manager.get_translation('choose_color')}</h2>")
        self.layout.addWidget(self.color_label)
        
        self.color_combo = QComboBox()
        self.colors = ['color_red', 'color_green', 'color_blue']
        self.color_combo.addItems([self.manager.get_translation(color) for color in self.colors])
        self.color_combo.currentIndexChanged.connect(self.change_color)
        self.layout.addWidget(self.color_combo)

        # Selected color label
        self.selected_color_label = QLabel(f"<h3 style='text-align:center;'></h3>")
        self.layout.addWidget(self.selected_color_label)

        self.setLayout(self.layout)
        self.setWindowTitle(self.manager.get_translation("title"))
        self.setGeometry(100, 100, 400, 300)
        self.show()
    
    def change_language(self):
        language_code = self.language_combo.currentText()
        self.manager.set_language(language_code)
        self.update_translations()
        
    def change_color(self):
        color_key = self.colors[self.color_combo.currentIndex()]
        color_translation = self.manager.get_translation(color_key)
        translation = self.manager.get_translation("color_selected", color=color_translation)
        self.selected_color_label.setText(f"<h3 style='text-align:center;'>{translation}</h3>")

    def update_translations(self):
        self.title_label.setText(f"<h1 style='text-align:center;'>{self.manager.get_translation('title')}</h1>")
        self.description_label.setText(f"<p style='text-align:center;'>{self.manager.get_translation('description')}</p>")
        self.language_label.setText(f"<h2 style='text-align:center;'>{self.manager.get_translation('choose_language')}</h2>")
        self.welcome_label.setText(f"<h3 style='text-align:center;'>{self.manager.get_translation('welcome')}</h3>")
        self.color_label.setText(f"<h2 style='text-align:center;'>{self.manager.get_translation('choose_color')}</h2>")
        self.color_combo.clear()
        self.color_combo.addItems([self.manager.get_translation(color) for color in self.colors])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = LocalizationApp()
    sys.exit(app.exec_())
