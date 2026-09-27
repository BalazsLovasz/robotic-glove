import sys

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QStackedWidget,
    QFrame,
)

from ui.home_page import HomePage
from ui.live_grip_page import LiveGripPage


class Dashboard(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Assistive Grip")
        self.resize(1200, 700)

        self.setStyleSheet("""
            QWidget {
                background-color: #08080a;
                color: white;
                font-family: Arial;
            }
        """)

        # ---------------- PAGES ----------------

        self.pages = QStackedWidget()

        self.home_page = HomePage()
        self.live_page = LiveGripPage()

        # Temporary pages
        self.analytics_page = QWidget()
        self.device_page = QWidget()
        self.settings_page = QWidget()

        self.pages.addWidget(self.home_page)
        self.pages.addWidget(self.live_page)
        self.pages.addWidget(self.analytics_page)
        self.pages.addWidget(self.device_page)
        self.pages.addWidget(self.settings_page)

        # ---------------- NAVIGATION ----------------

        navigation = QHBoxLayout()
        navigation.setContentsMargins(70, 12, 70, 18)
        navigation.setSpacing(20)

        self.home_button = QPushButton("⌂\nHome")
        self.live_button = QPushButton("◉\nLive Grip")
        self.analytics_button = QPushButton("▥\nAnalytics")
        self.device_button = QPushButton("▯\nDevice")
        self.settings_button = QPushButton("⚙\nSettings")

        self.nav_buttons = [
            self.home_button,
            self.live_button,
            self.analytics_button,
            self.device_button,
            self.settings_button,
        ]

        for button in self.nav_buttons:
            button.setFixedSize(150, 70)

        navigation.addStretch()

        for button in self.nav_buttons:
            navigation.addWidget(button)
            navigation.addSpacing(15)

        navigation.addStretch()

        # ---------------- BUTTON CONNECTIONS ----------------

        self.home_button.clicked.connect(
            lambda: self.change_page(0)
        )

        self.live_button.clicked.connect(
            lambda: self.change_page(1)
        )

        self.analytics_button.clicked.connect(
            lambda: self.change_page(2)
        )

        self.device_button.clicked.connect(
            lambda: self.change_page(3)
        )

        self.settings_button.clicked.connect(
            lambda: self.change_page(4)
        )

        # ---------------- DIVIDER ----------------

        divider = QFrame()
        divider.setFixedHeight(1)

        divider.setStyleSheet("""
            background-color: #242426;
        """)

        # ---------------- MAIN LAYOUT ----------------

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        main_layout.addWidget(self.pages, 1)
        main_layout.addWidget(divider)
        main_layout.addLayout(navigation)

        self.setLayout(main_layout)

        # Start on Home
        self.change_page(0)


    def change_page(self, page_number):

        self.pages.setCurrentIndex(page_number)

        # Reset all navigation buttons
        for button in self.nav_buttons:

            button.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    border: none;
                    border-radius: 16px;
                    color: #8e8e93;
                    font-size: 18px;
                }

                QPushButton:hover {
                    background-color: #1c1c1e;
                    color: white;
                }
            """)

        # Highlight current page
        active_button = self.nav_buttons[page_number]

        active_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                border-radius: 16px;
                color: #5ac8fa;
                font-size: 18px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #1c1c1e;
            }
        """)


app = QApplication(sys.argv)

window = Dashboard()
window.show()

sys.exit(app.exec())