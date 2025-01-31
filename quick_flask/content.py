base_api_py = r"""# import cv2
# this is for streaming video feed from webcam
# if you want to use this, uncomment the code above and run $ pip install opencv-python

from flask import Blueprint

api = Blueprint("api", __name__)

@api.route("/test")
def api_test():
    return "API blueprint is set up!"


# API to stream video feed from webcam
# camera = cv2.VideoCapture(0)
# def generate_frames():
#     while True:
#         success, frame = camera.read()
#         if not success:
#             break
#         else:
#             _, buffer = cv2.imencode('.jpg', frame)
#             frame = buffer.tobytes()
#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
# @api.route('/video_feed')
# def video_feed():
#     return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


# Build your APIs from here
"""

base_base_html = r"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{% block title %}{% endblock %}</title>
    <style>
      body {
        font-family: monospace;
        margin: 0;
        padding: 0;
      }
      .navbar {
        background-color: #333;
        color: white;
        padding: 1rem;
        text-align: center;
      }
      main {
        padding: 2rem;
      }
    </style>
  </head>
  <body>
    <div class="navbar">
      <h1>Quick flask</h1>
    </div>
    <main>
      {% block content %} {% endblock %}
    </main>
  </body>
</html>
"""

base_boilerplate_init_py = r"""# Register your blueprints here
"""

base_home_html = r"""{% extends 'base.html' %}

{% block title %}Home{% endblock %}

{% block content %}
  <h1>Welcome to Your Flask Application!</h1>
  <p>Welcome to your newly created Flask app powered by QuickFlask. This setup provides a solid foundation for creating a scalable and modular Flask application with ease.</p>

  <h2>Getting Started</h2>
  <p>Here are the key components of your project structure and how to begin:</p>
  <ul>
    <li>The main application folder is <code>app/</code>. All your app's core logic and structure will reside here.</li>
    <li>The entry point of your app is <code>app/__init__.py</code>. This is where Flask's app instance is created and configurations are initialized.</li>
    <li>Your app is organized using <code>Blueprints</code>, which are located in <code>app/blueprints/</code>. Blueprints help structure your app into logical modules.</li>
    <li>Blueprint for the Home Page: <code>app/blueprints/home.py</code>. This blueprint defines the routes and views for the homepage of your application.</li>
    <li>API Blueprint: <code>app/blueprints/api.py</code>. You can test the API at the endpoint: <a href="/api/test">/api/test</a>.</li>
    <li>If you selected SocketIO during setup, the SocketIO blueprint will be available in <code>app/blueprints/socketio.py</code>. This blueprint helps in adding real-time capabilities to your app, such as chat or notifications.</li>
  </ul>

  <h2>About Flask</h2>
  <p>Flask is a minimalistic WSGI (Web Server Gateway Interface) web application framework for Python. It focuses on simplicity and flexibility, which makes it ideal for both beginners and seasoned developers. Flask provides the core tools needed to get a web application up and running quickly, while allowing developers to add only the features they need.</p>
  
  <p>Some key features of Flask include:</p>
  <ul>
    <li>Lightweight: Flask is designed to keep the core simple yet extensible.</li>
    <li>Flexible: It doesn’t dictate how to structure your application, so you have the freedom to design your app the way you want.</li>
    <li>Extensible: Flask allows you to add any functionality you need through extensions. Some common extensions include Flask-SQLAlchemy for databases, Flask-WTF for forms, and Flask-Login for user authentication.</li>
    <li>Built-in development server and debugger for rapid development.</li>
  </ul>

  <h2>Blueprints in Flask</h2>
  <p>Blueprints allow you to organize your application into smaller, reusable components. They are an essential feature in Flask, particularly for larger applications that require modularization.</p>
  
  <p>Each blueprint encapsulates a set of routes, templates, static files, and other components that relate to a specific feature or functionality of the application. By using blueprints, you can keep your codebase clean and maintainable while also making it easier to scale your app in the future.</p>
  
  <p>To create a new blueprint, follow these steps:</p>
  <ul>
    <li>Define the blueprint in a separate Python file within <code>app/blueprints/</code>.</li>
    <li>Register the blueprint in the main app initialization file (<code>app/__init__.py</code>).</li>
    <li>Assign routes to the blueprint and link them to the necessary views or templates.</li>
  </ul>

  <h2>Templates and Jinja2</h2>
  <p>Flask uses <strong>Jinja2</strong> as its template engine. Jinja2 allows you to create dynamic HTML pages by embedding Python-like expressions inside your HTML files. This makes it possible to render data from Python objects directly into your HTML files.</p>

  <p>Benefits of using Jinja2 with Flask:</p>
  <ul>
    <li>Separation of concerns: Jinja2 allows you to separate your application's presentation logic (HTML) from the business logic (Python), leading to cleaner and more maintainable code.</li>
    <li>Dynamic content: You can easily include dynamic content like variables, conditionals, loops, and filters in your templates.</li>
    <li>Template inheritance: Jinja2 supports template inheritance, allowing you to create a base template and extend it across multiple pages, which promotes reuse and consistency.</li>
  </ul>

  <h2>Why Choose Flask?</h2>
  <p>Flask is a great choice for a web framework because of its:</p>
  <ul>
    <li>Minimalism: Flask’s core is simple and small, making it easy to understand and use, especially for those new to web development.</li>
    <li>Flexibility: Flask does not impose a specific way of organizing your code or how to structure your project. It gives you full control over the application's components.</li>
    <li>Rich ecosystem: Flask has a vibrant community and a wealth of extensions that can help you extend its functionality.</li>
    <li>Development speed: Flask’s built-in server and debugging tools make it quick and easy to prototype and develop applications.</li>
  </ul>
  
  <p>Whether you're building a small project or scaling a larger application, Flask can handle your needs without adding unnecessary complexity.</p>
{% endblock %}
"""

base_home_py = r"""from flask import Blueprint, render_template

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def home():
    return render_template('home.html')
"""

base_socketio_py = r"""from flask import Blueprint

socketio_bp = Blueprint("socketio", __name__)

@socketio_bp.route("/socketio-test")
def socketio_test():
    return "SocketIO blueprint is set up!"


# Handle your SocketIO events here
"""