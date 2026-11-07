from .create_shift import create_shift
from .get_shifts import get_shifts
from .update_shift import update_shift
from .delete_shift import delete_shift
def show_shifts():
    shifts = get_shifts()

    if not shifts:
        print("No shifts found.")
        return

    print("\nSaved Shifts:")
    print("-" * 55)

    for shift in shifts:
        print(
            f"ID: {shift[0]} | "
            f"Name: {shift[1]} | "
            f"Start: {shift[2]} | "
            f"End: {shift[3]} | "
            f"Productive Hours: {shift[4]}"
        )
def add_shift():
    name = input("Enter shift name: ")
    start_time = input("Enter start time (HH:MM): ")
    end_time = input("Enter end time (HH:MM): ")
    productive_hours = input("Enter productive hours: ")

    try:
        productive_hours = float(productive_hours)
    except ValueError:
        print("Error: Productive hours must be a number.")
        return

    create_shift(
        name,
        start_time,
        end_time,
        productive_hours
    )
def edit_shift():
    try:
        shift_id = int(input("Enter shift ID to update: "))
        productive_hours = float(input("Enter new productive hours: "))
    except ValueError:
        print("Error: Enter a valid shift ID and productive hours.")
        return

    name = input("Enter new shift name: ")
    start_time = input("Enter new start time (HH:MM): ")
    end_time = input("Enter new end time (HH:MM): ")

    update_shift(
        shift_id,
        name,
        start_time,
        end_time,
        productive_hours
    )

def remove_shift():
    try:
        shift_id = int(input("Enter shift ID to delete: "))
    except ValueError:
        print("Error: Enter a valid shift ID.")
        return

    confirmation = input(
        f"Are you sure you want to delete shift ID {shift_id}? (yes/no): "
    ).strip().lower()

    if confirmation != "yes":
        print("Deletion cancelled.")
        return

    delete_shift(shift_id)


if __name__ == "__main__":
    while True:
        print("\n=== Industrial WorkMate AI ===")
        print("1. View shifts")
        print("2. Create shift")
        print("3. Update shift")
        print("4. Delete shift")
        print("5. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            show_shifts()
        elif choice == "2":
            add_shift()
        elif choice == "3":
            edit_shift()
        elif choice == "4":
            remove_shift()
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please choose 1–5.")
