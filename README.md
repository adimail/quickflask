# QuickFlask

**QuickFlask** is a CLI tool designed to help you create modular, functional Flask applications in seconds. I love Flask, but I often found myself writing the same boilerplate code repeatedly. To save time, I created QuickFlask. This tool will save you time and effort, allowing you to focus on building your application rather than setting up the initial structure. It adheres to the DRY (Don’t Repeat Yourself) principle.

## Installation

To install QuickFlask, run:

```sh
pip3 install quick-flask
```

## Usage

Once installed, you can create a new Flask project by running:

```sh
quickflask
```

### Options:

- `--name` (Required): The name of your Flask application.
- `--socketio` (Optional): Include Flask-SocketIO support for real-time communication.

Example with SocketIO:

```sh
quickflask --name my-chat-app --socketio
```

## Running Your Flask App

After creating your project, navigate into the directory:

```sh
cd my_flask_app
```

Set up a virtual environment (recommended):

```sh
python3 -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

Install dependencies:

```sh
pip install -r requirements.txt
```

Run the Flask app:

```sh
python app.py
```

Your application will be accessible at `http://127.0.0.1:5000/`.

## Features

- Generates a structured Flask project with blueprints and templates.
- Automatically sets up templates and API routes.
- Saves time by eliminating repetitive boilerplate code.

## Contributing

Feel free to open issues or submit pull requests to improve QuickFlask. Contributions are always welcome!

## License

This project is licensed under the MIT License. See `LICENSE` for details.

## Change Log

For a detailed list of changes and version history, please see the [CHANGELOG.md](CHANGELOG.md) file.
