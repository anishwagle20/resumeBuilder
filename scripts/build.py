import os
import subprocess

def build_resume(template_script):
    """
    Run the template-specific build script.
    """
    try:
        subprocess.run(['python', template_script], check=True)
        print(f"Successfully generated resume using {template_script}")
    except subprocess.CalledProcessError as e:
        print(f"Error while running {template_script}: {e}")

def main():
    data = load_data('data.json')
    templates_dir = 'templates'
    build_dir = 'build'

    os.makedirs(build_dir, exist_ok=True)

    for template in os.listdir(templates_dir):
        if template.endswith('.tex'):
            output_file = os.path.join(build_dir, f"{os.path.splitext(template)[0]}.pdf")
            build_resume(os.path.join(templates_dir, template), data, output_file)

if __name__ == "__main__":
    main()
