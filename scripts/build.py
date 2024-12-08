import json
import os
import subprocess

def load_data(json_file):
    with open(json_file, 'r') as f:
        return json.load(f)

def replace_placeholders(template, data):
    for key, value in data.items():
        if isinstance(value, list):
            value = "\n".join(
                f"- {item['role']} at {item['company']} ({item['duration']}): {item['description']}"
                if isinstance(item, dict) and 'role' in item else f"- {item}"
                for item in value
            )
        elif isinstance(value, dict):
            value = "\n".join(f"{sub_key}: {sub_value}" for sub_key, sub_value in value.items())
        template = template.replace(f"{{{{ {key} }}}}", str(value))
    return template

def build_resume(template_file, data, output_file):
    with open(template_file, 'r') as f:
        template = f.read()

    filled_template = replace_placeholders(template, data)

    # Temporary file for processing
    temp_tex = "temp.tex"
    temp_pdf = "temp.pdf"
    build_dir = "build"

    os.makedirs(build_dir, exist_ok=True)

    with open(temp_tex, 'w') as f:
        f.write(filled_template)

    try:
        # Compile LaTeX file
        subprocess.run(['pdflatex', temp_tex, '-output-directory', build_dir], check=True)

        # Ensure the PDF is moved to the desired location
        generated_pdf = os.path.join(build_dir, os.path.splitext(temp_tex)[0] + ".pdf")
        if not os.path.exists(generated_pdf):
            # If not in build dir, look in the current dir
            generated_pdf = temp_pdf

        # Move the generated PDF to the output file
        os.rename(generated_pdf, output_file)
    finally:
        # Cleanup temporary files
        if os.path.exists(temp_tex):
            os.remove(temp_tex)
        if os.path.exists(temp_pdf):
            os.remove(temp_pdf)

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
