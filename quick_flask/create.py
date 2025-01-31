import os
import click
import subprocess
import platform
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
        f"{app_name}",
        f"{app_name}/app",
        f"{app_name}/app/blueprints",
        f"{app_name}/app/templates",
    ]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

def create_file(filepath, content):
    with open(filepath, "w") as f:
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

def check_installed_versions():
    """Check for installed versions of pip and python."""
    versions = {
        "pip": None,
        "pip2": None,
        "pip3": None,
        "python": None,
        "python2": None,
        "python3": None
    }
    for version in versions.keys():
        try:
            subprocess.run([version, "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            versions[version] = True
        except (subprocess.CalledProcessError, FileNotFoundError):
            versions[version] = False
    return versions

@click.command()
@click.option('--name', prompt='Enter your app name', help='Name of the Flask application')
@click.option('--socketio', is_flag=True, prompt='Include SocketIO?', help='Include Flask-SocketIO support')
def create_flask_app(name, socketio):
    while os.path.exists(name):
        click.echo(click.style(f"Error: '{name}' already exists. Choose a different name.", fg='red'))
        name = click.prompt('Enter a new app name')
    click.echo(click.style(f"\nCreating Flask application: {name}\n", fg='cyan'))
    click.echo(click.style(f"- SocketIO: {'Yes' if socketio else 'No'}", fg='cyan'))
    
    versions = check_installed_versions()

    pip_version = "pip3" if versions["pip3"] else "pip"
    python_version = "python3" if versions["python3"] else "python"

    if versions["pip2"]:
        pip_version = click.prompt("Which pip version would you like to use?", type=click.Choice(["pip", "pip2", "pip3"]), default=pip_version)

    if versions["python2"]:
        python_version = click.prompt("Which python version would you like to use?", type=click.Choice(["python", "python2", "python3"]), default=python_version)
        
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
    click.echo(click.style("5. python app.py", fg='cyan'))
    
    click.echo(click.style(f"\nQuick start in one command:", fg='yellow'))
    click.echo(click.style(
        f"cd {name} && {python_version} -m venv venv && {activation_command} && {pip_version} install -r requirements.txt && {python_version} app.py", 
        fg='green'
    ))


if __name__ == "__main__":
    create_flask_app()
