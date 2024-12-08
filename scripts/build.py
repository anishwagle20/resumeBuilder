import os
import subprocess

def build_resume(template_script):
    """
    Run the template-specific build script.
    :param template_script: Path to the script to execute.
    """
    try:
        # Execute the Python build script
        subprocess.run(['python', template_script], check=True)
        print(f"✅ Successfully generated resume using {template_script}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error while running {template_script}: {e}")
    except Exception as ex:
        print(f"⚠️ Unexpected error while running {template_script}: {ex}")

def main():
    """
    Main function to dynamically detect and execute template build scripts.
    """
    # Path to the scripts directory
    scripts_dir = "scripts"

    # Check if scripts directory exists
    if not os.path.isdir(scripts_dir):
        print(f"⚠️ The directory '{scripts_dir}' does not exist. Please create it and add build scripts.")
        return

    # Detect all build_template*.py scripts
    build_scripts = [
        script for script in os.listdir(scripts_dir)
        if script.startswith('build_template') and script.endswith('.py')
    ]

    if not build_scripts:
        print("⚠️ No template build scripts found. Please add build_templateX.py scripts to the scripts directory.")
        return

    # Execute each detected build script
    for script in build_scripts:
        script_path = os.path.join(scripts_dir, script)
        print(f"🚀 Processing {script}...")
        build_resume(script_path)

if __name__ == "__main__":
    main()
