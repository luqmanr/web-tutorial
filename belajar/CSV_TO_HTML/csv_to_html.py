import csv
from io import StringIO
import urllib.parse

def generate_html_table_from_csv(csv_data: str) -> str:
    """
    Generates a full HTML document displaying CSV data in a styled table.
    The 'Name' column will have clickable links to Google searches.

    Args:
        csv_data: A string containing the CSV content.

    Returns:
        A string containing the complete HTML document.
    """
    # Use StringIO to treat the string as a file for the csv reader
    csv_file = StringIO(csv_data)
    reader = csv.reader(csv_file)

    # Read header row
    try:
        headers = next(reader)
    except StopIteration:
        return "<p>Error: CSV data is empty or malformed (no header row).</p>"

    # Find the index of the 'Name' column for creating links, if applicable
    name_column_index = -1
    try:
        name_column_index = headers.index('Name')
    except ValueError:
        # 'Name' column not found, links won't be created for it
        pass

    # Build the table header (thead)
    thead_html = "<thead>\n<tr>\n"
    for header in headers:
        thead_html += f'<th class="px-6 py-3 bg-gray-50 text-xs font-medium text-gray-500 uppercase tracking-wider">{header}</th>\n'
    thead_html += "</tr>\n</thead>\n"

    # Build the table body (tbody)
    tbody_html = "<tbody>\n"
    for row in reader:
        # Skip empty rows that might result from trailing newlines
        if not any(row):
            continue

        tbody_html += "<tr>\n"
        for i, cell in enumerate(row):
            cell_content = cell
            if i == name_column_index:
                # Encode the name for URL safety
                encoded_name = urllib.parse.quote_plus(cell)
                # Create the clickable link for the Name column
                cell_content = f'<a href="https://google.com/search?q={encoded_name}" target="_blank" class="text-blue-600 hover:text-blue-800 hover:underline focus:outline-none focus:ring-2 focus:ring-blue-500 rounded">{cell}</a>'
            tbody_html += f'<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{cell_content}</td>\n'
        tbody_html += "</tr>\n"
    tbody_html += "</tbody>\n"

    # Construct the full HTML document
    full_html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dynamic CSV Viewer</title>
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        /* Custom styles to ensure rounded corners and Inter font */
        body {{
            font-family: 'Inter', sans-serif;
        }}
        .container {{
            max-width: 90%;
            margin: 0 auto;
        }}
        table {{
            width: 100%;
            border-collapse: separate; /* Allows for rounded borders on cells */
            border-spacing: 0;
            overflow: hidden; /* Ensures rounded corners are applied correctly */
        }}
        th, td {{
            padding: 0.75rem;
            text-align: left;
            border: 1px solid #e2e8f0; /* Tailwind gray-200 */
        }}
        th {{
            background-color: #f8fafc; /* Tailwind gray-50 */
            font-weight: 600;
        }}
        /* Rounded corners for the table and its cells */
        table {{
            border-radius: 0.5rem; /* Tailwind rounded-lg */
        }}
        th:first-child {{
            border-top-left-radius: 0.5rem;
        }}
        th:last-child {{
            border-top-right-radius: 0.5rem;
        }}
        tr:last-child td:first-child {{
            border-bottom-left-radius: 0.5rem;
        }}
        tr:last-child td:last-child {{
            border-bottom-right-radius: 0.5rem;
        }}
        /* Custom scrollbar for table container */
        .table-container::-webkit-scrollbar {{
            height: 8px;
            background-color: #f1f1f1;
            border-radius: 10px;
        }}
        .table-container::-webkit-scrollbar-thumb {{
            background-color: #cbd5e1; /* Tailwind gray-300 */
            border-radius: 10px;
        }}
        .table-container::-webkit-scrollbar-thumb:hover {{
            background-color: #94a3b8; /* Tailwind gray-400 */
        }}
    </style>
</head>
<body class="bg-gray-100 p-6">
    <div class="container bg-white shadow-lg rounded-lg p-8">
        <h1 class="text-3xl font-bold text-gray-800 mb-6 text-center">Dynamic CSV Viewer</h1>

        <!-- CSV Display Area -->
        <div id="csvDisplay">
            <h2 class="text-2xl font-semibold text-gray-700 mb-4">Generated CSV Content:</h2>
            <div class="overflow-x-auto rounded-lg shadow-sm table-container">
                <table id="csvTable" class="min-w-full bg-white border border-gray-200">
                    {thead_html}
                    {tbody_html}
                </table>
            </div>
        </div>
    </div>
</body>
</html>
"""
    return full_html

# Example Usage:
if __name__ == "__main__":
#     sample_csv_data = """Name,Age,City,Occupation
# Alice,30,New York,Engineer
# Bob,24,Los Angeles,Artist
# Charlie,35,Chicago,Doctor
# Diana,28,Houston,Designer
# Eve,32,Miami,Teacher
# Frank,29,Seattle,Developer""" # Added a new row for demonstration

    sample_csv_data = open("random.csv", "r").read()

    generated_html = generate_html_table_from_csv(sample_csv_data)

    # You can save this to an HTML file or print it
    with open("dynamic_csv_table.html", "w") as f:
        f.write(generated_html)
    print("HTML generated and saved to dynamic_csv_table.html")
    # For quick testing, you can also print the HTML directly
    # print(generated_html)
