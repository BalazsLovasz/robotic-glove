import sys
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QFrame
)

class Dashboard(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Assistive Grip - Robotic Glove Dashboard")
        self.resize(1200, 700)

        self.build_ui()


    def build_ui(self):

        # Main layout
        main_layout = QVBoxLayout()

        # ---------------- HEADER ----------------

        title = QLabel("ASSISTIVE GRIP")
        subtitle = QLabel("Robotic Glove Monitoring System")
        demo_status = QLabel("●  DEMO MODE")

        title.setStyleSheet("font-size: 28px; font-weight: bold;")
        subtitle.setStyleSheet("font-size: 14px; color: grey;")
        demo_status.setStyleSheet("font-size: 14px;")

        header_left = QVBoxLayout()
        header_left.addWidget(title)
        header_left.addWidget(subtitle)

        header = QHBoxLayout()
        header.addLayout(header_left)
        header.addStretch()
        header.addWidget(demo_status)

        main_layout.addLayout(header)

        # ---------------- DASHBOARD CARDS ----------------

        cards_layout = QHBoxLayout()

        # Device status card
        device_card = QFrame()
        device_layout = QVBoxLayout()

        device_title = QLabel("DEVICE STATUS")
        device_title.setStyleSheet("font-size: 18px; font-weight: bold;")

        device_layout.addWidget(device_title)
        device_layout.addWidget(QLabel("Status:     Disconnected"))
        device_layout.addWidget(QLabel("Mode:       Demo"))
        device_layout.addWidget(QLabel("Battery:    -- %"))
        device_layout.addStretch()

        device_card.setLayout(device_layout)

        # Live grip card
        grip_card = QFrame()
        grip_layout = QVBoxLayout()

        grip_title = QLabel("LIVE GRIP")
        grip_title.setStyleSheet("font-size: 18px; font-weight: bold;")

        grip_layout.addWidget(grip_title)
        grip_layout.addWidget(QLabel("Thumb:       -- N"))
        grip_layout.addWidget(QLabel("Index:       -- N"))
        grip_layout.addWidget(QLabel("Middle:      -- N"))
        grip_layout.addWidget(QLabel("Ring:        -- N"))
        grip_layout.addWidget(QLabel("Pinky:       -- N"))

        grip_layout.addSpacing(20)

        total_force = QLabel("TOTAL FORCE:     -- N")
        total_force.setStyleSheet("font-size: 20px; font-weight: bold;")

        grip_layout.addWidget(total_force)
        grip_layout.addStretch()

        grip_card.setLayout(grip_layout)

        # Add cards to dashboard
        cards_layout.addWidget(device_card)
        cards_layout.addWidget(grip_card)

        main_layout.addLayout(cards_layout)

        self.setLayout(main_layout)


app = QApplication(sys.argv)

window = Dashboard()
window.show()

sys.exit(app.exec())