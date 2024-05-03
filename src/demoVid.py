import cv2
import pandas as pd
import numpy as np
from ultralytics import YOLO
import time
from pycoral.utils import edgetpu
import tflite_runtime.interpreter as tflite
from PIL import Image

model=YOLO('yolov8s.pt')

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

areaBen1 = []

while (cap.isOpened()):   
    print("got here") 
    ret,frame = cap.read()
    if not ret:
        break
    
    frame=cv2.resize(frame,(1020,500))

    results=model.predict(frame)
 #   print(results)
    a=results[0].boxes.data
    px=pd.DataFrame(a).astype("float")
#    print(px)
   
    listBen1 = []
    
    for index,row in px.iterrows():
#        print(row)
 
        x1=int(row[0])
        y1=int(row[1])
        x2=int(row[2])
        y2=int(row[3])
        d=int(row[5])
        c=class_list[d]
        if 'person' or 'bottle' in c:
            cx=int(x1+x2)//2
            cy=int(y1+y2)//2
      
            resultsBen1=cv2.pointPolygonTest(np.array(areaBen1,np.int32),((cx,cy)),False)
            if resultsBen1>=0:
               cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)
               cv2.circle(frame,(cx,cy),3,(0,0,255),-1)
               listBen1.append(c)  
        
              
            
    
    ben1=(len(listBen1))
  
  
    if ben1==1:
        cv2.polylines(frame,[np.array(areaBen1,np.int32)],True,(0,0,255),2)
        cv2.putText(frame,str('Bench 1'),(591,398),cv2.FONT_HERSHEY_COMPLEX,0.5,(0,0,255),1)
    else:
        cv2.polylines(frame,[np.array(areaBen1,np.int32)],True,(0,255,0),2)
        cv2.putText(frame,str('Bench 1'),(591,398),cv2.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),1)
   
    
    

    cv2.imshow("RGB", frame)

    key = cv2.waitKey(1)
    if key == 27:  # esc
        break
    
cap.release()
cv2.destroyAllWindows()
#stream.stop()


