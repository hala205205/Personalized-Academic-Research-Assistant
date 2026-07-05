import json  # Used to read chunks from JSON file
import numpy as np  # Used to sort similarity scores
from sklearn.feature_extraction.text import TfidfVectorizer  # Converts text into TF-IDF vectors
from sklearn.metrics.pairwise import cosine_similarity  # Calculates similarity between query and chunks


CHUNKS_FILE = "data/chunks.json"  # Path of the chunks file created from PDFs


def load_chunks():
    # Load all text chunks from chunks.json

    with open(CHUNKS_FILE, "r", encoding="utf-8") as file:
        # Open the JSON file in read mode

        chunks = json.load(file)
        # Convert JSON content into a Python list

    return chunks
    # Return the loaded chunks


def build_tfidf_index(chunks):
    # Build a TF-IDF search index from the chunks

    texts = [chunk["text"] for chunk in chunks]
    # Extract only the text from each chunk

    vectorizer = TfidfVectorizer(stop_words="english")
    # Create a TF-IDF vectorizer

    tfidf_matrix = vectorizer.fit_transform(texts)
    # Convert all chunks into TF-IDF vectors

    return vectorizer, tfidf_matrix
    # Return the vectorizer and the TF-IDF matrix


def retrieve(query, chunks, vectorizer, tfidf_matrix, top_k=3):
    # Retrieve the most relevant chunks for the user query

    query_vector = vectorizer.transform([query])
    # Convert the user query into a TF-IDF vector

    similarity_scores = cosine_similarity(query_vector, tfidf_matrix).flatten()
    # Calculate similarity between the query and all chunks

    top_indices = np.argsort(similarity_scores)[-top_k:][::-1]
    # Get indices of the top matching chunks in descending order

    results = []
    # Create an empty list to store retrieval results

    for index in top_indices:
        # Loop through the best matching chunks

        results.append({
            "score": float(similarity_scores[index]),  # Similarity score
            "paper_name": chunks[index]["paper_name"],  # Source paper name
            "page": chunks[index]["page"],  # Source page number
            "text": chunks[index]["text"]  # Retrieved text chunk
        })

    return results
    # Return the top relevant results


if __name__ == "__main__":
    # Run this part only when this file is executed directly

    chunks = load_chunks()
    # Load chunks from the JSON file

    vectorizer, tfidf_matrix = build_tfidf_index(chunks)
    # Build the TF-IDF index

    print("Retriever is ready. Type 'exit' to stop.")
    # Tell the user that the retriever is ready

    while True:
        # Start an infinite loop for asking questions

        query = input("\nAsk a question about the papers: ")
        # Read the user's question

        if query.lower() in ["exit", "quit"]:
            # Check if the user wants to stop

            break
            # Exit the loop

        results = retrieve(query, chunks, vectorizer, tfidf_matrix)
        # Retrieve the top relevant chunks

        for i, result in enumerate(results, start=1):
            # Print each retrieved result

            print(f"\nResult {i}")
            print(f"Score: {result['score']:.4f}")
            print(f"Paper: {result['paper_name']}")
            print(f"Page: {result['page']}")
            print(f"Text: {result['text'][:700]}...")