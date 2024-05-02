import cv2
import pandas as pd
import numpy as np

if __name__ == "__main__":
    cap = cv2.VideoCapture('src/test/testFile.mp4')

    while True:
        ret, frame = cap.read()

        key = cv2.waitKey(1)
        if key == 27:  # esc
            break

    cap.release()
    cv2.destroyAllWindows()