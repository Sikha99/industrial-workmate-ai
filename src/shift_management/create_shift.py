
import sqlite3
from .shift_validator import validate_shift

from .database import DB_PATH, initialize_database


def create_shift(name, start_time, end_time, productive_hours):

    # Validate the shift name
    if not name.strip():
        print("Error: Shift name cannot be empty.")
        return

    # Validate shift details using the shared validator
    is_valid, message, break_hours = validate_shift(
        start_time, end_time, productive_hours
    )

    if not is_valid:
        print(f"Error: {message}")
        return

    print(f"Break duration: {break_hours} hours")

    initialize_database()

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO shifts (name, start_time, end_time, productive_hours)
            VALUES (?, ?, ?, ?)
            """,
            (name, start_time, end_time, productive_hours)
        )

        connection.commit()
        print(f"Shift '{name}' created successfully!")

    except sqlite3.IntegrityError:
        print(f"Error: A shift named '{name}' already exists.")

    finally:
        connection.close()


if __name__ == "__main__":
    create_shift("Shift1", "10:00", "19:00", 8)
