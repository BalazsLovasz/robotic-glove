from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
)

from PySide6.QtCore import Qt, QDateTime
from PySide6.QtGui import QColor, QBrush, QPainter, QPen
from PySide6.QtCharts import (
    QChart,
    QChartView,
    QBarSeries,
    QBarSet,
    QBarCategoryAxis,
    QValueAxis,
    QLineSeries,
    QDateTimeAxis,
    QAbstractBarSeries,
)

from storage import data_store


class AnalyticsPage(QWidget):

    def __init__(self):
        super().__init__()

        # Which graph is showing
        self.current_metric = "Force"

        self.build_ui()
        self.load_data()


    def build_ui(self):

        layout = QVBoxLayout()
        layout.setContentsMargins(55, 30, 55, 25)

        # ---------------- TITLE ----------------

        title = QLabel("ANALYTICS")
        title.setAlignment(Qt.AlignCenter)

        title.setStyleSheet("""
            color: #8e8e93;
            font-size: 16px;
            letter-spacing: 3px;
        """)

        layout.addWidget(title)
        layout.addSpacing(15)

        # ---------------- TOP NUMBERS ----------------

        top_row = QHBoxLayout()
        top_row.addStretch()

        self.time_value = self.add_block(top_row, "TIME ACTIVE")
        self.assistance_value = self.add_block(top_row, "AVG ASSISTANCE")
        self.mode_value = self.add_block(top_row, "FAVOURITE MODE")

        top_row.addStretch()

        layout.addLayout(top_row)
        layout.addSpacing(15)

        # ---------------- GRAPH BUTTONS ----------------

        metric_style = """
            QPushButton {
                background-color: #131316;
                border: 2px solid #2c2c30;
                border-radius: 22px;
                color: #8e8e93;
                font-size: 15px;
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
                color: #08080a;
            }

            QPushButton:checked:hover {
                background-color: #7dd6fb;
                border: 2px solid #7dd6fb;
            }
        """

        self.metric_buttons = {}

        metric_row = QHBoxLayout()
        metric_row.addStretch()

        for name in ["Force", "Range of Motion", "Assistance"]:

            button = QPushButton(name)
            button.setCheckable(True)
            button.setFixedSize(180, 44)
            button.setStyleSheet(metric_style)

            button.clicked.connect(
                lambda checked, metric=name: self.show_metric(metric)
            )

            metric_row.addWidget(button)
            metric_row.addSpacing(15)

            self.metric_buttons[name] = button

        metric_row.addStretch()

        layout.addLayout(metric_row)
        layout.addSpacing(15)

        # ---------------- GRAPH TITLE + NOTE ----------------

        self.caption = QLabel("")
        self.caption.setAlignment(Qt.AlignCenter)

        self.caption.setStyleSheet("""
            color: #8e8e93;
            font-size: 12px;
            letter-spacing: 3px;
        """)

        # Shown instead of a graph when there is nothing to show yet
        self.note = QLabel("")
        self.note.setAlignment(Qt.AlignCenter)

        self.note.setStyleSheet("""
            color: #5ac8fa;
            font-size: 13px;
        """)

        layout.addWidget(self.caption)
        layout.addWidget(self.note)

        # ---------------- GRAPH ----------------

        self.chart_view = QChartView()
        self.chart_view.setRenderHint(QPainter.Antialiasing)
        self.chart_view.setMinimumHeight(240)

        self.chart_view.setStyleSheet("""
            background-color: transparent;
            border: none;
        """)

        layout.addWidget(self.chart_view, 1)

        self.setLayout(layout)


    # ---------------- SMALL HELPERS ----------------

    def add_block(self, row, title):

        # A small title with a number underneath, added to the row.
        # Returns the number label so it can be updated later.

        column = QVBoxLayout()

        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignCenter)

        title_label.setStyleSheet("""
            color: #8e8e93;
            font-size: 11px;
            letter-spacing: 2px;
        """)

        value_label = QLabel("—")
        value_label.setAlignment(Qt.AlignCenter)

        value_label.setStyleSheet("""
            color: white;
            font-weight: bold;
            font-size: 30px;
        """)

        column.addWidget(title_label)
        column.addWidget(value_label)

        row.addLayout(column)
        row.addSpacing(60)

        return value_label


    def format_time(self, seconds):

        hours = seconds // 3600
        minutes = (seconds % 3600) // 60

        if hours > 0:
            return str(hours) + "h " + str(minutes) + "m"

        if minutes > 0:
            return str(minutes) + "m " + str(seconds % 60) + "s"

        return str(seconds) + "s"


    # ---------------- LOADING SAVED DATA ----------------

    def load_data(self):

        self.summary = data_store.get_summary()
        self.daily = data_store.get_daily_assistance()

        # Top numbers
        self.time_value.setText(self.format_time(self.summary["seconds"]))

        if self.summary["avg_assistance"] is None:
            self.assistance_value.setText("—")
        else:
            self.assistance_value.setText(
                str(round(self.summary["avg_assistance"])) + "%"
            )

        if self.summary["favourite_mode"] is None:
            self.mode_value.setText("—")
        else:
            self.mode_value.setText(self.summary["favourite_mode"])

        # Redraw whichever graph is showing with the new data
        self.show_metric(self.current_metric)


    # ---------------- SWITCHING GRAPHS ----------------

    def show_metric(self, metric):

        self.current_metric = metric

        # Only the picked button stays highlighted
        for name, button in self.metric_buttons.items():
            button.setChecked(name == metric)

        self.note.setText("")

        if metric == "Force":

            self.caption.setText("AVERAGE FORCE PER FINGER (N)")

            values = []
            for finger in data_store.FINGERS:
                values.append(self.summary["forces"][finger])

            if self.all_empty(values):
                self.note.setText("No sensor data yet. Connect the glove sensors to see this.")

            self.chart = self.make_bar_chart(values, 1, "#5ac8fa")

        elif metric == "Range of Motion":

            self.caption.setText("RANGE OF MOTION PER FINGER (DEGREES)")

            values = []
            for finger in data_store.FINGERS:
                values.append(self.summary["ranges"][finger])

            if self.all_empty(values):
                self.note.setText("No sensor data yet. Connect the glove sensors to see this.")

            self.chart = self.make_bar_chart(values, 0, "#bf5af2")

        else:

            self.caption.setText("AVERAGE ASSISTANCE PER DAY (%)")

            if len(self.daily) == 0:
                self.note.setText("Nothing recorded yet. Activate the glove to start.")

            self.chart = self.make_line_chart()

        self.chart_view.setChart(self.chart)


    def all_empty(self, values):

        for value in values:
            if value is not None:
                return False

        return True


    # ---------------- BUILDING THE GRAPHS ----------------

    def base_chart(self):

        # Dark, flat look to match the rest of the app
        chart = QChart()
        chart.setBackgroundBrush(QBrush(QColor("#08080a")))
        chart.setBackgroundRoundness(0)
        chart.legend().hide()

        return chart


    def style_axes(self, axes):

        for axis in axes:
            axis.setLabelsColor(QColor("#8e8e93"))
            axis.setGridLineColor(QColor("#1c1c1e"))
            axis.setLinePen(QPen(QColor("#2c2c30")))


    def make_bar_chart(self, raw_values, decimals, color):

        chart = self.base_chart()

        # Missing values are drawn as 0
        values = []

        for value in raw_values:
            if value is None:
                values.append(0)
            else:
                values.append(round(value, decimals))

        bar_set = QBarSet("")

        for value in values:
            bar_set.append(value)

        bar_set.setColor(QColor(color))
        bar_set.setBorderColor(QColor(color))
        bar_set.setLabelColor(QColor("white"))

        series = QBarSeries()
        series.append(bar_set)
        series.setBarWidth(0.45)

        # Only write the numbers on the bars if there is real data
        if not self.all_empty(raw_values):
            series.setLabelsVisible(True)
            series.setLabelsPosition(QAbstractBarSeries.LabelsOutsideEnd)

        chart.addSeries(series)

        # X axis = the five fingers
        axis_x = QBarCategoryAxis()

        for finger in data_store.FINGERS:
            axis_x.append(finger.capitalize())

        # Y axis = the values
        top = max(values) * 1.25

        if top == 0:
            top = 10

        axis_y = QValueAxis()
        axis_y.setRange(0, top)
        axis_y.setLabelFormat("%." + str(decimals) + "f")

        self.style_axes([axis_x, axis_y])

        chart.addAxis(axis_x, Qt.AlignBottom)
        chart.addAxis(axis_y, Qt.AlignLeft)

        series.attachAxis(axis_x)
        series.attachAxis(axis_y)

        return chart


    def make_line_chart(self):

        chart = self.base_chart()

        series = QLineSeries()
        series.setPointsVisible(True)

        pen = QPen(QColor("#5ac8fa"))
        pen.setWidth(3)
        series.setPen(pen)

        first_day = None
        last_day = None

        for day, average in self.daily:

            moment = QDateTime.fromString(day, "yyyy-MM-dd")
            series.append(moment.toMSecsSinceEpoch(), average)

            if first_day is None:
                first_day = moment

            last_day = moment

        chart.addSeries(series)

        # X axis = days (a day of space either side so one point still fits)
        if first_day is None:
            last_day = QDateTime.currentDateTime()
            first_day = last_day.addDays(-6)

        axis_x = QDateTimeAxis()
        axis_x.setRange(first_day.addDays(-1), last_day.addDays(1))
        axis_x.setFormat("dd MMM")
        axis_x.setTickCount(7)

        # Y axis = assistance level
        axis_y = QValueAxis()
        axis_y.setRange(0, 100)
        axis_y.setLabelFormat("%d")

        self.style_axes([axis_x, axis_y])

        chart.addAxis(axis_x, Qt.AlignBottom)
        chart.addAxis(axis_y, Qt.AlignLeft)

        series.attachAxis(axis_x)
        series.attachAxis(axis_y)

        return chart