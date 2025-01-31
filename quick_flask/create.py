import os
import re
import click
import platform
import pkg_resources
import requests
from quick_flask.content import (
    base_api_py,
    base_base_html,
    base_boilerplate_init_py,
    base_home_html,
    base_home_py,
    base_socketio_py,
)

def create_directory_structure(app_name):
    directories = [
        os.path.join(app_name),
        os.path.join(app_name, "app"),
        os.path.join(app_name, "app", "blueprints"),
        os.path.join(app_name, "app", "templates"),
        os.path.join(app_name, "app", "static"),
        os.path.join(app_name, "app", "static", "js"),
        os.path.join(app_name, "app", "static", "css"),
    ]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

def create_file(filepath, content, encoding="utf-8"):
    with open(filepath, "w", encoding=encoding, errors="replace") as f:
        f.write(content)

def create_app_py(app_name, use_socketio=False):
    content = [
        "from app import create_app",
        "",
        "app = create_app()",
        "",
        "if __name__ == '__main__':"
    ]
    if use_socketio:
        content.insert(0, "from flask_socketio import SocketIO")
        content.append("    socketio = SocketIO(app)")
        content.append("    socketio.run(app, debug=True)")
    else:
        content.append("    app.run(debug=True)")
    create_file(f"{app_name}/app.py", "\n".join(content))

def create_init_py(app_name, use_socketio=False):
    content = [
        "from flask import Flask",
        "from app.blueprints.home import home_bp",
        "from app.blueprints.api import api",
        "",
        "def create_app():",
        "    app = Flask(__name__)",
        "",
        "    # Register blueprints",
        "    app.register_blueprint(home_bp)",
        "    app.register_blueprint(api, url_prefix='/api')"
    ]
    if use_socketio:
        content.insert(1, "from flask_socketio import SocketIO")
        content.insert(1, "from app.blueprints.socketio import socketio_bp")
        content.append("    app.register_blueprint(socketio_bp)")
        content.append("    socketio = SocketIO(app)")
    content.append("    return app")
    create_file(f"{app_name}/app/__init__.py", "\n".join(content))

def create_wsgi_py(app_name):
    create_file(f"{app_name}/wsgi.py", "from app import create_app\n\napp = create_app()\n")

def create_blueprints(app_name, use_socketio=False):
    create_file(f"{app_name}/app/blueprints/__init__.py", base_boilerplate_init_py)
    create_file(f"{app_name}/app/blueprints/home.py", base_home_py)
    create_file(f"{app_name}/app/blueprints/api.py", base_api_py)
    if use_socketio:
        create_file(f"{app_name}/app/blueprints/socketio.py", base_socketio_py)

def create_templates(app_name):
    create_file(f"{app_name}/app/templates/base.html", base_base_html)
    create_file(f"{app_name}/app/templates/home.html", base_home_html)

def create_requirements(app_name, use_socketio=False):
    requirements = ["flask"]
    if use_socketio:
        requirements.append("flask-socketio")
    create_file(f"{app_name}/requirements.txt", "\n".join(requirements))

def choose_pip_version():
    """Prompt user to select the pip version."""
    is_windows = platform.system() == "Windows"
    default_pip = "pip" if is_windows else "pip3"

    return click.prompt(
        "\nWhich pip version would you like to use?",
        type=click.Choice(["pip", "pip2", "pip3"]),
        default=default_pip
    )

def choose_python_version():
    """Prompt user to select the python version."""
    is_windows = platform.system() == "Windows"
    default_python = "python" if is_windows else "python3"

    return click.prompt(
        "Which python version would you like to use?",
        type=click.Choice(["python", "python2", "python3"]),
        default=default_python
    )

def get_latest_version():
    """Fetch the latest version from PyPI."""
    try:
        response = requests.get("https://pypi.org/pypi/quick-flask/json", timeout=5)
        if response.status_code == 200:
            return response.json()["info"]["version"]
    except requests.RequestException:
        return None
    return None

def check_for_update():
    """Compare the installed version with the latest version and prompt for update."""
    installed_version = pkg_resources.get_distribution("quick-flask").version
    latest_version = get_latest_version()

    if latest_version and installed_version < latest_version:
        message_lines = [
            f"A new version of quick-flask is available: {latest_version} (You have {installed_version})",
            "Run the following to update:",
            "pip install --upgrade quick-flask",
        ]

        max_length = max(len(line) for line in message_lines)
        border = "─" * (max_length + 4)

        click.echo(click.style(f"\n╭{border}╮", fg="yellow"))
        for line in message_lines:
            click.echo(click.style(f"│  {line.ljust(max_length)}  │", fg="yellow"))
        click.echo(click.style(f"╰{border}╯", fg="yellow"))

@click.command()
@click.option('--name', prompt='Enter your app name', help='Name of the Flask application')
@click.option('--socketio', is_flag=True, prompt='Include SocketIO?', help='Include Flask-SocketIO support')
def create_flask_app(name, socketio):
    check_for_update()

    valid_name_pattern = r'^[a-zA-Z0-9_-]+$'

    while not re.match(valid_name_pattern, name):
        click.echo(click.style("\nError: App name can only contain letters, numbers, hyphens (-), and underscores (_).", fg='red'))
        name = click.prompt('Enter a valid app name')

    while os.path.exists(name):
        click.echo(click.style(f"Error: '{name}' already exists. Choose a different name.", fg='red'))
        name = click.prompt('Enter a new app name')
    click.echo(click.style(f"\nCreating Flask application: {name}\n", fg='cyan'))
    click.echo(click.style(f"- SocketIO: {'Yes' if socketio else 'No'}", fg='cyan'))

    pip_version = choose_pip_version()
    python_version = choose_python_version()

    create_directory_structure(name)
    create_app_py(name, socketio)
    create_init_py(name, socketio)
    create_wsgi_py(name)
    create_blueprints(name, socketio)
    create_templates(name)
    create_requirements(name, socketio)

    is_windows = platform.system() == "Windows"
    activation_command = "source venv/bin/activate" if not is_windows else ".\\venv\\Scripts\\activate"

    click.echo(click.style(f"\nFlask application '{name}' created successfully!", fg='green'))
    click.echo(click.style("\nTo get started:", fg='cyan'))
    click.echo(click.style(f"1. cd {name}", fg='cyan'))
    click.echo(click.style(f"2. {python_version} -m venv venv", fg='cyan'))
    click.echo(click.style(f"3. {activation_command}", fg='cyan'))
    click.echo(click.style(f"4. {pip_version} install -r requirements.txt", fg='cyan'))
    click.echo(click.style(f"5. {python_version} app.py", fg='cyan'))

    click.echo(click.style(f"\nQuick start in one command:", fg='yellow'))
    click.echo(click.style(
        f"cd {name} && {python_version} -m venv venv && {activation_command} && {pip_version} install -r requirements.txt && {python_version} app.py",
        fg='green'
    ))


if __name__ == "__main__":
    create_flask_app()
