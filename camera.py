#Modified by smartbuilds.io
#Date: 27.09.20
#Desc: This script uses the laptop's built-in camera instead of the Pi camera.

import cv2 as cv
import imutils
import time
from datetime import datetime
import numpy as np

class VideoCamera(object):
    def __init__(self, flip=False, file_type=".jpg", photo_string="stream_photo"):
        self.vs = cv.VideoCapture(0)  # Use the laptop's built-in camera
        self.flip = flip  # Flip frame vertically
        self.file_type = file_type  # Image type, e.g., .jpg
        self.photo_string = photo_string  # Name to save the photo
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
            return None
        frame = self.flip_if_needed(frame)  # Flip the frame if needed
        ret, jpeg = cv.imencode(self.file_type, frame)
        self.previous_frame = jpeg
        return jpeg.tobytes()

    # Take a photo, called by camera button
    def take_picture(self):
        ret, frame = self.vs.read()  # Capture a frame
        if not ret:
            return None
        frame = self.flip_if_needed(frame)  # Flip the frame if needed
        today_date = datetime.now().strftime("%m%d%Y-%H%M%S")  # Get current time
        cv.imwrite(str(self.photo_string + "_" + today_date + self.file_type), frame)
