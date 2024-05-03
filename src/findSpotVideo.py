import cv2
import pandas as pd
import numpy as np
from ultralytics import YOLO
import time

model=YOLO('gymFlowModel_edgetpu.tflite', task='detect')


def RGB(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE :  
        colorsBGR = [x, y]
        print(colorsBGR)
        

cv2.namedWindow('RGB')
cv2.setMouseCallback('RGB', RGB)

cap=cv2.VideoCapture('testFile.mp4')

my_file = open("coco.txt", "r")
data = my_file.read()
class_list = data.split("\n")
   




area9=[(511,327),(557,388),(603,383),(549,324)]




while True:    
    ret,frame = cap.read()
    if not ret:
        break
    
    frame=cv2.resize(frame,(640,640))

    results=model.predict(frame)
 #   print(results)
    a=results[0].boxes.data
    px=pd.DataFrame(a).astype("float")
#    print(px)

    cv2.imshow("RGB", frame)

    if cv2.waitKey(1)&0xFF==27:
        break
cap.release()
cv2.destroyAllWindows()
#stream.stop()


