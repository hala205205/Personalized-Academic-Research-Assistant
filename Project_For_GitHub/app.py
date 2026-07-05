import streamlit as st  # Build web interface

from semantic_retriever import load_chunks, build_embeddings, retrieve
# Import retrieval functions

from memory import add_question
# Save original user question into memory

from personalized_ranker import personalize_results
# Re-rank results using user memory

from gemini_query_rewriter import rewrite_query_with_gemini
# Rewrite query using Gemini

from answer_generator import generate_answer_with_gemini
# Generate final grounded answer


st.set_page_config(
    page_title="Personalized Academic Research Assistant",
    page_icon="📚",
    layout="wide"
)
# Configure Streamlit page


st.title("📚 Personalized Academic Research Assistant")
st.write("Ask questions about your academic papers using semantic retrieval, user memory, and Gemini-based answer generation.")


@st.cache_resource
def load_system():
    # Load chunks, model, and embeddings only once

    chunks = load_chunks()
    # Load extracted paper chunks

    model, embeddings = build_embeddings(chunks)
    # Load embedding model and create embeddings

    return chunks, model, embeddings
    # Return system components


chunks, model, embeddings = load_system()
# Initialize system


query = st.text_input("Ask a question about the papers:")
# User question input


if st.button("Ask"):
    # Run when user clicks Ask

    if not query.strip():
        # Check if question is empty

        st.warning("Please enter a question.")
        # Show warning

    else:
        # If user entered a question

        with st.spinner("Rewriting query using Gemini..."):
            rewritten_query = rewrite_query_with_gemini(query)
            # Rewrite query using Gemini

        st.subheader("Query Rewriting")
        st.write("**Original Query:**", query)
        st.write("**Rewritten Query:**", rewritten_query)

        with st.spinner("Retrieving relevant passages..."):
            results = retrieve(rewritten_query, chunks, model, embeddings)
            # Retrieve relevant chunks

            add_question(query)
            # Save original question in memory

            personalized_results = personalize_results(results, model)
            # Apply memory-based personalization

        top_results_for_answer = personalized_results[:3]
        # Use top 3 results for answer generation

        with st.spinner("Generating answer..."):
            final_answer = generate_answer_with_gemini(query, top_results_for_answer)
            # Generate answer from retrieved passages

        st.subheader("Final Answer")
        st.write(final_answer)

        st.subheader("Sources Used")
        for i, result in enumerate(top_results_for_answer, start=1):
            st.write(f"{i}. **{result['paper_name']}** - Page {result['page']}")

        st.subheader("Retrieved Passages and Scores")

        for i, result in enumerate(personalized_results, start=1):
            with st.expander(f"Result {i}: {result['paper_name']} - Page {result['page']}"):
                st.write(f"**Semantic Score:** {result['semantic_score']:.4f}")
                st.write(f"**Memory Similarity:** {result['memory_similarity']:.4f}")
                st.write(f"**Memory Bonus:** {result['memory_bonus']:.4f}")
                st.write(f"**Final Score:** {result['final_score']:.4f}")
                st.write("**Passage:**")
                st.write(result["text"])