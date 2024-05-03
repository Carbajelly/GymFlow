import re
import cv2
import numpy as np
import time
import math
from pycoral.utils import edgetpu
from pycoral.adapters import detect
from pycoral.adapters import common

import tflite_runtime.interpreter as tflite

from PIL import Image

def process_image(interpreter, image, input_index):
    r"""Process an image, Return a list of detected class ids and positions"""
    input_data = (np.array(image)).astype(np.float32)
    input_data = input_data.reshape((1, 640, 640, 3))

    # Process
    interpreter.set_tensor(input_index, input_data)
    interpreter.invoke

    # Get outputs
    detections = detect.get_objects(interpreter, 0.8)

    for obj in detections:
        print(obj)

if __name__ == "__main__":

    model_path = 'gymFlowModel_edgetpu.tflite'

    cap = cv2.VideoCapture('testFile.mp4')

    interpreter = edgetpu.make_interpreter(model_path, device='usb')
    interpreter.allocate_tensors()

    input_details = interpreter.get_input_details()
    
    input_shape = input_details[0]['shape']
    height = input_shape[1]
    width = input_shape[2]

    input_index = input_details[0]['index']

    while cap.isOpened():
        ret, frame = cap.read()

        image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        image = image.resize((width, height))

        top_result = process_image(interpreter, image, input_index)


    cap.release()
    cv2.destroyAllWindows()