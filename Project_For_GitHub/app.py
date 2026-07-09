import streamlit as st  # Build web interface

from semantic_retriever import load_chunks, build_embeddings, retrieve
# Import retrieval functions

from memory import add_question
# Save original user question into memory

from personalized_ranker import personalize_results
# Re-rank results using user memory

from gemini_query_rewriter import rewrite_query_with_history
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

if "messages" not in st.session_state:
    # Create chat history if it does not exist

    st.session_state.messages = []
    # Store conversation messages


for message in st.session_state.messages:
    # Display previous chat messages

    with st.chat_message(message["role"]):
        st.write(message["content"])


query = st.chat_input("Ask a question about the papers...")
# User question input as chat


if query:
    # Run when user sends a message

    previous_messages = st.session_state.messages.copy()
    # Save previous conversation before adding the new question

    st.session_state.messages.append({
        "role": "user",
        "content": query
    })
    # Save user message in chat history

    with st.chat_message("user"):
        st.write(query)
        # Display user message

    with st.chat_message("assistant"):
        # Display assistant response

        with st.spinner("Rewriting query using conversation history..."):
            rewritten_query = rewrite_query_with_history(
                query,
                previous_messages
            )
            # Rewrite query using only previous conversation history

        st.subheader("Query Rewriting")
        st.write("**Original Query:**", query)
        st.write("**Rewritten Query:**", rewritten_query)

        with st.spinner("Retrieving relevant passages..."):
            results = retrieve(rewritten_query, chunks, model, embeddings)
            # Retrieve relevant chunks using rewritten standalone query

            add_question(query)
            # Save original question in memory

            personalized_results = personalize_results(results, model)
            # Apply memory-based personalization

        top_results_for_answer = personalized_results[:3]
        # Use top 3 results for answer generation

        with st.spinner("Generating answer..."):
            final_answer = generate_answer_with_gemini(
                rewritten_query,
                top_results_for_answer
            )
            # Generate answer using the standalone rewritten query

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

        assistant_message = f"""
Final Answer:
{final_answer}

Sources:
{', '.join([result['paper_name'] + ' page ' + str(result['page']) for result in top_results_for_answer])}
"""
        # Create assistant message for chat history

        st.session_state.messages.append({
            "role": "assistant",
            "content": assistant_message
        })
        # Save assistant response in chat history
