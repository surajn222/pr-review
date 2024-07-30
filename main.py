import os
import sys
import subprocess
from copenai import copenai
import yaml
from dotenv import load_dotenv
import os
import pprint

# Load the .env file
load_dotenv()
print(os.getenv('OPENAI_KEY'))

def run_bash_command(command):
    """
    Runs a bash command and returns the output.

    :param command: A string representing the bash command to be executed.
    :return: The output of the command as a string.
    """
    try:
        result = subprocess.run(command, shell=True, check=True, text=True, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"An error occurred: {e.stderr}"


def extract_new_code_from_git_diff(absolute_path):
    try:
        # Generate the git diff output
        command = "cd " + absolute_path + " && git diff HEAD~1 HEAD -U5"
        diff_output = run_bash_command(command)

        # Filter new code lines and clean them
        grep_command = f"echo '{diff_output}' | grep '^[+]' | sed 's/^+//'"
        new_code = run_bash_command(grep_command)

        return new_code
    except Exception as e:
        return f"An error occurred: {str(e)}"

def process(absolute_path):
    # Example usage
    new_code_output = extract_new_code_from_git_diff(absolute_path)
    # print("Output")
    # print(new_code_output)

    code_changes_map ={}
    file_name = ""
    code_changes_string = ""
    for line in new_code_output.splitlines():
        if line.startswith("++"):
            if code_changes_map:
                code_changes_map[file_name] = code_changes_string
            code_changes_string = ""
            file_name = line[2:]
            code_changes_map[file_name] = ""
            continue
        code_changes_string = code_changes_string + line + "\n"

    code_changes_map[file_name] = code_changes_string

    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(code_changes_map)
    # print(code_changes_map)
    return code_changes_map

def parse_config(config_file):
    # Read the YAML file
    with open(config_file, 'r') as file:
        config = yaml.safe_load(file)

    return config


def pr_review():
    print("PR Review")
    config = parse_config("config.yaml")
    absolute_path = config['path']['location']
    print("Absolute Path " + absolute_path)
    code_changes_map = process(absolute_path)
    sys.exit(1)
    for k, v in code_changes_map.items():
        print("Filename", k)
        print("Changes", v)
        if "pkg/pb" not in k:
            copenai.suggest_changes(v)
        else:
            print("Skipping proto files")



if __name__ == "__main__":
    try:
        pr_review()
    except Exception as e:
        print(str(e))