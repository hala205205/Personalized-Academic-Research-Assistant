from sklearn.metrics.pairwise import cosine_similarity  # Calculate similarity between embeddings
from memory import get_memory_text  # Get user memory as text


def personalize_results(results, model, max_bonus=0.15):
    # Re-rank retrieved results using semantic similarity with user memory

    memory_text = get_memory_text()
    # Convert user memory into one text string

    memory_embedding = model.encode([memory_text])
    # Convert memory text into an embedding vector

    personalized_results = []
    # Create a list to store updated results

    for result in results:
        # Loop through each retrieved result

        chunk_text = result["text"]
        # Get the retrieved chunk text

        chunk_embedding = model.encode([chunk_text])
        # Convert chunk text into an embedding vector

        memory_similarity = cosine_similarity(memory_embedding, chunk_embedding)[0][0]
        # Calculate semantic similarity between memory and chunk

        memory_bonus = float(memory_similarity) * max_bonus
        # Convert memory similarity into a small bonus

        semantic_score = result["score"]
        # Get original semantic retrieval score

        final_score = semantic_score + memory_bonus
        # Combine original score with memory bonus

        updated_result = result.copy()
        # Copy original result

        updated_result["semantic_score"] = semantic_score
        # Store original semantic score

        updated_result["memory_similarity"] = float(memory_similarity)
        # Store memory similarity

        updated_result["memory_bonus"] = memory_bonus
        # Store memory bonus

        updated_result["final_score"] = final_score
        # Store final personalized score

        personalized_results.append(updated_result)
        # Add updated result to list

    personalized_results = sorted(
        personalized_results,
        key=lambda x: x["final_score"],
        reverse=True
    )
    # Sort results by final personalized score

    return personalized_results
    # Return personalized ranked results