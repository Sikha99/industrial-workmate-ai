
import sqlite3

from .database import DB_PATH, initialize_database


def get_shifts():
    initialize_database()

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, name, start_time, end_time, productive_hours
        FROM shifts
        ORDER BY id
        """
    )

    shifts = cursor.fetchall()
    connection.close()

    return shifts


if __name__ == "__main__":
    shifts = get_shifts()

    print("Saved shifts:")

    for shift in shifts:
        print(shift)
