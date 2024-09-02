from flask import Flask, render_template, Response, jsonify, url_for
from camera import VideoCamera

pi_camera = VideoCamera(flip=False)  # Use the laptop's built-in camera

app = Flask(__name__)

@app.route('/')
def index():
    # Home page providing a link to the live stream
    stream_url = url_for('video_feed')
    return render_template('index.html', stream_url=stream_url)

def gen(camera):
    # Get camera frame
    while True:
        frame = camera.get_frame()
        if frame is None:
            continue
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    # Route to serve the video feed
    return Response(gen(pi_camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/api/live_stream')
def get_live_stream_link():
    # API route to get the live stream link
    stream_url = url_for('video_feed', _external=True)
    return jsonify({"live_stream_url": stream_url})

@app.route('/picture')
def take_picture():
    # Route to take a picture
    pi_camera.take_picture()
    return "Photo taken"

if __name__ == '__main__':
    app.run(debug=False)
