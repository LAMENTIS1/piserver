from flask import Flask, request, render_template, Response
from flask_cors import CORS
import queue

app = Flask(__name__)
CORS(app)  # Enable CORS to allow cross-origin requests

# Queue to hold frames from the client
frame_queue = queue.Queue(maxsize=10)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/client')
def client():
    return render_template('client.html')

@app.route('/video_feed', methods=['POST'])
def video_feed():
    if request.method == 'POST':
        frame = request.data
        frame_queue.put(frame)
        return 'Frame received', 200

@app.route('/stream_feed')
def stream_feed():
    def generate_frames():
        while True:
            if not frame_queue.empty():
                frame = frame_queue.get()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
