import os  # Used to work with folders and file paths
import json  # Used to read and write JSON files
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
MEMORY_FILE = BASE_DIR / "data" / "memory.json"


DEFAULT_MEMORY = {
    # Default memory structure if memory file does not exist

    "research_interests": [
        "memory-based RAG",
        "scientific literature chatbots",
        "personalized retrieval"
    ],
    # A list of the user's research interests

    "previous_questions": [],
    # A list to store the user's previous questions

    "current_focus": "personalized academic research assistant"
    # The current research focus of the user
}


def create_memory_if_not_exists():
    # Create memory file if it does not already exist

    os.makedirs("data", exist_ok=True)
    # Create the data folder if it does not exist

    if not os.path.exists(MEMORY_FILE):
        # Check if memory.json does not exist

        with open(MEMORY_FILE, "w", encoding="utf-8") as file:
            # Open memory.json in write mode

            json.dump(DEFAULT_MEMORY, file, ensure_ascii=False, indent=2)
            # Save the default memory structure into the file


def load_memory():
    # Load user memory from memory.json

    create_memory_if_not_exists()
    # Make sure memory file exists before reading it

    with open(MEMORY_FILE, "r", encoding="utf-8") as file:
        # Open memory.json in read mode

        memory = json.load(file)
        # Convert JSON content into a Python dictionary

    return memory
    # Return the loaded memory


def save_memory(memory):
    # Save updated memory back to memory.json

    with open(MEMORY_FILE, "w", encoding="utf-8") as file:
        # Open memory.json in write mode

        json.dump(memory, file, ensure_ascii=False, indent=2)
        # Save memory dictionary as formatted JSON


def add_question(question):
    # Add a new user question to previous_questions

    memory = load_memory()
    # Load current memory

    memory["previous_questions"].append(question)
    # Add the new question to the list

    save_memory(memory)
    # Save the updated memory


def add_interest(interest):
    # Add a new research interest to memory

    memory = load_memory()
    # Load current memory

    if interest not in memory["research_interests"]:
        # Avoid adding duplicate interests

        memory["research_interests"].append(interest)
        # Add new interest

    save_memory(memory)
    # Save the updated memory


def get_memory_text():
    # Convert memory into a simple text format for retrieval or ranking

    memory = load_memory()
    # Load current memory

    interests = ", ".join(memory["research_interests"])
    # Convert interests list into one text string

    previous_questions = " | ".join(memory["previous_questions"][-5:])
    # Keep only the last 5 questions to avoid very long memory text

    current_focus = memory["current_focus"]
    # Get current research focus

    memory_text = f"Research interests: {interests}. Current focus: {current_focus}. Previous questions: {previous_questions}"
    # Combine memory fields into one text string

    return memory_text
    # Return memory as text


if __name__ == "__main__":
    # Run this part only when testing memory.py directly

    create_memory_if_not_exists()
    # Create memory file if needed

    print("Memory loaded successfully.")
    # Print success message

    print("\nCurrent Memory:")
    # Print title

    print(json.dumps(load_memory(), ensure_ascii=False, indent=2))
    # Print current memory content

    test_question = input("\nEnter a test question to save: ")
    # Ask user to enter a test question

    add_question(test_question)
    # Save the question into memory

    print("\nUpdated Memory:")
    # Print title

    print(json.dumps(load_memory(), ensure_ascii=False, indent=2))
    # Print updated memory
