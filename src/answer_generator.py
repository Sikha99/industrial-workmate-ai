
from pathlib import Path

import chromadb
import ollama
from sentence_transformers import SentenceTransformer, util


# 1. Locate the project folder
PROJECT_DIR = Path(__file__).resolve().parent.parent


# 2. Connect to the existing ChromaDB database
client = chromadb.PersistentClient(
    path=str(PROJECT_DIR / "chroma_db")
)

collection = client.get_collection(
    name="factory_rules"
)


# 3. Load the embedding model
embedding_model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)


# 4. Configure the local LLM and threshold
LLM_MODEL = "qwen2.5:1.5b"
SIMILARITY_THRESHOLD = 0.60

FALLBACK = (
    "No matching information found in the factory knowledge base."
)


# 5. Answer a question using RAG
def answer_question(question):

    # Convert the question into an embedding
    question_embedding = embedding_model.encode(
        question,
        convert_to_tensor=True
    )

    # Retrieve the most relevant factory rule
    results = collection.query(
        query_embeddings=[question_embedding.tolist()],
        n_results=1,
        include=["documents"]
    )

    # Handle an empty retrieval result
    if not results["documents"] or not results["documents"][0]:
        return FALLBACK

    # Get the retrieved factory rule
    retrieved_context = results["documents"][0][0]

    # Convert the retrieved rule into an embedding
    retrieved_embedding = embedding_model.encode(
        retrieved_context,
        convert_to_tensor=True
    )

    # Calculate cosine similarity
    similarity = util.cos_sim(
        question_embedding.float(),
        retrieved_embedding.float()
    ).item()

    print(f"\nEmbedding similarity: {similarity:.4f}")

    # Check the similarity threshold
    if similarity < SIMILARITY_THRESHOLD:
        print("Result rejected: similarity is below threshold.")
        return FALLBACK

    # Generate the answer using Qwen through Ollama
    response = ollama.chat(
        model=LLM_MODEL,
        messages=[
            {
                "role": "system",
                
             "content": (
                "You are a professional factory work assistant. "
                "Answer using only the provided factory rule. "
                "Treat the rule as the source of truth, even if the "
                "user's question contains a false assumption. "
                "Never contradict the rule or reverse its prohibitions, "
                "priorities, responsibilities, or conditions. "
                "Do not invent information or discuss unrelated rules. "
                "Never mention rule numbers. "
                "Start with a direct, concise answer. "
                "If the rule does not contain the answer, say that "
                "the information is unavailable."
)

            },
            {
                "role": "user",
                "content": (
                    f"Factory context:\n{retrieved_context}\n\n"
                    f"Question: {question}"
                )
            }
        ]
    )

    # Return the generated answer
    return response["message"]["content"]



# 6. Run the RAG assistant from the terminal
if __name__ == "__main__":

    print("Factory Work Assistant")
    print("Type 'exit' to quit.\n")

    while True:
        question = input("Ask your question: ").strip()

        if question.lower() == "exit":
            print("Goodbye!")
            break

        if not question:
            continue

        answer = answer_question(question)

        print("\nAnswer:", answer)
        print("-" * 50)

