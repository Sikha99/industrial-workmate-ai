
from pathlib import Path

# Locate the project folder
PROJECT_DIR = Path(__file__).resolve().parent.parent

# Locate the factory rules document
document_path = PROJECT_DIR / "data" / "factory_assignment_rules.txt"

# Read the document
with open(document_path, "r", encoding="utf-8") as file:
    document_text = file.read()

# Display the document
print(document_text)
