
from shift_management.create_shift import create_shift
from shift_management.get_shifts import get_shifts

from intent_detector import (
    detect_intent,
    extract_details,
    validate_extracted_details,
    get_missing_field_questions,
    INTENT_SCHEMAS
)


user_message = input("Enter your request: ")

# Step 1: Detect intent
result = detect_intent(user_message)
intent = result["intent"]

print("Detected intent:", intent)


# Step 2: Handle operations that require no details
if intent == "LIST_SHIFTS":

    shifts = get_shifts()

    if shifts:
        print("\nSaved shifts:")

        for shift in shifts:
            print(shift)
    else:
        print("No shifts have been created yet.")


# Step 3: Handle operations that require details
elif intent in INTENT_SCHEMAS:

    # Extract details
    details = extract_details(user_message, intent)
    print("Extracted details:", details)

    schema = INTENT_SCHEMAS[intent]

    # Validate extracted details
    is_valid, message = validate_extracted_details(
        details,
        schema
    )

    # Ask for missing information
    if not is_valid:
        print(message)

        questions = get_missing_field_questions(
            details,
            schema
        )

        for field, question in questions:
            answer = input(question + " ").strip()

            expected_type = schema[field]["type"]

            if expected_type == "number":
                answer = float(answer)

            details[field] = answer

        # Validate again after collecting answers
        is_valid, message = validate_extracted_details(
            details,
            schema
        )

    # Display the result
    print(message)
    print("Final details:", details)

    # Execute the operation
    if is_valid and intent == "CREATE_SHIFT":
        create_shift(**details)


# Step 4: Handle unsupported operations
else:
    print("This operation is not implemented yet.")
