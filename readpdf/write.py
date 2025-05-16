from fpdf import FPDF

# Your Markdown content
markdown_text = """
Bandung, 10 May 2025

Invoice 909812323

| No. | Deskripsi |  Nilai |
| --- | -- | -- |
| 1. | Printer | 300.000 |
| 2. | Kertas  | 70.000 |

PT Borma
"""

# Create FPDF object
# Portrait mode, mm units, A4 format
pdf = FPDF('P', 'mm', 'A4')

# Add a page
pdf.add_page()

# Set auto page break
pdf.set_auto_page_break(auto=True, margin=15)

# Set font
pdf.set_font('Helvetica', size=12)

# --- Manually parse and add content ---

lines = markdown_text.strip().split('\n')

table_start_index = -1
# Find the index of the table header separator line (| --- | ...)
for i, line in enumerate(lines):
    if line.strip().startswith('|') and '---' in line:
        table_start_index = i
        break

# --- Add content before the table ---
if table_start_index != -1:
    for i in range(table_start_index - 1): # Process lines before header row
        # Add text line by line
        pdf.cell(0, 10, lines[i].strip(), 0, 1) # Width=0 means full width, Height=10, Border=0, Ln=1 (move to next line)
else:
    # If no table found, process all lines as paragraphs
    for line in lines:
         pdf.cell(0, 10, line.strip(), 0, 1)


# --- Add the table ---
if table_start_index != -1:
    # Extract header and data rows
    header_line = lines[table_start_index - 1].strip('|')
    headers = [h.strip() for h in header_line.split('|')]

    data_rows = []
    for i in range(table_start_index + 1, len(lines)):
        line = lines[i].strip()
        if line.startswith('|'):
            data_rows.append([d.strip() for d in line.strip('|').split('|')])
        else:
            # Stop processing table rows if a line doesn't start with |
            # and is not empty
            if line: # Only break if it's not just an empty line
                # Process lines after the table block starts but before PT Borma if any
                # This handles cases where there are empty lines between table and final text
                break
            # If it's an empty line, just continue past it
            continue

    # --- Define column widths ---
    # You need to define widths manually as fpdf2 doesn't automatically calculate them from content
    # These are approximate widths in mm. Adjust as needed for your content and page size.
    # Total available width for content on A4 with default 10mm margins is approx 190mm.
    col_widths = [20, 100, 40] # [No., Deskripsi, Nilai] - Total 160mm

    # --- Table Header ---
    pdf.set_fill_color(230, 230, 230) # Light gray background
    pdf.set_font('Helvetica', style='B', size=12) # Bold font for header

    # Draw header row
    for i, header in enumerate(headers):
        # Cell(width, height, text, border, ln, align, fill)
        pdf.cell(col_widths[i], 10, header, 1, 0, 'C', 1) # Border=1, Ln=0 (next cell on same line), Align=Center, Fill=1
    pdf.ln() # Move to the next line after the header row

    # --- Table Data ---
    pdf.set_fill_color(255, 255, 255) # White background
    pdf.set_font('Helvetica', style='', size=12) # Regular font for data

    # Draw data rows
    for row in data_rows:
        # Ensure we have enough cell data for the defined columns
        row_cells = row[:len(col_widths)] + [''] * (len(col_widths) - len(row)) # Pad with empty strings if row is short

        # Cell(width, height, text, border, ln, align, fill)
        pdf.cell(col_widths[0], 10, row_cells[0], 1, 0, 'L', 0) # No. - Left align, No fill
        pdf.cell(col_widths[1], 10, row_cells[1], 1, 0, 'L', 0) # Deskripsi - Left align
        pdf.cell(col_widths[2], 10, row_cells[2], 1, 0, 'R', 0) # Nilai - Right align

        pdf.ln() # Move to the next line after each data row

    # # --- Add content after the table ---
    # # Find the first line after the last table data row processed
    # post_table_content_start_index = table_start_index + 1 + len(data_rows) + 1 # +1 for header line, +len(data_rows) for data, +1 for separator line

    # # Adjust start index if there were non-| lines immediately after the table data
    # if i < len(lines) and not lines[i].strip().startswith('|') and lines[i].strip():
    #      post_table_content_start_index = i


    # for i in range(post_table_content_start_index, len(lines)):
    #     pdf.cell(0, 10, lines[i].strip(), 0, 1)


# Output the PDF
output_filename = "invoice_fpdf2.pdf"
pdf.output(output_filename)

print(f"Successfully created {output_filename} using fpdf2.")
print("Note: Table column widths were manually set and might need adjustment.")