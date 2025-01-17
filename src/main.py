import os
import subprocess
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_script(script_path):
    try:
        result = subprocess.run(['python', script_path], capture_output=True, text=True)
        logging.info(f'Script output: {result.stdout}')
        if result.stderr:
            logging.error(f'Script errors: {result.stderr}')
    except Exception as e:
        logging.error(f"Error executing script {script_path}: {e}")

def main():
    scripts = {
        '0': 'contentgenerator_bot/contentgenerator_general.py.py',
        '1': 'x_bot/x_uploader.py',
        '2': 'youtube_bot/youtube_uploader.py',
        '3': 'instagram_bot/instagram_uploader.py'
    }

    if len(sys.argv) > 1:
        choices = sys.argv[1].split(',')
    else:
        print("Select scripts to run (comma-separated):")
        print("1: x_uploader.py")
        print("2: youtube_uploader.py")
        print("3: instagram_uploader.py")
        choices = input("Enter the numbers of the scripts to run (e.g., 1,2,3): ").split(',')

    # Append '0' to the first value of choices
    choices = ['0'] + choices

    for choice in choices:
        choice = choice.strip()
        if choice in scripts:
            logging.info(f"Executing Script: {choice}")
            script_path = os.path.join(os.path.dirname(__file__), scripts[choice])
            run_script(script_path)
            logging.info(f"Script Finished: {choice}")
        else:
            logging.warning(f"Invalid choice: {choice}. Please select a valid script number.")

    logging.info(f"Project Finished for: {choices}")

if __name__ == "__main__":
    main()
