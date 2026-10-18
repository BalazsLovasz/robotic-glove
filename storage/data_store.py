import sqlite3

from datetime import datetime
from pathlib import Path


# This file lives in storage/, so go up one level to the project folder.
# The data folder sits in the project folder, so if the whole project is
# on a USB stick the data travels with it, whatever laptop it is plugged into.
BASE_FOLDER = Path(__file__).resolve().parent.parent
DATA_FOLDER = BASE_FOLDER / "data"
DB_FILE = DATA_FOLDER / "glove.db"

FINGERS = ["thumb", "index", "middle", "ring", "pinky"]


# ---------------- SETUP ----------------

def setup_database():

    # Returns True if a new data file had to be created,
    # False if one was already there.

    already_exists = DB_FILE.exists()

    try:
        DATA_FOLDER.mkdir(exist_ok=True)

        connection = sqlite3.connect(DB_FILE)

        # Does nothing if the table is already there
        connection.execute("""
            CREATE TABLE IF NOT EXISTS readings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                time TEXT,
                mode TEXT,
                assistance INTEGER,
                thumb_force REAL,
                index_force REAL,
                middle_force REAL,
                ring_force REAL,
                pinky_force REAL,
                thumb_angle REAL,
                index_angle REAL,
                middle_angle REAL,
                ring_angle REAL,
                pinky_angle REAL
            )
        """)

        connection.commit()
        connection.close()

    except (sqlite3.Error, OSError) as error:
        print("Could not set up the data file:", error)

    return not already_exists


# ---------------- SAVING ----------------

def save_reading(mode, assistance, forces=None, angles=None):

    # forces and angles are dictionaries like {"thumb": 2.5, "index": 3.1, ...}
    # They are left empty until the glove sensors are connected.

    force_values = []
    angle_values = []

    for finger in FINGERS:

        if forces is None:
            force_values.append(None)
        else:
            force_values.append(forces[finger])

        if angles is None:
            angle_values.append(None)
        else:
            angle_values.append(angles[finger])

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    row = [now, mode, assistance] + force_values + angle_values

    try:
        connection = sqlite3.connect(DB_FILE)

        connection.execute(
            "INSERT INTO readings (time, mode, assistance, "
            "thumb_force, index_force, middle_force, ring_force, pinky_force, "
            "thumb_angle, index_angle, middle_angle, ring_angle, pinky_angle) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            row
        )

        connection.commit()
        connection.close()

        return True

    except sqlite3.Error as error:
        # Don't crash the app if the stick is full or read-only
        print("Could not save reading:", error)
        return False


# ---------------- LOADING ----------------

def get_summary():

    summary = {
        "seconds": 0,
        "avg_assistance": None,
        "favourite_mode": None,
        "forces": {},
        "ranges": {},
    }

    for finger in FINGERS:
        summary["forces"][finger] = None
        summary["ranges"][finger] = None

    try:
        connection = sqlite3.connect(DB_FILE)

        # Each reading is saved once per second, so count = seconds
        row = connection.execute(
            "SELECT COUNT(*), AVG(assistance) FROM readings"
        ).fetchone()

        summary["seconds"] = row[0]
        summary["avg_assistance"] = row[1]

        row = connection.execute(
            "SELECT mode, COUNT(*) AS total FROM readings "
            "GROUP BY mode ORDER BY total DESC LIMIT 1"
        ).fetchone()

        if row is not None:
            summary["favourite_mode"] = row[0]

        # Average force per finger (empty values are skipped)
        force_query = "SELECT "

        for finger in FINGERS:
            force_query = force_query + "AVG(" + finger + "_force), "

        force_query = force_query.rstrip(", ") + " FROM readings"

        row = connection.execute(force_query).fetchone()

        for i in range(len(FINGERS)):
            summary["forces"][FINGERS[i]] = row[i]

        # Range of motion = biggest angle minus smallest angle
        angle_query = "SELECT "

        for finger in FINGERS:
            angle_query = (
                angle_query
                + "MAX(" + finger + "_angle) - MIN(" + finger + "_angle), "
            )

        angle_query = angle_query.rstrip(", ") + " FROM readings"

        row = connection.execute(angle_query).fetchone()

        for i in range(len(FINGERS)):
            summary["ranges"][FINGERS[i]] = row[i]

        connection.close()

    except sqlite3.Error as error:
        print("Could not load data:", error)

    return summary


def get_weekly_assistance(how_many=4):

    # Returns [(week, average assistance), ...] oldest first
    weeks = []

    try:
        connection = sqlite3.connect(DB_FILE)

        rows = connection.execute(
            "SELECT strftime('%Y-W%W', time) AS week, AVG(assistance) "
            "FROM readings GROUP BY week ORDER BY week DESC LIMIT ?",
            (how_many,)
        ).fetchall()

        connection.close()

        weeks = list(reversed(rows))

    except sqlite3.Error as error:
        print("Could not load weekly data:", error)

    return weeks


def get_daily_assistance(how_many=14):

    # Returns [(day, average assistance), ...] oldest first
    days = []

    try:
        connection = sqlite3.connect(DB_FILE)

        rows = connection.execute(
            "SELECT strftime('%Y-%m-%d', time) AS day, AVG(assistance) "
            "FROM readings GROUP BY day ORDER BY day DESC LIMIT ?",
            (how_many,)
        ).fetchall()

        connection.close()

        days = list(reversed(rows))

    except sqlite3.Error as error:
        print("Could not load daily data:", error)

    return days