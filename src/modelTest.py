import re
import cv2
import numpy as np
import time
import math
from pycoral.utils import edgetpu
from pycoral.utils import dataset
from pycoral.adapters import common
from pycoral.adapters import classify

import tflite_runtime.interpreter as tflite

from PIL import Image

model_path = 'gymFlowModel_edgetpu.tflite'

interpreter = edgetpu.make_interpreter(model_path, device='usb')
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()

output_details = interpreter.get_output_details()

print("Input Details: ", input_details)

print("Output Details: ", output_details)