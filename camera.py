import cv2 as cv
import time
from datetime import datetime
import numpy as np

class VideoCamera(object):
    def __init__(self, flip=False, file_type=".jpg", photo_string="stream_photo"):
        self.vs = cv.VideoCapture(0)  # Use the laptop's built-in camera
        self.flip = flip  # Flip frame vertically
        self.file_type = file_type  # Image type, e.g., .jpg
        self.photo_string = photo_string  # Name to save the photo
        self.previous_frame = None  # Initialize previous frame
        time.sleep(2.0)  # Allow the camera sensor to warm up

    def __del__(self):
        self.vs.release()  # Release the camera

    def flip_if_needed(self, frame):
        if self.flip:
            return np.flip(frame, 0)
        return frame

    def get_frame(self):
        ret, frame = self.vs.read()  # Read a frame from the camera
        if not ret:
            if self.previous_frame is not None:
                return self.previous_frame.tobytes()  # Return the previous frame if available
            else:
                # Return a placeholder image if no previous frame is available
                placeholder = np.zeros((480, 640, 3), dtype=np.uint8)
                ret, jpeg = cv.imencode(self.file_type, placeholder)
                return jpeg.tobytes()

        frame = self.flip_if_needed(frame)  # Flip the frame if needed
        ret, jpeg = cv.imencode(self.file_type, frame)
        self.previous_frame = jpeg  # Save the current frame as previous frame
        return jpeg.tobytes()

    def take_picture(self):
        ret, frame = self.vs.read()  # Capture a frame
        if not ret:
            return None
        frame = self.flip_if_needed(frame)  # Flip the frame if needed
        today_date = datetime.now().strftime("%m%d%Y-%H%M%S")  # Get current time
        cv.imwrite
