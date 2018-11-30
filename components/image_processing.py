import cv2
import numpy as np


class ImageProcessing():
    """docstring for ImageProcessing."""

    def __init__(self):
        print("Création d'un processeur d'images")


    def fopen_camera(self):
        cap = cv2.VideoCapture(0)
        while True:
            # Capture fram-by-frame
            ret, frame = cap.read()
            # Our operations on the frame come here
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # Display the resulting frame
            cv2.imshow('frame', gray)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        # when enrything done, release the Capture
        cap.release()
        cv2.destroyAllWindows()
