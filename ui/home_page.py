from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QSlider,
)

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap


class HomePage(QWidget):

    def __init__(self):
        super().__init__()
        self.build_ui()


    def build_ui(self):

        layout = QVBoxLayout()
        layout.setContentsMargins(55, 30, 55, 30)

        # ---------------- TITLE ----------------

        product_title = QLabel("Assistive Glove")
        product_title.setAlignment(Qt.AlignCenter)

        product_title.setStyleSheet("""
            font-size: 34px;
            font-weight: bold;
        """)

        layout.addWidget(product_title)
        layout.addSpacing(10)

        # ---------------- GLOVE VISUAL ----------------

        glove = QLabel()
        glove.setAlignment(Qt.AlignCenter)
        glove.setFixedSize(540, 350)

        # Soft background light behind glove
        glove.setStyleSheet("""
            QLabel {
                background: qradialgradient(
                    cx: 0.5, cy: 0.5,
                    radius: 0.5,
                    fx: 0.5, fy: 0.5,
                    stop: 0 rgba(100, 120, 135, 100),
                    stop: 0.45 rgba(60, 70, 80, 55),
                    stop: 1 rgba(13, 13, 15, 0)
                );
            }
        """)

        glove_image = QPixmap("assets/glove.png")

        glove_image = glove_image.scaled(
            500,
            330,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )

        glove.setPixmap(glove_image)

        glove_row = QHBoxLayout()
        glove_row.addStretch()
        glove_row.addWidget(glove)
        glove_row.addStretch()

        layout.addLayout(glove_row)

        # ---------------- ASSISTANCE LEVEL ----------------

        assistance_title = QLabel("ASSISTANCE LEVEL")
        assistance_title.setAlignment(Qt.AlignCenter)

        assistance_title.setStyleSheet("""
            color: #8e8e93;
            font-size: 13px;
            font-weight: bold;
            letter-spacing: 2px;
        """)

        self.assistance_value = QLabel("60%")
        self.assistance_value.setAlignment(Qt.AlignCenter)

        layout.addWidget(assistance_title)
        layout.addSpacing(3)
        layout.addWidget(self.assistance_value)
        layout.addSpacing(5)

        # ---------------- ASSISTANCE CONTROLS ----------------

        assistance_row = QHBoxLayout()
        assistance_row.addStretch()

        self.minus_button = QPushButton("−")
        self.plus_button = QPushButton("+")

        self.minus_button.setFixedSize(56, 56)
        self.plus_button.setFixedSize(56, 56)

        adjustment_button_style = """
            QPushButton {
                background-color: #19191c;
                border: 1px solid #323237;
                border-radius: 28px;
                color: white;
                font-size: 25px;
            }

            QPushButton:hover {
                background-color: #242428;
                border: 1px solid #44444a;
            }

            QPushButton:pressed {
                background-color: #303034;
            }
        """

        self.minus_button.setStyleSheet(adjustment_button_style)
        self.plus_button.setStyleSheet(adjustment_button_style)

        self.assistance_slider = QSlider(Qt.Horizontal)

        self.assistance_slider.setMinimum(0)
        self.assistance_slider.setMaximum(100)

        self.assistance_slider.setSingleStep(5)
        self.assistance_slider.setPageStep(5)

        self.assistance_slider.setFixedWidth(340)

        assistance_row.addWidget(self.minus_button)
        assistance_row.addSpacing(25)

        assistance_row.addWidget(self.assistance_slider)
        assistance_row.addSpacing(25)

        assistance_row.addWidget(self.plus_button)

        assistance_row.addStretch()

        layout.addLayout(assistance_row)

        # ---------------- RELEASE ----------------

        self.release_button = QPushButton("Release")
        self.release_button.setFixedSize(220, 52)

        self.release_button.setStyleSheet("""
            QPushButton {
                background-color: #19191c;
                border: 1px solid #38383e;
                border-radius: 17px;
                color: white;
                font-size: 16px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #242428;
                border: 1px solid #4a4a50;
            }

            QPushButton:pressed {
                background-color: #303034;
            }
        """)

        release_row = QHBoxLayout()
        release_row.addStretch()
        release_row.addWidget(self.release_button)
        release_row.addStretch()

        layout.addSpacing(12)
        layout.addLayout(release_row)

        layout.addStretch()

        self.setLayout(layout)

        # ---------------- CONNECTIONS ----------------

        self.assistance_slider.valueChanged.connect(
            self.update_assistance
        )

        self.minus_button.clicked.connect(
            self.decrease_assistance
        )

        self.plus_button.clicked.connect(
            self.increase_assistance
        )

        self.release_button.clicked.connect(
            self.release_grip
        )

        # Starting assistance level
        self.assistance_slider.setValue(60)
        self.update_assistance(60)


    # ---------------- ASSISTANCE FUNCTIONS ----------------

    def update_assistance(self, value):

        # Keep the value in 5% steps
        rounded_value = round(value / 5) * 5

        if rounded_value != value:
            self.assistance_slider.setValue(rounded_value)
            return

        self.assistance_value.setText(
            str(rounded_value) + "%"
        )

        # Assistance off
        if rounded_value == 0:

            self.assistance_value.setStyleSheet("""
                color: #8e8e93;
                font-size: 38px;
                font-weight: bold;
            """)

        # Assistance active
        else:

            self.assistance_value.setStyleSheet("""
                color: #5ac8fa;
                font-size: 38px;
                font-weight: bold;
            """)

        self.update_slider_style(rounded_value)


    def update_slider_style(self, value):

        # Calculate where the blue part of the slider should stop
        position = value / 100

        self.assistance_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                height: 6px;
                border-radius: 3px;
                background-color: #2c2c30;
            }

            QSlider::sub-page:horizontal {
                background-color: #5ac8fa;
                border-radius: 3px;
            }

            QSlider::add-page:horizontal {
                background-color: #2c2c30;
                border-radius: 3px;
            }

            QSlider::handle:horizontal {
                background-color: white;
                width: 20px;
                height: 20px;
                margin: -7px 0;
                border-radius: 10px;
            }
        """)


    def increase_assistance(self):

        current_value = self.assistance_slider.value()

        self.assistance_slider.setValue(
            min(current_value + 5, 100)
        )


    def decrease_assistance(self):

        current_value = self.assistance_slider.value()

        self.assistance_slider.setValue(
            max(current_value - 5, 0)
        )


    def release_grip(self):

        self.assistance_slider.setValue(0)