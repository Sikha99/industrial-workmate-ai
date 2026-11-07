
from datetime import datetime


def validate_shift(start_time, end_time, productive_hours):

    # Step 1: Validate the time format
    try:
        start = datetime.strptime(start_time, "%H:%M")
        end = datetime.strptime(end_time, "%H:%M")
    except (ValueError, TypeError):
        return False, "Enter time in HH:MM format.", None

    # Step 2: Calculate total shift duration
    if start_time == end_time:
        return False, "Start and end times cannot be the same.", None

    total_hours = (end - start).total_seconds() / 3600

    # Handle overnight shifts
    if total_hours < 0:
        total_hours += 24

    # Step 3: Validate productive hours
    try:
        productive_hours = float(productive_hours)
    except (ValueError, TypeError):
        return False, "Productive hours must be a number.", None

    if productive_hours <= 0:
        return False, "Productive hours must be greater than zero.", None

    if productive_hours > total_hours:
        return False, "Productive hours cannot exceed total shift duration.", None

    # Step 4: Calculate break hours
    break_hours = total_hours - productive_hours

    return True, "Shift details are valid.", break_hours


if __name__ == "__main__":
    result = validate_shift("22:00", "06:00", 7.5)
    print(result)
