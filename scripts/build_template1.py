import json
import os
import subprocess

def escape_latex(value):
    """
    Escape special LaTeX characters in a string.
    """
    return (value
            .replace("&", "\\&")
            .replace("%", "\\%")
            .replace("$", "\\$")
            .replace("#", "\\#")
            .replace("_", "\\_")
            .replace("{", "\\{")
            .replace("}", "\\}")
            .replace("~", "\\textasciitilde{}")
            .replace("^", "\\textasciicircum{}")
            )

def format_list(items, key_mappings=None):
    """
    Format a list as LaTeX \itemize content.
    If items are dictionaries, map keys using `key_mappings`.
    """
    formatted = []
    for item in items:
        if isinstance(item, dict):
            formatted_item = ", ".join(
                f"{key_mappings[k]}: {escape_latex(str(v))}"
                for k, v in item.items() if k in key_mappings
            )
            formatted.append(f"\\item {formatted_item}")
        else:
            formatted.append(f"\\item {escape_latex(str(item))}")
    return "\n".join(formatted)

def replace_placeholders(template, data):
    """
    Replace placeholders in the LaTeX template with content from the data.
    """
    key_mappings = {
        "role": "Role",
        "company": "Company",
        "duration": "Duration",
        "description": "Description",
        "degree": "Degree",
        "institution": "Institution",
        "details": "Details"
    }
    
    for key, value in data.items():
        if isinstance(value, list):
            # Format as LaTeX itemized list
            value = format_list(value, key_mappings)
        elif isinstance(value, dict):
            # Process dictionary fields
            value = format_list([value], key_mappings)
        else:
            # Escape LaTeX for plain strings
            value = escape_latex(str(value))
        template = template.replace(f"{{{{ {key} }}}}", value)
    return template

def build_resume():
    # Paths
    template_path = os.path.join("templates", "template1.tex")
    data_file = "data.json"
    output_pdf = "resume_template1.pdf"

    # Read LaTeX template
    with open(template_path, 'r') as template_file:
        template = template_file.read()

    # Load JSON data
    with open(data_file, 'r') as file:
        data = json.load(file)

    # Replace placeholders
    populated_template = replace_placeholders(template, data)

    # Save the populated LaTeX template to a temporary file
    temp_tex = 'temp_template1.tex'
    with open(temp_tex, 'w') as tex_file:
        tex_file.write(populated_template)

    # Build the PDF using pdflatex
    build_dir = "builds"
    os.makedirs(build_dir, exist_ok=True)

    try:
        subprocess.run(['pdflatex', temp_tex, '-output-directory', build_dir], check=True)
        print(f"PDF successfully generated: {os.path.join(build_dir, output_pdf)}")
    except subprocess.CalledProcessError as e:
        print("Error during PDF generation:", e)
    finally:
        # Clean up temporary files
        for ext in ['aux', 'log', 'out', 'tex']:
            temp_file = f"temp_template1.{ext}"
            if os.path.exists(temp_file):
                os.remove(temp_file)

if __name__ == "__main__":
    build_resume()
