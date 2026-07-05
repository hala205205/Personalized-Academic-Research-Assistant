import json  # Used to read chunks from the JSON file
import numpy as np  # Used to sort similarity scores
from sentence_transformers import SentenceTransformer  # Used to create semantic embeddings
from sklearn.metrics.pairwise import cosine_similarity  # Used to calculate similarity between vectors

from gemini_query_rewriter import rewrite_query_with_gemini  # Rewrite user query using Gemini
from memory import add_question  # Save user questions into memory
from personalized_ranker import personalize_results  # Re-rank results using memory
from answer_generator import generate_answer_with_gemini  # Generate final answer from retrieved passages

from pathlib import Path  # Handle file paths correctly

BASE_DIR = Path(__file__).resolve().parent
CHUNKS_FILE = BASE_DIR / "data" / "chunks.json"
MODEL_NAME = "sentence-transformers/paraphrase-MiniLM-L3-v2"  # Lightweight semantic embedding model


def load_chunks():
    # Load all chunks from chunks.json

    with open(CHUNKS_FILE, "r", encoding="utf-8") as file:
        # Open the chunks file in read mode

        chunks = json.load(file)
        # Convert JSON content into a Python list

    return chunks
    # Return all loaded chunks


def build_embeddings(chunks):
    # Build semantic embeddings for all chunks

    model = SentenceTransformer(MODEL_NAME)
    # Load the pre-trained sentence-transformer model

    texts = [chunk["text"] for chunk in chunks]
    # Extract only the text from each chunk

    embeddings = model.encode(texts, show_progress_bar=True)
    # Convert chunk texts into semantic vectors

    return model, embeddings
    # Return both the model and the embeddings


def retrieve(query, chunks, model, embeddings, top_k=3):
    # Retrieve the most semantically relevant chunks for a query

    query_embedding = model.encode([query])
    # Convert the user query into a semantic vector

    similarity_scores = cosine_similarity(query_embedding, embeddings).flatten()
    # Calculate cosine similarity between query and all chunk embeddings

    top_indices = np.argsort(similarity_scores)[-top_k:][::-1]
    # Get indices of the top results in descending order

    results = []
    # Create an empty list to store retrieved results

    for index in top_indices:
        # Loop through the top matching chunks

        results.append({
            "score": float(similarity_scores[index]),  # Store similarity score
            "paper_name": chunks[index]["paper_name"],  # Store source paper name
            "page": chunks[index]["page"],  # Store source page number
            "text": chunks[index]["text"]  # Store retrieved chunk text
        })

    return results
    # Return the top retrieved chunks


if __name__ == "__main__":
    # Run this block only when this file is executed directly

    chunks = load_chunks()
    # Load chunks from the JSON file

    model, embeddings = build_embeddings(chunks)
    # Build semantic embeddings for all chunks

    print("Semantic Retriever is ready. Type 'exit' to stop.")
    # Inform the user that the retriever is ready

    while True:
        # Keep asking the user for questions

        query = input("\nAsk a question about the papers: ")
        # Read the user's question

        if query.lower() in ["exit", "quit"]:
            # If the user wants to stop

            break
            # Exit the loop
            
        print("\nRewriting query using Gemini...")
        rewritten_query = rewrite_query_with_gemini(query)

        print(f"Original Query: {query}")
        print(f"Rewritten Query: {rewritten_query}")

        results = retrieve(rewritten_query, chunks, model, embeddings)
        # Retrieve top relevant chunks
        
        add_question(query)
        # Save the user's question into long-term memory

        personalized_results = personalize_results(results, model)
        # Re-rank results using semantic similarity between memory and chunks
        
        top_results_for_answer = personalized_results[:3]
        # Use top 3 personalized results as context for answer generation

        print("\nGenerating final answer using retrieved passages...")
        # Tell user that answer generation is running

        final_answer = generate_answer_with_gemini(query, top_results_for_answer)
        # Generate answer using original user question and retrieved passages

        print("\nFinal Answer:")
        print(final_answer)
        
        print("\nSources Used:")
        for i, result in enumerate(top_results_for_answer, start=1):
            print(f"{i}. {result['paper_name']} - Page {result['page']}")

        for i, result in enumerate(personalized_results, start=1):
            # Print each retrieved result

            print(f"\nResult {i}")
            print(f"Semantic Score: {result['semantic_score']:.4f}")
            print(f"Memory Similarity: {result['memory_similarity']:.4f}")
            print(f"Memory Bonus: {result['memory_bonus']:.4f}")
            print(f"Final Score: {result['final_score']:.4f}")
            print(f"Paper: {result['paper_name']}")
            print(f"Page: {result['page']}")
            print(f"Text: {result['text'][:1200]}...")
