
from .database import DB_PATH, initialize_database
import sqlite3


def create_shift(name, shift_type, productive_hours):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO shifts (name, shift_type, productive_hours)
        VALUES (?, ?, ?)
        """,
        (name, shift_type, productive_hours)
    )

    connection.commit()
    connection.close()

    print(f"Shift '{name}' created successfully!")


if __name__ == "__main__":
    initialize_database()
    create_shift("Shift1", "Morning", 8)
