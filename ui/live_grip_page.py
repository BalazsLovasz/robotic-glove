from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
)

from PySide6.QtCore import Qt


class LiveGripPage(QWidget):

    def __init__(self):
        super().__init__()

        self.build_ui()


    def build_ui(self):

        layout = QVBoxLayout()
        layout.setContentsMargins(55, 35, 55, 35)

        # ---------------- TOP BAR ----------------

        top_bar = QHBoxLayout()

        self.back_button = QPushButton("←")
        self.back_button.setFixedSize(50, 42)

        self.back_button.setStyleSheet("""
            QPushButton {
                background-color: #1c1c1e;
                border: 1px solid #2c2c2e;
                border-radius: 12px;
                font-size: 20px;
            }

            QPushButton:hover {
                background-color: #2c2c2e;
            }
        """)

        title = QLabel("LIVE GRIP")

        title.setStyleSheet("""
            font-size: 22px;
            font-weight: bold;
        """)

        top_bar.addWidget(self.back_button)
        top_bar.addSpacing(15)
        top_bar.addWidget(title)
        top_bar.addStretch()

        layout.addLayout(top_bar)

        # ---------------- CONTENT ----------------

        layout.addStretch()

        message = QLabel("Live Grip")
        message.setAlignment(Qt.AlignCenter)

        message.setStyleSheet("""
            font-size: 36px;
            font-weight: bold;
        """)

        description = QLabel(
            "Real-time force monitoring will appear here."
        )

        description.setAlignment(Qt.AlignCenter)

        description.setStyleSheet("""
            color: #8e8e93;
            font-size: 15px;
        """)

        layout.addWidget(message)
        layout.addWidget(description)

        layout.addStretch()

        self.setLayout(layout)