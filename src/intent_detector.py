
import json
import ollama


INTENT_SCHEMAS = {
    "CREATE_SHIFT": {
        "name": {
            "type": "string",
            "required": True,
            "label": "shift name"
        },
        "start_time": {
            "type": "string",
            "required": True,
            "label": "shift start time"
        },
        "end_time": {
            "type": "string",
            "required": True,
            "label": "shift end time"
        },
        "productive_hours": {
            "type": "number",
            "required": True,
            "label": "productive hours"
        }
    }
}


def detect_intent(user_message):
    response = ollama.chat(
        model="qwen2.5:1.5b",
        messages=[
            {
                "role": "system",
                "content": (
                    "You identify the user's intent in an industrial work assistant. "
                    "Return valid JSON containing only the field 'intent'. "
                    "Choose exactly one value from: CREATE_SHIFT, LIST_SHIFTS, "
                    "UPDATE_SHIFT, DELETE_SHIFT, CREATE_TRAINING, ASSIGN_SHIFT, "
                    "ASSIGN_TRAINING, FACTORY_QUESTION. "
                    "Classify requests to create, view, update, or delete shifts "
                    "according to the action explicitly requested by the user. "
                    "Questions about factory rules, workers, or whether an activity "
                    "is allowed must be classified as FACTORY_QUESTION. "
                    "Mentioning the word 'shift' alone does not mean the user wants "
                    "to view or create a shift. "
                    "Do not extract details or perform operations."
                )
            },
            {
                "role": "user",
                "content": user_message
            }
        ],
        format="json"
    )

    result = json.loads(response["message"]["content"])
    intent = result.get("intent")

    if intent not in {
        "CREATE_SHIFT",
        "LIST_SHIFTS",
        "UPDATE_SHIFT",
        "DELETE_SHIFT",
        "CREATE_TRAINING",
        "ASSIGN_SHIFT",
        "ASSIGN_TRAINING",
        "FACTORY_QUESTION"
    }:
        raise ValueError(f"Unknown intent returned: {intent}")

    return result


def extract_details(user_message, intent):
    schema = INTENT_SCHEMAS.get(intent)

    if schema is None:
        raise ValueError(f"No schema defined for intent: {intent}")

    # Build the extraction schema from metadata.
    extraction_schema = {
        field: metadata["type"]
        for field, metadata in schema.items()
    }

    response = ollama.chat(
        model="qwen2.5:1.5b",
        messages=[
            {
                "role": "system",
                "content": (
                    "Extract information from the user's message. "
                    f"Return a flat JSON object matching this schema: "
                    f"{json.dumps(extraction_schema)}. "
                    "Use null for any field whose value is not explicitly "
                    "provided or clearly stated in the user's message. "
                    "Never calculate, infer, or assume missing values. "
                    "Extract shift times strictly in 24-hour HH:MM format. "
                    "Use values such as 06:00 and 14:00, without AM or PM. "
                    "Return only the fields defined in the schema."
                    "Never infer shift start or end times from names such as "
                    "'morning', 'evening', or 'night'. Return null unless the "
                    "user explicitly provides that time. "
                )
            },
            {
                "role": "user",
                "content": user_message
            }
        ],
        format="json"
    )

    return json.loads(response["message"]["content"])


def validate_extracted_details(details, schema):
    # Check whether the extracted object contains exactly the expected fields.
    if not isinstance(details, dict) or set(details) != set(schema):
        return False, "Fields do not match the schema."

    # Find all missing fields that are required.
    missing_fields = [
        field
        for field, metadata in schema.items()
        if metadata["required"]
        and (
            details[field] is None
            or (
                isinstance(details[field], str)
                and not details[field].strip()
            )
        )
    ]

    if missing_fields:
        missing_labels = [
            schema[field]["label"]
            for field in missing_fields
        ]

        return False, (
            f"Missing required fields: {', '.join(missing_labels)}."
        )

    # Validate data types for fields that have values.
    for field, metadata in schema.items():
        value = details[field]
        expected_type = metadata["type"]

        if value is None:
            continue

        if expected_type == "string" and not isinstance(value, str):
            return False, f"{metadata['label']} must be a string."

        if expected_type == "number" and (
            not isinstance(value, (int, float))
            or isinstance(value, bool)
        ):
            return False, f"{metadata['label']} must be a number."

    return True, "Details are valid."


def get_missing_field_questions(details, schema):

    questions = []

    for field, metadata in schema.items():

        value = details.get(field)

        is_missing = (
            value is None
            or (isinstance(value, str) and not value.strip())
        )

        if metadata["required"] and is_missing:

            label = metadata["label"]

            if field in ["start_time", "end_time"]:
                questions.append(
                    (field, f"What is the {label}? Please enter in HH:MM format (example: 06:00).")
                )

            else:
                questions.append(
                    (field, f"What is the {label}?")
                )

    return questions

