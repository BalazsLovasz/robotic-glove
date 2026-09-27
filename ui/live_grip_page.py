from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
)

from PySide6.QtCore import Qt


class LiveGripPage(QWidget):

    def __init__(self):
        super().__init__()
        self.build_ui()


    def build_ui(self):

        layout = QVBoxLayout()
        layout.setContentsMargins(55, 35, 55, 35)

        title = QLabel("Live Grip")
        title.setAlignment(Qt.AlignCenter)

        title.setStyleSheet("""
            font-size: 32px;
            font-weight: bold;
        """)

        layout.addWidget(title)

        layout.addStretch()

        message = QLabel(
            "Real-time grip monitoring will appear here."
        )

        message.setAlignment(Qt.AlignCenter)

        message.setStyleSheet("""
            color: #8e8e93;
            font-size: 15px;
        """)

        layout.addWidget(message)

        layout.addStretch()

        self.setLayout(layout)