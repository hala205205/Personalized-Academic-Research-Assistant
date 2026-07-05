import os    # Import os to work with folders and file paths
import json  # Import json to save the extracted chunks into a JSON file
import fitz  # Import PyMuPDF library to read PDF files


PAPERS_DIR = "papers"  # Define the folder that contains the PDF papers
OUTPUT_FILE = "data/chunks.json"  # Define the output file where chunks will be saved


def extract_text_from_pdf(pdf_path):
    # This function extracts text from one PDF file

    document = fitz.open(pdf_path)  # Open the PDF file using PyMuPDF

    pages_text = []  # Create an empty list to store text from each page

    for page_number, page in enumerate(document, start=1):
        # Loop through each page in the PDF, starting page numbers from 1

        text = page.get_text()  # Extract text from the current page

        if text.strip():
            # Check if the extracted text is not empty

            pages_text.append({
                "page": page_number,  # Store the page number
                "text": text  # Store the text extracted from this page
            })

    document.close()  # Close the PDF file after reading it

    return pages_text  # Return the list of pages with their extracted text


def split_text_into_chunks(text, chunk_size=800, overlap=150):
    # This function splits long text into smaller overlapping chunks

    words = text.split()  # Split the text into a list of words

    chunks = []  # Create an empty list to store the chunks

    start = 0  # Start from the first word

    while start < len(words):
        # Continue splitting until we reach the end of the word list

        end = start + chunk_size  # Define the ending index of the current chunk

        chunk = " ".join(words[start:end])  # Join selected words into one text chunk

        chunks.append(chunk)  # Add the chunk to the chunks list

        start += chunk_size - overlap  # Move forward while keeping overlap with previous chunk

    return chunks  # Return the list of chunks


def process_pdfs():
    # This function processes all PDF files inside the papers folder

    all_chunks = []  # Create an empty list to store chunks from all papers

    for filename in os.listdir(PAPERS_DIR):
        # Loop through all files inside the papers folder

        if filename.endswith(".pdf"):
            # Process only files that end with .pdf

            pdf_path = os.path.join(PAPERS_DIR, filename)
            # Create the full path of the current PDF file

            print(f"Processing: {filename}")
            # Print the name of the PDF currently being processed

            pages = extract_text_from_pdf(pdf_path)
            # Extract text from all pages of the current PDF

            for page in pages:
                # Loop through each extracted page

                chunks = split_text_into_chunks(page["text"])
                # Split the page text into smaller chunks

                for i, chunk in enumerate(chunks):
                    # Loop through all chunks created from this page

                    all_chunks.append({
                        "paper_name": filename,  # Store the source paper name
                        "page": page["page"],  # Store the page number
                        "chunk_id": f"{filename}_p{page['page']}_c{i}",  # Create a unique chunk ID
                        "text": chunk  # Store the actual text of the chunk
                    })

    os.makedirs("data", exist_ok=True)
    # Create the data folder if it does not already exist

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        # Open the output JSON file for writing

        json.dump(all_chunks, f, ensure_ascii=False, indent=2)
        # Save all chunks into the JSON file in a readable format

    print(f"\nDone. Total chunks: {len(all_chunks)}")
    # Print the total number of chunks created

    print(f"Saved to: {OUTPUT_FILE}")
    # Print the location of the saved output file


if __name__ == "__main__":
    # This line means: run the following code only when this file is executed directly

    process_pdfs()
    # Start processing all PDFs