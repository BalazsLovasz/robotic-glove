import sys

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QStackedWidget,
)

from ui.home_page import HomePage
from ui.live_grip_page import LiveGripPage


class Dashboard(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Assistive Grip")
        self.resize(1200, 700)

        # Global appearance
        self.setStyleSheet("""
            QWidget {
                background-color: #0d0d0f;
                color: white;
                font-family: Arial;
            }
        """)

        # ---------------- PAGES ----------------

        self.pages = QStackedWidget()

        self.home_page = HomePage()
        self.live_page = LiveGripPage()

        self.pages.addWidget(self.home_page)
        self.pages.addWidget(self.live_page)

        # ---------------- NAVIGATION ----------------

        self.home_page.live_button.clicked.connect(
            lambda: self.pages.setCurrentIndex(1)
        )

        self.live_page.back_button.clicked.connect(
            lambda: self.pages.setCurrentIndex(0)
        )

        # ---------------- MAIN LAYOUT ----------------

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)

        main_layout.addWidget(self.pages)

        self.setLayout(main_layout)


app = QApplication(sys.argv)

window = Dashboard()
window.show()

sys.exit(app.exec())