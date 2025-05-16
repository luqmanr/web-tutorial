from pypdf import PdfReader

def get_text_from_pdf(pdf_path):
    """
    Extracts text from each page of a PDF file.

    Args:
        pdf_path (str): The path to the PDF file.

    Returns:
        list: A list where each element is a string containing the text
              from a page. Returns an empty list if an error occurs.
    """
    all_text = []
    try:
        # Open the PDF file
        reader = PdfReader(pdf_path)

        # Get the number of pages
        number_of_pages = len(reader.pages)
        print(f"Reading {number_of_pages} pages from {pdf_path}")

        # Iterate through each page and extract text
        for page_number in range(number_of_pages):
            page = reader.pages[page_number]
            text = page.extract_text()
            if text: # Add text only if extraction was successful and not empty
                all_text.append(text)
            else:
                all_text.append(f"Could not extract text from page {page_number + 1}") # Indicate if extraction failed for a page

    except FileNotFoundError:
        print(f"Error: The file '{pdf_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

    return all_text

# --- How to use the function ---
pdf_file_path = "contoh1.pdf"  # Replace with the path to your PDF file
extracted_texts = get_text_from_pdf(pdf_file_path)

# You can now process the extracted_texts list
if extracted_texts:
    for i, page_text in enumerate(extracted_texts):
        print(f"--- Text from Page {i + 1} ---")
        print(page_text)
        print("-" * 20) # Separator
        