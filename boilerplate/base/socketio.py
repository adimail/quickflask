from flask import Blueprint

socketio_bp = Blueprint("socketio", __name__)

@socketio_bp.route("/socketio-test")
def socketio_test():
    return "SocketIO blueprint is set up!"


# Handle your SocketIO events here
