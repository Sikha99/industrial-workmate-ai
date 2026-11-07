
from typing import TypedDict, Any

from langgraph.graph import StateGraph, START, END

from intent_detector import (
    detect_intent,
    extract_details,
    validate_extracted_details,
    get_missing_field_questions,
    INTENT_SCHEMAS
)

from shift_management.create_shift import create_shift
from shift_management.get_shifts import get_shifts
from answer_generator import answer_question


# ----------------------------------
# 1. Define LangGraph State
# ----------------------------------

class FactoryState(TypedDict):
    user_message: str
    intent: str
    details: dict
    response: Any
    missing_fields: list
    user_answer: str


# ----------------------------------
# 2. Validation and Execution
# ----------------------------------

def validate_and_execute(intent, details):

    schema = INTENT_SCHEMAS[intent]

    is_valid, message = validate_extracted_details(
        details, schema
    )

    if not is_valid:
        missing = get_missing_field_questions(details, schema)

        return {
            "status": "missing_details",
            "message": message,
            "questions": [question for field, question in missing],
            "missing_fields": [field for field, question in missing],
            "details": details,
            "intent": intent
        }

    return create_shift(**details)


def prepare_shift_result(details):

    result = validate_and_execute("CREATE_SHIFT", details)

    missing_fields = []

    if isinstance(result, dict) and result.get("status") == "missing_details":
        missing_fields = result["missing_fields"]

    return {
        "details": details,
        "missing_fields": missing_fields,
        "response": result
    }


# ----------------------------------
# 3. LangGraph Nodes
# ----------------------------------

def detect_intent_node(state: FactoryState):

    result = detect_intent(state["user_message"])

    return {"intent": result["intent"]}


def create_shift_node(state: FactoryState):

    details = state["details"]

    if not details:
        details = extract_details(
            state["user_message"],
            "CREATE_SHIFT"
        )

    return prepare_shift_result(details)


def resume_shift_node(state: FactoryState):

    details = state["details"].copy()
    missing_fields = state["missing_fields"]

    if not missing_fields:
        return {"response": "No pending shift details found."}

    # Identify the first missing field
    field = missing_fields[0]
    schema = INTENT_SCHEMAS["CREATE_SHIFT"]

    # Get the user's answer
    answer = state["user_answer"]

    # Convert the answer if it should be a number
    if schema[field]["type"] == "number":
        try:
            answer = float(answer)
        except ValueError:
            return {
                "response": {
                    "status": "missing_details",
                    "message": "Invalid numeric value.",
                    "questions": ["Please enter a valid number."],
                    "missing_fields": missing_fields,
                    "details": details,
                    "intent": "CREATE_SHIFT"
                }
            }

    # Update the missing field
    details[field] = answer

    return prepare_shift_result(details)


def list_shifts_node(state: FactoryState):

    return {"response": get_shifts()}


def factory_question_node(state: FactoryState):

    return {
        "response": answer_question(state["user_message"])
    }


def unknown_node(state: FactoryState):

    return {
        "response": "This operation is not implemented yet."
    }


# ----------------------------------
# 4. Conditional Routing
# ----------------------------------

def route_start(state: FactoryState):

    if state["user_answer"]:
        return "resume_shift"

    return "detect_intent"


def route_request(state: FactoryState):

    intent = state["intent"]

    if intent == "CREATE_SHIFT":
        return "create_shift"

    elif intent == "LIST_SHIFTS":
        return "list_shifts"

    elif intent == "FACTORY_QUESTION":
        return "factory_question"

    return "unknown"


# ----------------------------------
# 5. Build LangGraph Workflow
# ----------------------------------

workflow = StateGraph(FactoryState)

# Register nodes
workflow.add_node("detect_intent", detect_intent_node)
workflow.add_node("create_shift", create_shift_node)
workflow.add_node("resume_shift", resume_shift_node)
workflow.add_node("list_shifts", list_shifts_node)
workflow.add_node("factory_question", factory_question_node)
workflow.add_node("unknown", unknown_node)

# Choose the starting node
workflow.set_conditional_entry_point(
    route_start,
    {
        "detect_intent": "detect_intent",
        "resume_shift": "resume_shift"
    }
)

# Route based on detected intent
workflow.add_conditional_edges(
    "detect_intent",
    route_request,
    {
        "create_shift": "create_shift",
        "list_shifts": "list_shifts",
        "factory_question": "factory_question",
        "unknown": "unknown"
    }
)

# Connect nodes to END
workflow.add_edge("create_shift", END)
workflow.add_edge("resume_shift", END)
workflow.add_edge("list_shifts", END)
workflow.add_edge("factory_question", END)
workflow.add_edge("unknown", END)

# Compile graph
factory_graph = workflow.compile()


# ----------------------------------
# 6. Main Application Function
# ----------------------------------

def process_request(user_message):

    initial_state = {
        "user_message": user_message,
        "intent": "",
        "details": {},
        "response": "",
        "missing_fields": [],
        "user_answer": ""
    }

    result = factory_graph.invoke(initial_state)

    return result["response"]


# ----------------------------------
# 7. Resume Pending Requests
# ----------------------------------

def resume_request(pending, user_answer):

    initial_state = {
        "user_message": "",
        "intent": pending["intent"],
        "details": pending["details"],
        "response": "",
        "missing_fields": pending["missing_fields"],
        "user_answer": user_answer
    }

    result = factory_graph.invoke(initial_state)

    return result["response"]

# 8. Local Testing

if __name__ == "__main__":

    user_message = input("Enter your request: ")

    print(process_request(user_message))
