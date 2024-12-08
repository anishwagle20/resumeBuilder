import json
import os
import subprocess

def replace_placeholders(template, data):
    def format_list(items):
        """Format a list as LaTeX itemized list."""
        formatted = "\n".join(
            f"\\item {item}" if isinstance(item, str) else 
            f"\\item {item['role']} at {item['company']} ({item['duration']}): {item['description']}"
            for item in items
        )
        return f"\\begin{{itemize}}\n{formatted}\n\\end{{itemize}}"

    for key, value in data.items():
        if isinstance(value, list):
            value = format_list(value)
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
