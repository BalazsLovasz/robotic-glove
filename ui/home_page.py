from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QSlider,
)

from PySide6.QtCore import Qt


class HomePage(QWidget):

    def __init__(self):
        super().__init__()

        # Keeps track of which fingers are currently picked
        self.selected_fingers = set()

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

        # ---------------- HAND DIAGRAM ----------------

        # Soft glow sitting behind the hand, same idea as before
        hand_area = QWidget()
        hand_area.setFixedSize(560, 380)

        hand_area.setStyleSheet("""
            QWidget {
                background: qradialgradient(
                    cx: 0.5, cy: 0.55,
                    radius: 0.55,
                    fx: 0.5, fy: 0.55,
                    stop: 0 rgba(100, 120, 135, 100),
                    stop: 0.45 rgba(60, 70, 80, 55),
                    stop: 1 rgba(13, 13, 15, 0)
                );
            }
        """)

        hand_layout = QVBoxLayout(hand_area)
        hand_layout.setContentsMargins(0, 25, 0, 0)

        finger_style = """
            QPushButton {
                background-color: transparent;
                border: 2px solid #3a3a40;
                border-radius: 32px;
                color: #8e8e93;
                font-size: 11px;
                font-weight: bold;
            }

            QPushButton:hover {
                border: 2px solid #5ac8fa;
                background-color: rgba(90, 200, 250, 35);
                color: white;
            }

            QPushButton:checked {
                background-color: #5ac8fa;
                border: 2px solid #5ac8fa;
                color: #0d0d0f;
            }

            QPushButton:disabled {
                border: 2px solid #242426;
                color: #4a4a4d;
                background-color: transparent;
            }
        """

        # name, height -> taller middle finger, shorter thumb/pinky
        finger_data = [
            ("Thumb", 100),
            ("Index", 150),
            ("Middle", 175),
            ("Ring", 160),
            ("Pinky", 125),
        ]

        self.finger_buttons = {}

        fingers_row = QHBoxLayout()
        fingers_row.setSpacing(12)
        fingers_row.addStretch()

        for name, height in finger_data:

            button = QPushButton(name)
            button.setCheckable(True)
            button.setFixedSize(65, height)
            button.setStyleSheet(finger_style)

            # bottom align each finger so they look like they share one palm
            column = QVBoxLayout()
            column.addStretch()
            column.addWidget(button, 0, Qt.AlignBottom)

            fingers_row.addLayout(column)

            self.finger_buttons[name] = button

            button.clicked.connect(
                lambda checked, finger=name: self.toggle_finger(finger)
            )

        fingers_row.addStretch()

        hand_layout.addLayout(fingers_row)
        hand_layout.addSpacing(12)

        # Palm doubles as the "select all fingers" button
        self.palm_button = QPushButton("All Fingers")
        self.palm_button.setCheckable(True)
        self.palm_button.setFixedSize(373, 90)
        self.palm_button.setStyleSheet(finger_style.replace("32px", "24px"))

        self.palm_button.clicked.connect(self.toggle_all_fingers)

        palm_row = QHBoxLayout()
        palm_row.addStretch()
        palm_row.addWidget(self.palm_button)
        palm_row.addStretch()

        hand_layout.addLayout(palm_row)

        hand_row = QHBoxLayout()
        hand_row.addStretch()
        hand_row.addWidget(hand_area)
        hand_row.addStretch()

        layout.addLayout(hand_row)

        # ---------------- ASSISTANCE LEVEL ----------------

        assistance_title = QLabel("ASSISTANCE LEVEL")
        assistance_title.setAlignment(Qt.AlignCenter)

        assistance_title.setStyleSheet("""
            color: #8e8e93;
            font-size: 13px;
            font-weight: bold;
            letter-spacing: 2px;
        """)

        self.assistance_value = QLabel("0%")
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

            QPushButton:disabled {
                background-color: #19191c;
                border: 1px solid #242426;
                color: #4a4a4d;
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

        # ---------------- RELEASE / ACTIVATE ----------------

        self.release_button = QPushButton("Release")
        self.release_button.setFixedSize(200, 52)

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

        self.activate_button = QPushButton("Activate")
        self.activate_button.setFixedSize(200, 52)

        self.activate_button.setStyleSheet("""
            QPushButton {
                background-color: #0a84ff;
                border: 1px solid #0a84ff;
                border-radius: 17px;
                color: white;
                font-size: 16px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #2196ff;
            }

            QPushButton:pressed {
                background-color: #006fe0;
            }

            QPushButton:disabled {
                background-color: #19191c;
                border: 1px solid #28282c;
                color: #4a4a4d;
            }
        """)

        action_row = QHBoxLayout()
        action_row.addStretch()
        action_row.addWidget(self.release_button)
        action_row.addSpacing(20)
        action_row.addWidget(self.activate_button)
        action_row.addStretch()

        layout.addSpacing(12)
        layout.addLayout(action_row)

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

        self.activate_button.clicked.connect(
            self.activate_grip
        )

        # Starting state: nothing selected, everything locked until Release
        self.update_assistance(0)
        self.release_grip()


    # ---------------- FINGER SELECTION ----------------

    def toggle_finger(self, name):

        button = self.finger_buttons[name]

        if button.isChecked():
            self.selected_fingers.add(name)
        else:
            self.selected_fingers.discard(name)

        self.sync_palm_button()
        self.update_selection_dependent_controls()


    def toggle_all_fingers(self):

        select_all = self.palm_button.isChecked()

        for name, button in self.finger_buttons.items():

            button.setChecked(select_all)

            if select_all:
                self.selected_fingers.add(name)
            else:
                self.selected_fingers.discard(name)

        self.update_selection_dependent_controls()


    def sync_palm_button(self):

        all_selected = len(self.selected_fingers) == len(self.finger_buttons)
        self.palm_button.setChecked(all_selected)


    def update_selection_dependent_controls(self):

        has_selection = len(self.selected_fingers) > 0

        self.assistance_slider.setEnabled(has_selection)
        self.minus_button.setEnabled(has_selection)
        self.plus_button.setEnabled(has_selection)
        self.activate_button.setEnabled(has_selection)


    # ---------------- ACTIVATE / RELEASE ----------------

    def activate_grip(self):

        # Lock selection and strength while the grip is engaged
        for button in self.finger_buttons.values():
            button.setEnabled(False)

        self.palm_button.setEnabled(False)
        self.assistance_slider.setEnabled(False)
        self.minus_button.setEnabled(False)
        self.plus_button.setEnabled(False)
        self.activate_button.setEnabled(False)


    def release_grip(self):

        # Clear the selection
        self.selected_fingers.clear()

        for button in self.finger_buttons.values():
            button.setChecked(False)
            button.setEnabled(True)

        self.palm_button.setChecked(False)
        self.palm_button.setEnabled(True)

        # Reset strength and lock it again until a finger is picked
        self.assistance_slider.setValue(0)
        self.assistance_slider.setEnabled(False)
        self.minus_button.setEnabled(False)
        self.plus_button.setEnabled(False)

        self.activate_button.setEnabled(False)


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

            QSlider::sub-page:horizontal:disabled {
                background-color: #3a3a3d;
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

            QSlider::handle:horizontal:disabled {
                background-color: #6a6a6d;
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