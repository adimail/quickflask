# import cv2
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
