import os  # Used to read environment variables
from dotenv import load_dotenv  # Load environment variables from .env file
from google import genai  # Google GenAI SDK
from google.genai import errors  # Handle Gemini API errors

load_dotenv()
# Load variables from .env file

def rewrite_query_with_gemini(user_query):
    # Rewrite the user query using Gemini without answering it

    api_key = os.getenv("GEMINI_API_KEY")
    # Read the Gemini API key from environment variables

    if not api_key:
        # Check if the API key is missing

        raise ValueError("GEMINI_API_KEY is not set. Please set it in PowerShell first.")
        # Stop the program and show a clear error message

    client = genai.Client(api_key=api_key)
    # Create a Gemini client using the API key

    prompt = f"""
You are a query rewriting module for an academic paper retrieval system.

Rewrite the user's query into a detailed academic search query for retrieving relevant passages from research papers.

Rules:
- Do NOT answer the question.
- Keep the original meaning.
- Expand abbreviations when needed.
- Add academic terms that help retrieval.
- Make the query specific and informative.
- The rewritten query should be one clear sentence.
- Return only the rewritten query.
- Do not add explanations.

Examples:

User query: What is RAG?
Rewritten query: Find passages that define Retrieval-Augmented Generation, explain its main concept, and describe its retrieval and generation workflow.

User query: What are the limitations of RAG?
Rewritten query: Find passages discussing the main limitations and challenges of Retrieval-Augmented Generation systems, including retrieval quality, context integration, faithfulness, evaluation, and robustness.

User query: How does memory improve RAG?
Rewritten query: Find passages explaining how memory mechanisms improve Retrieval-Augmented Generation systems through long-context modeling, personalized retrieval, and better use of previous information.

User query:
{user_query}
"""
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt
        )
        # Send the prompt to Gemini and get the rewritten query

        rewritten_query = response.text.strip()
        # Try to read Gemini response text

    except errors.ServerError:
        print("Gemini is temporarily unavailable. Using original query instead.")
        rewritten_query = user_query
        # If Gemini server is busy, use original query

    except Exception as e:
        print(f"Gemini rewriting failed: {e}")
        print("Using original query instead.")
        rewritten_query = user_query
        # If any other error happens, use original query

    if not rewritten_query or rewritten_query.lower() == "none":
        rewritten_query = user_query
        # If Gemini returns empty or None, use original query

    return rewritten_query
    # Return the rewritten query
    
def rewrite_query_with_history(user_query, chat_history):
    # Rewrite the user query using recent conversation history

    api_key = os.getenv("GEMINI_API_KEY")
    # Read the Gemini API key from environment variables

    if not api_key:
        # Check if the API key is missing
        raise ValueError("GEMINI_API_KEY is not set. Please set it first.")

    client = genai.Client(api_key=api_key)
    # Create a Gemini client

    recent_history = chat_history[-4:]
    # Use only the last 4 messages to keep the prompt short

    history_text = ""
    # Prepare conversation history text

    for message in recent_history:
        # Loop through recent chat messages

        role = message["role"]
        # Get message role: user or assistant

        content = message["content"]
        # Get message content

        history_text += f"{role}: {content}\n"
        # Add message to history text

    prompt = f"""
You are a conversational query rewriting module for an academic paper retrieval system.

Your task:
Rewrite the user's latest query into a clear standalone academic search query.

Rules:
- Do NOT answer the question.
- Use the conversation history only to resolve pronouns and missing context.
- Keep the user's original meaning.
- Expand abbreviations when needed.
- Make the query useful for retrieving relevant passages from research papers.
- Return only the rewritten query.
- Do not add explanations.

Conversation history:
{history_text}

Latest user query:
{user_query}
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt
        )
        # Send prompt to Gemini

        rewritten_query = response.text.strip()
        # Extract rewritten query

    except errors.ServerError:
        print("Gemini is temporarily unavailable. Using original query instead.")
        rewritten_query = user_query
        # Fallback to original query

    except Exception as e:
        print(f"Conversational rewriting failed: {e}")
        rewritten_query = user_query
        # Fallback to original query

    if not rewritten_query or rewritten_query.lower() == "none":
        rewritten_query = user_query
        # If Gemini returns empty response, use original query

    return rewritten_query
    # Return rewritten query    
    

if __name__ == "__main__":
    # Run this part only when testing the file directly

    while True:
        # Keep asking for queries

        query = input("\nEnter a query: ")
        # Read user query

        if query.lower() in ["exit", "quit"]:
            # Stop the program if user types exit or quit

            break
            # Exit loop

        rewritten = rewrite_query_with_gemini(query)
        # Rewrite the query using Gemini

        print("\nOriginal Query:")
        print(query)

        print("\nRewritten Query:")
        print(rewritten)
