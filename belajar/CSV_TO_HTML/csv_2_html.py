def if_budi(input):
    if input == 'Budi':
        return 'iduB'
    return input

def csv_to_html(csv_string):
    """
    Converts a CSV string to an HTML table string.

    Args:
        csv_string: A string containing CSV data.

    Returns:
        A string containing the HTML table, or an error message if the input is invalid.
    """

    # lines = [x for x in csv_string.strip().split('\n') if len(x) > 1]
    lines_ori = csv_string.strip().split('\n')
    lines = []
    # kalau line kosong, jangan dimasukkan ke variable lines
    for line in lines_ori:
        if len(line) == 0:
            continue
        lines.append(line)

    # print(lines)
    # print(len(lines))
    if not lines:
        return "<p>Error: Empty CSV input.</p>"

    # 1. Extract row headers (first line)
    headers = [h.strip() for h in lines[0].split(',')]

    html_output = """
<!DOCTYPE html>
<head>
<link rel="stylesheet" href="style.css">
</head>\n
    """
    html_output += "<table>\n"
    # html_output += "<thead style='font-style:bold;font-family:\"Serif\";color:red;background-color:rgba(20,20,20,255);'>\n"
    html_output += "<thead class=\"header\">\n"
    html_output += "<tr>\n"

    # 2. Generate <th> tags for each header
    for header in headers:
        html_output += f"<th>{header}</th>\n"
    html_output += "</tr>\n"
    html_output += "</thead>\n"
    html_output += "<tbody>\n"

    # Process data rows (starting from the second line)
    for line in lines[1:]:
        if len(line) == 0:
            continue

        values = [v.strip() for v in line.split(',')]
        if len(values) != len(headers):
            return f"<p>Error: Mismatched column count in row: {line}</p>"

        # example: values[0] = 'Budi' => '<a href="https://google.com?search=Budi">Budi</a>'
        values[0] = f'<a href="https://google.com/search?tbm=isch&q={values[0]}">{values[0]}</a>'

        # 3. Generate <tr> and <td> tags for each row's values
        html_output += "<tr>\n"
        for value in values:
            html_output += f"<td>{value}</td>\n"
        html_output += "</tr>\n"

    html_output += "</tbody>\n"
    html_output += "</table>"

    return html_output

# Example Usage:
# csv_data = """
# Name,Age,City
# Alice,30,New York
# Bob,24,Los Angeles
# Charlie,35,
# Diana,28,Houston
# Eve,32,Miami
# ,,
# """
csv_data = open('data.csv', 'r').read()

html_output = csv_to_html(csv_data)
with open('html_output.html', 'w') as f:
    f.write(html_output)
    f.close()

# Example with different data
csv_data_2 = """
Product,Price,Quantity
Laptop,1200,10
Mouse,25,50
Keyboard,75,20
"""

html_output_2 = csv_to_html(csv_data_2)
with open('html_output_2.html', 'w') as f:
    f.write(html_output_2)
    f.close()

# Example with missing column in a row (will return an error)
csv_data_error = """
Name,col1,col2
budi,A,B
luqman,C
"""
html_output_error = csv_to_html(csv_data_error)
with open('html_output_error.html', 'w') as f:
    f.write(html_output_error)
    f.close()

# Example with empty CSV
csv_data_empty = ""
html_output_empty = csv_to_html(csv_data_empty)
with open('html_output_empty.html', 'w') as f:
    f.write(html_output_empty)
    f.close()