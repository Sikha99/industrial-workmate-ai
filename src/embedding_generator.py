
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer

# 1. Locate the project folder
PROJECT_DIR = Path(__file__).resolve().parent.parent

# 2. Locate and read the factory rules document
document_path = PROJECT_DIR / "data" / "factory_assignment_rules.txt"

with open(document_path, "r", encoding="utf-8") as file:
    document_text = file.read()

# 3. Split the document into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=50
)

chunks = text_splitter.split_text(document_text)

# 4. Load the embedding model
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# 5. Generate embeddings for all chunks
embeddings = model.encode(chunks)

# 6. Display the results
print("Total chunks:", len(chunks))
print("Total embeddings:", len(embeddings))
print("Dimensions of each embedding:", embeddings.shape[1])

for index, chunk in enumerate(chunks, start=1):
    print(f"\n--- Chunk {index} ---")
    print("Text:", chunk)
    print("Embedding shape:", embeddings[index - 1].shape)
