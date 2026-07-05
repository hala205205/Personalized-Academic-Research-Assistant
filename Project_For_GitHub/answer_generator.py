import os  # Used to read environment variables
from dotenv import load_dotenv  # Load environment variables from .env file
from google import genai  # Google GenAI SDK
from google.genai import errors  # Handle Gemini API errors

load_dotenv()
# Load variables from .env file


def generate_answer_with_gemini(original_query, retrieved_results):
    # Generate an academic answer using only the retrieved passages

    api_key = os.getenv("GEMINI_API_KEY")
    # Read Gemini API key from environment variables

    if not api_key:
        # Check if API key is missing

        raise ValueError("GEMINI_API_KEY is not set. Please set it in PowerShell first.")
        # Stop the program if API key is missing

    client = genai.Client(api_key=api_key)
    # Create Gemini client

    context_parts = []
    # Create a list to store retrieved passages as context

    for i, result in enumerate(retrieved_results, start=1):
        # Loop through retrieved results

        passage = f"""
Source {i}
Paper: {result['paper_name']}
Page: {result['page']}
Text:
{result['text']}
"""
        # Format each passage with source information

        context_parts.append(passage)
        # Add passage to context list

    retrieved_context = "\n\n".join(context_parts)
    # Combine all retrieved passages into one context string

    prompt = f"""
You are an academic research assistant.

Your task:
Answer the user's question using ONLY the retrieved passages below.

Rules:
- Do not use outside knowledge.
- Use the retrieved passages even if they are partially relevant.
- If the passages contain related challenges, limitations, evaluation issues, retrieval issues, or future research directions, synthesize them into an answer.
- Only say that the passages do not provide enough information if they are completely unrelated to the question.
- Answer only the user's question.
- Do not add unrelated details.
- Write a clear academic answer.
- Keep the answer concise but informative.
- Mention the sources using paper name and page number.
- Do not invent citations.
- Do not mention sources that are not listed.

User question:
{original_query}

Retrieved passages:
{retrieved_context}

Answer:
"""
    # Build a grounded generation prompt

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt
        )
        # Send prompt to Gemini

        answer = response.text.strip()
        # Extract answer text

    except errors.ServerError:
        answer = "Gemini is temporarily unavailable. Please try again later."
        # Handle temporary Gemini server errors

    except Exception as e:
        answer = f"Answer generation failed: {e}"
        # Handle any other error

    return answer
    # Return generated answer
