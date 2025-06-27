# html_generator.py

# This script demonstrates how to use Python's f-strings
# to dynamically create content and generate a static HTML file.

import os

def generate_static_html(name: str, favorite_language: str, year: int) -> str:
    """
    Generates a simple HTML string using f-strings, embedding dynamic data.

    Args:
        name (str): A name to display in the HTML.
        favorite_language (str): A programming language.
        year (int): A year.

    Returns:
        str: A complete HTML document as a string.
    """
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Personalized Greeting</title>
    <!-- Tailwind CSS CDN for basic styling -->
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body {{
            font-family: 'Inter', sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            background-color: #f3f4f6; /* Tailwind gray-100 */
        }}
        .card {{
            background-color: #ffffff;
            padding: 2.5rem; /* p-10 */
            border-radius: 0.75rem; /* rounded-xl */
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05); /* shadow-xl */
            text-align: center;
            max-width: 500px;
            width: 90%;
        }}
        h1 {{
            font-size: 2.25rem; /* text-4xl */
            font-weight: 700; /* font-bold */
            color: #1f2937; /* text-gray-900 */
            margin-bottom: 1.5rem; /* mb-6 */
        }}
        p {{
            font-size: 1.125rem; /* text-lg */
            color: #4b5563; /* text-gray-700 */
            line-height: 1.75rem; /* leading-relaxed */
        }}
        .highlight {{
            color: #2563eb; /* text-blue-600 */
            font-weight: 600;
        }}
    </style>
</head>
<body>
    <div class="card">
        <h1>Welcome, <span class="highlight">{name}</span>!</h1>
        <p>
            We're glad to have you here in <span class="highlight">{year}</span>.
            You've chosen <span class="highlight">{favorite_language}</span> as your favorite programming language.
            That's a great choice!
        </p>
        <p class="mt-6 text-sm text-gray-500">
            This page was dynamically generated using Python's string formatting.
        </p>
    </div>
</body>
</html>
"""
    return html_content

# --- Example Usage ---
if __name__ == "__main__":
    # Define some dynamic data
    user_name = "Jane Doe"
    lang = "Python"
    current_year = 2025

    # Generate the HTML content
    html_output = generate_static_html(user_name, lang, current_year)

    # Define the output file path
    output_filename = "greeting_page.html"

    # Write the HTML content to a static file
    try:
        with open(output_filename, "w", encoding="utf-8") as file:
            file.write(html_output)
        print(f"Successfully generated '{output_filename}' in the current directory.")
        print(f"You can open '{output_filename}' in your web browser.")
    except IOError as e:
        print(f"Error writing to file '{output_filename}': {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    # You can also print the HTML to the console for verification
    # print("\n--- Generated HTML Content ---")
    # print(html_output)
