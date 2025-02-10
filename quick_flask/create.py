import os
import shutil
import sys
import platform
import argparse
import questionary
from colorama import init, Fore, Style

def create_flask_app():
    init(autoreset=True)

    parser = argparse.ArgumentParser(description="Create a Flask app project from a template.")
    parser.add_argument("--name", required=False, help="The name of your Flask application")
    parser.add_argument("--template", choices=["base"], required=False,
                        help="The template to use for the Flask app")
    args = parser.parse_args()

    project_name = args.name or questionary.text("Enter your project name").ask()
    if not project_name:
        sys.exit(1)

    project_template = args.template or questionary.select(
        "Choose a template",
        choices=["base"]
    ).ask()
    if not project_template:
        print(f"{Fore.RED}Error: No template selected. Exiting.{Style.RESET_ALL}")
        sys.exit(1)

    if os.path.exists(project_name):
        print(f"{Fore.RED}Error: Directory '{project_name}' already exists. Please choose a different name.{Style.RESET_ALL}")
        sys.exit(1)

    base_dir = os.path.dirname(os.path.realpath(__file__))
    template_dir = os.path.join(base_dir, 'boilerplate', project_template)

    if not os.path.exists(template_dir):
        print(f"{Fore.RED}Error: Template '{project_template}' not found!{Style.RESET_ALL}")
        sys.exit(1)

    try:
        shutil.copytree(template_dir, project_name)
        print(f"{Fore.GREEN}Project '{project_name}' created successfully using the '{project_template}' template.{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error copying template: {e}{Style.RESET_ALL}")
        sys.exit(1)

    is_windows = platform.system() == "Windows"
    python_cmd = "python" if is_windows else "python3"
    pip_cmd = "pip" if is_windows else "pip3"
    activation_command = ".\\venv\\Scripts\\activate" if is_windows else "source venv/bin/activate"

    print(f"\n{Fore.CYAN}To get started, follow these instructions:{Style.RESET_ALL}")
    print(f"{Fore.CYAN}1. cd {project_name}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}2. {python_cmd} -m venv venv{Style.RESET_ALL}")
    print(f"{Fore.CYAN}3. {activation_command}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}4. {pip_cmd} install -r requirements.txt{Style.RESET_ALL}")
    print(f"{Fore.CYAN}5. {python_cmd} app.py{Style.RESET_ALL}")

    print(f"\n{Fore.YELLOW}Quick start in one command:{Style.RESET_ALL}")
    print(f"{Fore.GREEN}cd {project_name} && {python_cmd} -m venv venv && {activation_command} && {pip_cmd} install -r requirements.txt && {python_cmd} app.py{Style.RESET_ALL}")

if __name__ == '__main__':
    create_flask_app()
