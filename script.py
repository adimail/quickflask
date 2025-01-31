import os
import click
import subprocess

def create_directory_structure(app_name):
    """Create the basic directory structure for the Flask app."""
    directories = [
        f"{app_name}",
        f"{app_name}/app",
        f"{app_name}/app/blueprints",
        f"{app_name}/app/templates",
    ]

    for directory in directories:
        os.makedirs(directory, exist_ok=True)

def create_app_py(app_name, use_socketio=False):
    """Generate app.py content based on user choices."""
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

    with open(f"{app_name}/app.py", "w") as f:
        f.write("\n".join(content))

def create_init_py(app_name, use_socketio=False):
    """Generate __init__.py content based on user choices."""
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
    content.append("")

    with open(f"{app_name}/app/__init__.py", "w") as f:
        f.write("\n".join(content))

def create_wsgi_py(app_name):
    """Generate wsgi.py content."""
    content = [
        "from app import create_app",
        "",
        "app = create_app()",
        ""
    ]

    with open(f"{app_name}/wsgi.py", "w") as f:
        f.write("\n".join(content))

def create_blueprints_init(app_name, use_socketio=False):
    """Create blueprints/__init__.py, blueprints/home.py, blueprints/api.py, and blueprints/socketio.py files."""
    boilerplate_dir = "boilerplate/base"

    # Map source files to target files
    file_mapping = {
        "boilerplate.__init__.py": "__init__.py",
        "home.py": "home.py",
        "api.py": "api.py"
    }

    for source_file, target_file in file_mapping.items():
        source_path = os.path.join(boilerplate_dir, source_file)
        target_path = os.path.join(f"{app_name}/app/blueprints", target_file)

        if os.path.exists(source_path):
            with open(source_path, "r") as src, open(target_path, "w") as dst:
                dst.write(src.read())
        else:
            print(f"Warning: {source_path} not found. Skipping {target_file}.")

    if use_socketio:
        socketio_path = os.path.join(boilerplate_dir, "socketio.py")
        if os.path.exists(socketio_path):
            with open(socketio_path, "r") as src, open(f"{app_name}/app/blueprints/socketio.py", "w") as dst:
                dst.write(src.read())
        else:
            print(f"Warning: {socketio_path} not found. Skipping socketio.py.")

def create_templates(app_name):
    """Generate HTML templates from boilerplate files."""
    boilerplate_dir = "boilerplate/base"
    target_dir = f"{app_name}/app/templates"

    os.makedirs(target_dir, exist_ok=True)

    files = ["base.html", "home.html"]

    for file in files:
        source_path = os.path.join(boilerplate_dir, file)
        target_path = os.path.join(target_dir, file)

        if os.path.exists(source_path):
            with open(source_path, "r") as src, open(target_path, "w") as dst:
                dst.write(src.read())
        else:
            print(f"Warning: {source_path} not found. Skipping {file}.")

def create_requirements(app_name, use_socketio=False):
    """Generate requirements.txt based on user choices."""
    requirements = ["flask"]

    if use_socketio:
        requirements.append("flask-socketio")

    with open(f"{app_name}/requirements.txt", "w") as f:
        f.write("\n".join(requirements))

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
@click.option('--socketio', is_flag=True, prompt='Do you want to include SocketIO?', help='Include Flask-SocketIO support')
def create_flask_app(name, socketio):
    """Create a new Flask application with the specified options."""

    while os.path.exists(name):
        click.echo(click.style(f"Error: The application name '{name}' already exists. Please choose a different name.", fg='red'))
        name = click.prompt('Enter a new app name')

    click.echo(click.style(f"\nCreating Flask application: {name}", fg='cyan'))
    click.echo(click.style("Selected options:", fg='cyan'))
    click.echo(click.style(f"- SocketIO: {'Yes' if socketio else 'No'}", fg='cyan'))

    versions = check_installed_versions()
    pip_version = "pip3" if versions["pip3"] else "pip"
    python_version = "python3" if versions["python3"] else "python"

    if versions["pip2"]:
        pip_version = click.prompt("Which pip version would you like to use?", type=click.Choice(["pip", "pip2", "pip3"]), default=pip_version)
    if versions["python2"]:
        python_version = click.prompt("Which python version would you like to use?", type=click.Choice(["python", "python2", "python3"]), default=python_version)

    try:
        create_directory_structure(name)

        create_app_py(name, socketio)
        create_init_py(name, socketio)
        create_wsgi_py(name)
        create_blueprints_init(name, socketio)
        create_templates(name)
        create_requirements(name, socketio)

        click.echo(click.style(f"\nFlask application '{name}' created successfully!", fg='green'))
        click.echo(click.style("\nTo get started:", fg='cyan'))
        click.echo(click.style(f"1. cd {name}", fg='cyan'))
        click.echo(click.style(f"2. {python_version} -m venv venv", fg='cyan'))
        click.echo(click.style(f"3. source venv/bin/activate  # On Windows: .\\venv\\Scripts\\activate", fg='cyan'))
        click.echo(click.style(f"4. {pip_version} install -r requirements.txt", fg='cyan'))
        click.echo(click.style("5. python app.py", fg='cyan'))

    except Exception as e:
        click.echo(click.style(f"An error occurred: {e}", fg='red'))

if __name__ == '__main__':
    create_flask_app()
