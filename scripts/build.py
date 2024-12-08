import json
import os
import subprocess


def load_data(json_file):
    with open(json_file, 'r') as f:
        return json.load(f)


def format_list(values):
    """Format a list into LaTeX itemize format."""
    return "\n".join([f"\\item {item}" for item in values])


def format_projects(values):
    """Format projects for LaTeX."""
    formatted = []
    for project in values:
        details = "\n".join([f"- {key.capitalize()}: {value}" for key, value in project.items()])
        formatted.append(f"\\textbf{{{project['title']}}} \\\\ {details}")
    return "\n\n".join(formatted)


def replace_placeholders(template, data):
    def format_list(items):
        """Format a list as LaTeX itemized list."""
        formatted = "\n".join(
            f"\\item {item}" if isinstance(item, str) else 
            f"\\item {item['role']} at {item['company']} ({item['duration']}): {item['description']}"
            for item in items
        )
        return f"\\begin{{itemize}}\n{formatted}\n\\end{{itemize}}"

    def format_dict(dictionary):
        """Format a dictionary as LaTeX key-value pairs."""
        return "\n".join(f"\\textbf{{{key}}}: {value}" for key, value in dictionary.items())

    for key, value in data.items():
        if isinstance(value, list):
            value = format_list(value)
        elif isinstance(value, dict):
            value = format_dict(value)
        template = template.replace(f"{{{{ {key} }}}}", value)
    return template



def build_resume(template_file, data, output_file):
    """Generate a resume PDF from a LaTeX template."""
    with open(template_file, 'r') as f:
        template = f.read()

    filled_template = replace_placeholders(template, data)

    # Temporary files for processing
    temp_tex = "temp.tex"
    build_dir = "builds"

    os.makedirs(build_dir, exist_ok=True)

    with open(temp_tex, 'w') as f:
        f.write(filled_template)

    try:
        # Compile LaTeX file
        subprocess.run(['pdflatex', temp_tex, '-output-directory', build_dir], check=True)

        # Move the generated PDF to the output file
        generated_pdf = os.path.join(build_dir, os.path.splitext(temp_tex)[0] + ".pdf")
        os.rename(generated_pdf, output_file)
    finally:
        # Cleanup temporary files
        if os.path.exists(temp_tex):
            os.remove(temp_tex)


def main():
    data = load_data('data.json')
    templates_dir = 'templates'
    build_dir = 'builds'

    os.makedirs(build_dir, exist_ok=True)

    for template in os.listdir(templates_dir):
        if template.endswith('.tex'):
            output_file = os.path.join(build_dir, f"{os.path.splitext(template)[0]}.pdf")
            build_resume(os.path.join(templates_dir, template), data, output_file)


if __name__ == "__main__":
    main()
