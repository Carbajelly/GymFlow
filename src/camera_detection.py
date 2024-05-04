"""
Run object detection on images, Press ESC to exit the program
For Raspberry PI, please use `import tflite_runtime.interpreter as tflite` instead
"""
import re
import cv2
import numpy as np
import time
from pycoral.utils import edgetpu
from pycoral.utils import dataset

import tflite_runtime.interpreter as tflite

from PIL import Image

VIDEO_WIDTH = 640 #640 to fill whole screen, 320 for GUI component
VIDEO_HEIGHT = 480 #480 to fill whole screen, 240 for GUI component

bench1 = [(327, 459), (338, 282), (520, 285), (526, 445)]
bench2 = [(94, 423), (117, 272), (273, 275), (211, 454)]

def load_labels(label_path):
    r"""Returns a list of labels"""
    with open(label_path) as f:
        labels = {}
        for line in f.readlines():
            m = re.match(r"(\d+)\s+(\w+)", line.strip())
            labels[int(m.group(1))] = m.group(2)
        return labels


def load_model(model_path):
    r"""Load TFLite model, returns a Interpreter instance."""
    
    interpreter = edgetpu.make_interpreter(model_path, device = 'usb')
    print('got here')
    interpreter.allocate_tensors()
    return interpreter


def process_image(interpreter, image, input_index):
    r"""Process an image, Return a list of detected class ids and positions"""
    input_data = np.expand_dims(image, axis=0)  # expand to 4-dim

    # Process
    interpreter.set_tensor(input_index, input_data)
    interpreter.invoke()

    # Get outputs
    output_details = interpreter.get_output_details()
    
    
    #print(output_details)
    #output_details[0] - position
    # output_details[1] - class id
    # output_details[2] - score
    # output_details[3] - count

    positions = np.squeeze(interpreter.get_tensor(output_details[0]['index']))
    classes = np.squeeze(interpreter.get_tensor(output_details[1]['index']))
    scores = np.squeeze(interpreter.get_tensor(output_details[2]['index']))

    result = []

    for idx, score in enumerate(scores):
        if score > 0.8:
            result.append({'pos': positions[idx], '_id': classes[idx]})

    return result

def bboxCenterPoint(x1, y1, x2, y2):
    bbox_center_x = int((x1 + x2) / 2)
    bbox_center_y = int((y1 + y2) / 2)

    return [bbox_center_x, bbox_center_y]

def display_result(result, frame, labels):
    r"""Display Detected Objects"""
    font = cv2.FONT_HERSHEY_SIMPLEX
    size = 0.6
    color = (255, 255, 0)  # Blue color
    thickness = 2

    list1 = []
    list2 = []

    for obj in result:
        pos = obj['pos']
        _id = obj['_id']

        x1 = int(pos[1] * VIDEO_WIDTH)
        x2 = int(pos[3] * VIDEO_WIDTH)
        y1 = int(pos[0] * VIDEO_HEIGHT)
        y2 = int(pos[2] * VIDEO_HEIGHT)

        center = bboxCenterPoint(x1, y1, x2, y2)

        cv2.putText(frame, labels[_id], (x1, y1), font, size, color, thickness)
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, thickness)

        results1=cv2.pointPolygonTest(np.array(bench1,np.int32),((center[0], center[1])),False)
        results2=cv2.pointPolygonTest(np.array(bench2,np.int32),((center[0], center[1])),False)

        if results1>=0:
            list1.append(labels[_id])

        if results2>=0:
            list2.append(labels[_id])

    ben1 = len(list1)
    ben2 = len(list2)

    if ben1==1:
        cv2.polylines(frame,[np.array(bench1,np.int32)],True,(0,0,255),2)
        cv2.putText(frame, "Bench 1",(520, 285), font, size, (0,0,255), thickness)
    else:
        cv2.polylines(frame,[np.array(bench1,np.int32)],True,(0,255,0),2)
        cv2.putText(frame, "Bench 1",(520, 285), font, size, (0,255,0), thickness)

    if ben2==1:
        cv2.polylines(frame,[np.array(bench2,np.int32)],True,(0,0,255),2)
        cv2.putText(frame, "Bench 2",(273, 275), font, size, (0,0,255), thickness)
    else:
        cv2.polylines(frame,[np.array(bench2,np.int32)],True,(0,255,0),2)
        cv2.putText(frame, "Bench 2",(273, 275), font, size, (0,255,0), thickness)
           
    cv2.imshow('Object Detection', frame)


if __name__ == "__main__":

    model_path = 'ssd_mobilenet_v2_coco_quant_postprocess_edgetpu.tflite'

    label_path = 'coco_labels.txt'
    cap = cv2.VideoCapture(0)

    interpreter = load_model(model_path)
    
    #labels = load_labels(label_path)
    labels = dataset.read_label_file(label_path)
    
    #input_details = common.input_size(interpreter)
    input_details = interpreter.get_input_details()

    # Get Width and Height
    input_shape = input_details[0]['shape']
    height = input_shape[1]
    width = input_shape[2]
    print(height)
    print(width)

    # Get input index
    input_index = input_details[0]['index']

    # Process Stream
    while True:
        ret, frame = cap.read()
        
        image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        image = image.resize((width, height))

        top_result = process_image(interpreter, image, input_index)

        display_result(top_result, frame, labels)
        
        key = cv2.waitKey(1)
        if key == 27:  # esc
            break

    cap.release()
    cv2.destroyAllWindows()
