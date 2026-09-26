from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
)

from PySide6.QtCore import Qt


class HomePage(QWidget):

    def __init__(self):
        super().__init__()

        self.build_ui()


    def build_ui(self):

        layout = QVBoxLayout()

        layout.setContentsMargins(55, 35, 55, 35)

        # ---------------- HEADER ----------------

       

        # ---------------- CENTRE ----------------

        layout.addStretch()

        product_title = QLabel("Assistive Glove")
        product_title.setAlignment(Qt.AlignCenter)

        product_title.setStyleSheet("""
            font-size: 32px;
            font-weight: bold;
        """)

        layout.addWidget(product_title)

        layout.addSpacing(25)

        # Temporary glove visual
        glove = QLabel("GLOVE\nVISUAL")
        glove.setAlignment(Qt.AlignCenter)
        glove.setFixedSize(300, 230)

        glove.setStyleSheet("""
            background-color: #161618;
            border: 1px solid #29292d;
            border-radius: 28px;
            color: #55555c;
            font-size: 15px;
        """)

        glove_row = QHBoxLayout()

        glove_row.addStretch()
        glove_row.addWidget(glove)
        glove_row.addStretch()

        layout.addLayout(glove_row)

        layout.addSpacing(25)

        ready = QLabel("Ready")
        ready.setAlignment(Qt.AlignCenter)

        ready.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
        """)

        assistance = QLabel("Grip assistance active")
        assistance.setAlignment(Qt.AlignCenter)

        assistance.setStyleSheet("""
            color: #8e8e93;
            font-size: 14px;
        """)

        layout.addWidget(ready)
        layout.addWidget(assistance)

        layout.addStretch()

        # ---------------- NAVIGATION ----------------

        navigation = QHBoxLayout()

        self.live_button = QPushButton("◉\nLive Grip")
        self.analytics_button = QPushButton("⌁\nAnalytics")
        self.device_button = QPushButton("◇\nDevice")
        self.settings_button = QPushButton("⚙\nSettings")

        buttons = [
            self.live_button,
            self.analytics_button,
            self.device_button,
            self.settings_button,
        ]

        for button in buttons:

            button.setFixedSize(150, 70)

            button.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    border: none;
                    border-radius: 16px;
                    font-size: 15px;
                    color: #a8a8ad;
                }

                QPushButton:hover {
                    background-color: #1c1c1e;
                    color: white;
                }

                QPushButton:pressed {
                    background-color: #2c2c2e;
                }
            """)

        navigation.addStretch()

        navigation.addWidget(self.live_button)
        navigation.addSpacing(25)

        navigation.addWidget(self.analytics_button)
        navigation.addSpacing(25)

        navigation.addWidget(self.device_button)
        navigation.addSpacing(25)

        navigation.addWidget(self.settings_button)

        navigation.addStretch()

        layout.addLayout(navigation)

        self.setLayout(layout)