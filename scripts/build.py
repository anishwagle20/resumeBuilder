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
    # Path to template-specific build scripts
    scripts_dir = "scripts"
    
    # List all build scripts for templates
    build_scripts = [
        script for script in os.listdir(scripts_dir)
        if script.startswith('build_template') and script.endswith('.py')
    ]

    if not build_scripts:
        print("No template build scripts found. Please add a build_templateX.py script to the scripts directory.")
        return

    # Execute each build script
    for script in build_scripts:
        print(f"Processing {script}...")
        build_resume(os.path.join(scripts_dir, script))

if __name__ == "__main__":
    main()
