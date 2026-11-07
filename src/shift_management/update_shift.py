
import sqlite3
from .shift_validator import validate_shift

from .database import DB_PATH, initialize_database


def update_shift(shift_id, name, start_time, end_time, productive_hours):
   
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
            UPDATE shifts
            SET name = ?, start_time = ?, end_time = ?,
                productive_hours = ?
            WHERE id = ?
            """,
            (name, start_time, end_time, productive_hours, shift_id)
        )

        connection.commit()

        if cursor.rowcount > 0:
            print(f"Shift ID {shift_id} updated successfully!")
        else:
            print(f"No shift found with ID {shift_id}.")

    except sqlite3.IntegrityError:
        print(f"Error: A shift named '{name}' already exists.")

    finally:
        connection.close()


if __name__ == "__main__":
    update_shift(1, "Shift1", "22:00", "06:00", 7.5)
