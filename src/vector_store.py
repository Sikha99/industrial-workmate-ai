

from pathlib import Path
import chromadb
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer

# 1. Locate the project folder
PROJECT_DIR = Path(__file__).resolve().parent.parent

# 2. Read the factory rules document
document_path = PROJECT_DIR / "data" / "factory_assignment_rules.txt"

with open(document_path, "r", encoding="utf-8") as file:
    document_text = file.read()

# 3. Split the document into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,
    chunk_overlap=30,
    separators=["\n\n", "\n", " ", ""]
)

chunks = text_splitter.split_text(document_text)

# 4. Load the embedding model
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# 5. Generate embeddings for all chunks
embeddings = model.encode(chunks).tolist()

# 6. Connect to the persistent ChromaDB database
database_path = PROJECT_DIR / "chroma_db"
client = chromadb.PersistentClient(path=str(database_path))

# 7. Access the existing collection
collection = client.get_or_create_collection(name="factory_rules")

# 8. Replace the old records with the new chunks
client.delete_collection(name="factory_rules")
collection = client.create_collection(name="factory_rules")

collection.add(
    ids=[f"chunk_{i}" for i in range(1, len(chunks) + 1)],
    documents=chunks,
    embeddings=embeddings
)

# 9. Display confirmation
print("Total chunks stored:", collection.count())

for chunk_id, chunk_text in zip(
    [f"chunk_{i}" for i in range(1, len(chunks) + 1)],
    chunks
):
    print(f"\n--- {chunk_id} ---")
    print(chunk_text)


# from pathlib import Path
# import chromadb
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from sentence_transformers import SentenceTransformer

# # 1. Locate the project folder
# PROJECT_DIR = Path(__file__).resolve().parent.parent

# # 2. Read the factory rules document
# document_path = PROJECT_DIR / "data" / "factory_assignment_rules.txt"

# with open(document_path, "r", encoding="utf-8") as file:
#     document_text = file.read()

# # 3. Split the document into chunks
# text_splitter = RecursiveCharacterTextSplitter(
#     chunk_size=300,
#     chunk_overlap=50
# )
# chunks = text_splitter.split_text(document_text)

# # 4. Load the embedding model
# model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# # 5. Generate embeddings
# embeddings = model.encode(chunks).tolist()

# # 6. Create a local ChromaDB database
# database_path = PROJECT_DIR / "chroma_db"
# client = chromadb.PersistentClient(path=str(database_path))

# # 7. Create or access a collection
# collection = client.get_or_create_collection(name="factory_rules")

# # 8. Store chunks, embeddings, and IDs
# collection.upsert(
#     ids=[f"chunk_{i}" for i in range(len(chunks))],
#     documents=chunks,
#     embeddings=embeddings
# )

# # 9. Display confirmation
# print("Total chunks stored:", collection.count())
# print("Database location:", database_path)
