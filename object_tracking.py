import cv2
import numpy as np
from object_detection import ObjectDetection
import math
from Queue import Queue
import os
import glob

#initilaze obj detc
od = ObjectDetection()

tracking_objects = {}
track_id = 0
s = Queue()


def get_first_mp4(directory):
    # Construct the pattern for .mp4 files
    pattern = os.path.join(directory, '*.mp4')
    
    # Get a list of all .mp4 files in the directory
    mp4_files = glob.glob(pattern)
    
    if mp4_files:
        # Sort the files to ensure consistent order
        mp4_files.sort()
        
        # Return the path to the first .mp4 file
        return mp4_files[0]
    else:
        print("No .mp4 files found in the directory.")
        return None
    
directory = os.getcwd()
mp4File = get_first_mp4(directory)
cap = cv2.VideoCapture(mp4File)


while True:
    ret, frame = cap.read()
    if not ret:
        break

    center_points_cur_frame = []

    #detect objects
    (class_ids, scores, boxes) = od.detect(frame)
    for box in boxes:
        (x,y,w,h) = box
        cx = int((x+x+w)/2)
        cy = int((y + y + h)/2)
        center_points_cur_frame.append((cx,cy))
        cv2.rectangle(frame, (x,y), (x + w, y + h), (0, 255, 0), 2) #this creates the rectangle on the frame at postion x,y for its dimensions x+w and y+h and color and line thinccness


        
    tracking_objects_copy = tracking_objects.copy()
    center_points_cur_frame_copy = center_points_cur_frame.copy()
    for object_id, pt2 in tracking_objects_copy.items():
        object_exists = False
        for pt in center_points_cur_frame_copy:
            distance = math.hypot(pt2[0] - pt[0], pt2[1] - pt[1])
            if distance < 20:
                object_exists = True
                tracking_objects[object_id] = pt
                if pt in center_points_cur_frame:
                    center_points_cur_frame.remove(pt)
                continue
        if not object_exists:
            tracking_objects.pop(object_id)
            s.enqueue(object_id)

    
    for pt in center_points_cur_frame:
        if s.is_empty():
            tracking_objects[track_id] = pt
            track_id += 1
        else:
            tracking_objects[s.dequeue()] = pt



    for object_id, pt in tracking_objects.items():
        cv2.circle(frame, pt, 5, (0,0,255), -1)
        cv2.putText(frame, str(object_id), (pt[0],pt[1] - 7), 0, 1, (0, 0, 255), 1)


        

    cv2.imshow("Frame", frame)


    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()