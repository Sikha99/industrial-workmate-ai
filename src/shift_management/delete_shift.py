
import sqlite3

from .database import DB_PATH, initialize_database


def delete_shift(shift_id):
    initialize_database()

    connection = sqlite3.connect(DB_PATH)

    try:
        cursor = connection.cursor()

        cursor.execute(
            "DELETE FROM shifts WHERE id = ?",
            (shift_id,)
        )

        connection.commit()

        if cursor.rowcount > 0:
            print(f"Shift ID {shift_id} deleted successfully!")
        else:
            print(f"No shift found with ID {shift_id}.")

    finally:
        connection.close()
