
from pathlib import Path
import chromadb
from sentence_transformers import SentenceTransformer

# 1. Locate the project folder
PROJECT_DIR = Path(__file__).resolve().parent.parent

# 2. Connect to the existing ChromaDB database
database_path = PROJECT_DIR / "chroma_db"
client = chromadb.PersistentClient(path=str(database_path))

# 3. Access the factory rules collection
collection = client.get_collection(name="factory_rules")

# 4. Load the embedding model
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# 5. Write a user question
question = "Can an operator work two shifts on the same day?"

# 6. Convert the question into an embedding
question_embedding = model.encode(question).tolist()

# 7. Search ChromaDB for the 2 most relevant chunks
results = collection.query(
    query_embeddings=[question_embedding],
    n_results=1
)

# 8. Display the retrieved chunks
print("User question:", question)
print("\nRetrieved results:")

for index, document in enumerate(results["documents"][0], start=1):
    print(f"\n--- Result {index} ---")
    print(document)
