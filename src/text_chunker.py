from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 1. Locate the project folder
PROJECT_DIR = Path(__file__).resolve().parent.parent

# 2. Locate and read the knowledge document
document_path = PROJECT_DIR / "data" / "factory_assignment_rules.txt"

with open(document_path, "r", encoding="utf-8") as file:
    document_text = file.read()

# 3. Configure the text splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,
    chunk_overlap=30,
    separators=["\n\n", "\n", " ", ""]
)

# 4. Split the document into chunks
chunks = text_splitter.split_text(document_text)

# 5. Display the chunks
print("Total chunks:", len(chunks))

for index, chunk in enumerate(chunks, start=1):
    print(f"\n--- Chunk {index} ---")
    print(chunk)


# from pathlib import Path
# from langchain_text_splitters import RecursiveCharacterTextSplitter

# # 1. Find the project folder
# PROJECT_DIR = Path(__file__).resolve().parent.parent

# # 2. Find the factory rules document
# document_path = PROJECT_DIR / "data" / "factory_assignment_rules.txt"

# # 3. Read the document
# with open(document_path, "r", encoding="utf-8") as file:
#     document_text = file.read()

# # 4. Create the text splitter
# text_splitter = RecursiveCharacterTextSplitter(
#     chunk_size=300,
#     chunk_overlap=50
# )

# # 5. Split the document into chunks
# chunks = text_splitter.split_text(document_text)

# # 6. Display the chunks
# for index, chunk in enumerate(chunks, start=1):
#     print(f"\n--- Chunk {index} ---")
#     print(chunk)