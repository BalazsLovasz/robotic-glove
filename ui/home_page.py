from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QSlider,
    QFrame,
)

from PySide6.QtCore import Qt, QTimer

from storage import data_store


class HomePage(QWidget):

    def __init__(self):
        super().__init__()

        # The hand starts open, Grip is picked by default
        self.selected_mode = "Grip"
        self.is_active = False

        # Saves a reading every second while the grip is active
        self.log_timer = QTimer()
        self.log_timer.timeout.connect(self.log_reading)

        self.mode_descriptions = {
            "Pinch": "Thumb and index finger",
            "Grip": "All fingers",
        }

        self.build_ui()


    def build_ui(self):

        layout = QVBoxLayout()
        layout.setContentsMargins(55, 40, 55, 30)

        # ---------------- TITLE ----------------

        title = QLabel("Assistive Glove")
        title.setAlignment(Qt.AlignCenter)

        title.setStyleSheet("""
            color: #8e8e93;
            font-size: 16px;
            letter-spacing: 3px;
        """)

        layout.addWidget(title)
        layout.addStretch()

        # ---------------- MODE SWITCH ----------------

        mode_frame = QFrame()
        mode_frame.setFixedSize(480, 110)

        mode_frame.setStyleSheet("""
            QFrame {
                background-color: transparent;
            }
        """)

        mode_layout = QHBoxLayout(mode_frame)
        mode_layout.setContentsMargins(0, 0, 0, 0)
        mode_layout.setSpacing(20)

        mode_style = """
            QPushButton {
                background-color: #131316;
                border: 2px solid #2c2c30;
                border-radius: 26px;
                color: #8e8e93;
                font-size: 22px;
                font-weight: bold;
            }

            QPushButton:hover {
                border: 2px solid #5ac8fa;
                background-color: rgba(90, 200, 250, 35);
                color: white;
            }

            QPushButton:pressed {
                background-color: rgba(90, 200, 250, 70);
            }

            QPushButton:checked {
                background-color: #5ac8fa;
                border: 2px solid #5ac8fa;
                color: #08080a;
            }

            QPushButton:checked:hover {
                background-color: #7dd6fb;
                border: 2px solid #7dd6fb;
                color: #08080a;
            }

            QPushButton:disabled {
                background-color: #131316;
                border: 2px solid #1c1c1e;
                color: #4a4a4d;
            }

            QPushButton:checked:disabled {
                background-color: #1d5f7a;
                border: 2px solid #1d5f7a;
                color: white;
            }
        """

        self.mode_buttons = {}

        for name in self.mode_descriptions:

            button = QPushButton(name)
            button.setCheckable(True)
            button.setStyleSheet(mode_style)

            button.clicked.connect(
                lambda checked, mode=name: self.select_mode(mode)
            )

            mode_layout.addWidget(button)
            self.mode_buttons[name] = button

        mode_row = QHBoxLayout()
        mode_row.addStretch()
        mode_row.addWidget(mode_frame)
        mode_row.addStretch()

        layout.addLayout(mode_row)

        # ---------------- MODE DESCRIPTION ----------------

        self.mode_info = QLabel("")
        self.mode_info.setAlignment(Qt.AlignCenter)

        self.mode_info.setStyleSheet("""
            color: #8e8e93;
            font-size: 14px;
        """)

        layout.addSpacing(14)
        layout.addWidget(self.mode_info)
        layout.addSpacing(45)

        # ---------------- STRENGTH ----------------

        strength_title = QLabel("STRENGTH")
        strength_title.setAlignment(Qt.AlignCenter)

        strength_title.setStyleSheet("""
            color: #8e8e93;
            font-size: 12px;
            letter-spacing: 3px;
        """)

        self.strength_value = QLabel("50%")
        self.strength_value.setAlignment(Qt.AlignCenter)

        layout.addWidget(strength_title)
        layout.addSpacing(4)
        layout.addWidget(self.strength_value)
        layout.addSpacing(10)

        self.strength_slider = QSlider(Qt.Horizontal)

        self.strength_slider.setMinimum(0)
        self.strength_slider.setMaximum(100)
        self.strength_slider.setSingleStep(5)
        self.strength_slider.setPageStep(5)
        self.strength_slider.setFixedWidth(360)

        self.strength_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                height: 4px;
                border-radius: 2px;
                background-color: #2c2c30;
            }

            QSlider::sub-page:horizontal {
                background-color: #5ac8fa;
                border-radius: 2px;
            }

            QSlider::sub-page:horizontal:disabled {
                background-color: #4a4a4d;
            }

            QSlider::handle:horizontal {
                background-color: white;
                width: 22px;
                height: 22px;
                margin: -9px 0;
                border-radius: 11px;
            }

            QSlider::handle:horizontal:disabled {
                background-color: #6a6a6d;
            }
        """)

        slider_row = QHBoxLayout()
        slider_row.addStretch()
        slider_row.addWidget(self.strength_slider)
        slider_row.addStretch()

        layout.addLayout(slider_row)
        layout.addSpacing(50)

        # ---------------- MAIN BUTTON ----------------

        # One button does both jobs: Activate when open, Release when gripping
        self.main_button = QPushButton("Activate")
        self.main_button.setFixedSize(320, 70)

        button_row = QHBoxLayout()
        button_row.addStretch()
        button_row.addWidget(self.main_button)
        button_row.addStretch()

        layout.addLayout(button_row)
        layout.addStretch()

        self.setLayout(layout)

        # ---------------- CONNECTIONS ----------------

        self.strength_slider.valueChanged.connect(
            self.update_strength
        )

        self.main_button.clicked.connect(
            self.press_main_button
        )

        # Starting state
        self.strength_slider.setValue(50)
        self.update_strength(50)
        self.select_mode("Grip")
        self.update_look()


    # ---------------- MODE ----------------

    def select_mode(self, mode):

        self.selected_mode = mode

        # Only the picked mode stays highlighted
        for name, button in self.mode_buttons.items():
            button.setChecked(name == mode)

        self.mode_info.setText(self.mode_descriptions[mode])


    # ---------------- ACTIVATE / RELEASE ----------------

    def press_main_button(self):

        if self.is_active:
            self.release_grip()
        else:
            self.activate_grip()


    def activate_grip(self):

        self.is_active = True

        strength = self.strength_slider.value()
        self.send_to_glove(self.selected_mode, strength)

        # Save a reading now, then once every second
        self.log_reading()
        self.log_timer.start(1000)

        self.mode_info.setText(
            self.selected_mode + " active"
        )

        self.update_look()


    def release_grip(self):

        self.is_active = False

        self.send_to_glove("release", 0)

        # Stop saving readings
        self.log_timer.stop()

        self.mode_info.setText(
            self.mode_descriptions[self.selected_mode]
        )

        self.update_look()


    def send_to_glove(self, mode, strength):

        # TODO: connect this to the real glove (serial / bluetooth)
        print("Glove command:", mode, strength)


    def log_reading(self):

        # Later: read the finger forces and joint angles from the
        # glove sensors and pass them in as forces= and angles=
        data_store.save_reading(
            self.selected_mode,
            self.strength_slider.value()
        )


    # ---------------- LOOK ----------------

    def update_look(self):

        # While gripping, mode and strength are locked
        for button in self.mode_buttons.values():
            button.setEnabled(not self.is_active)

        self.strength_slider.setEnabled(not self.is_active)

        if self.is_active:

            self.main_button.setText("Release")

            # Dark button, white text
            self.main_button.setStyleSheet("""
                QPushButton {
                    background-color: #1c1c1e;
                    border: 1px solid #38383e;
                    border-radius: 35px;
                    color: white;
                    font-size: 20px;
                    font-weight: bold;
                }

                QPushButton:hover {
                    background-color: #2a2a2e;
                    border: 1px solid #5ac8fa;
                }
            """)

            self.strength_value.setStyleSheet("""
                color: #5ac8fa;
                font-size: 64px;
                font-weight: bold;
            """)

        else:

            self.main_button.setText("Activate")

            # White button, black text
            self.main_button.setStyleSheet("""
                QPushButton {
                    background-color: white;
                    border: none;
                    border-radius: 35px;
                    color: black;
                    font-size: 20px;
                    font-weight: bold;
                }

                QPushButton:hover {
                    background-color: #5ac8fa;
                }

                QPushButton:pressed {
                    background-color: #3aa8da;
                }
            """)

            self.strength_value.setStyleSheet("""
                color: white;
                font-size: 64px;
                font-weight: bold;
            """)


    # ---------------- STRENGTH ----------------

    def update_strength(self, value):

        # Keep the value in 5% steps
        rounded_value = round(value / 5) * 5

        if rounded_value != value:
            self.strength_slider.setValue(rounded_value)
            return

        self.strength_value.setText(str(rounded_value) + "%")