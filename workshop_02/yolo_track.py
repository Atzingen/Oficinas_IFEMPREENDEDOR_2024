import cv2
from ultralytics import YOLO
from collections import defaultdict
import numpy as np

model = YOLO("../models/yolo11l.pt") 
# model = YOLO("../models/maca_y11l.pt") 
# model = YOLO("yolov10n.pt") 
# model = YOLO("yolov8n-pose.pt") 
# model = YOLO("../models/best.pt")

cap = cv2.VideoCapture(0) 

if not cap.isOpened():
    print("Error: Cannot open webcam")
    exit()

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

track_history = defaultdict(lambda: [])

while True:
    ret, frame = cap.read()
    results = model.track(source=frame, 
                          persist=True, 
                          verbose=False)
    if results[0]:
        boxes = results[0].boxes.xywh.cpu()
        track_ids = results[0].boxes.id.int().cpu().tolist()
        annotated_frame = results[0].plot()
        for box, track_id in zip(boxes, track_ids):
            x, y, w, h = box
            track = track_history[track_id]
            track.append((float(x), float(y))) 
            if len(track) > 30:  
                track.pop(0)
            points = np.hstack(track).astype(np.int32).reshape((-1, 1, 2))
            cv2.polylines(annotated_frame, 
                          [points], 
                          isClosed=False, 
                          color=(230, 230, 230), 
                          thickness=10)
        cv2.imshow("YOLO", annotated_frame)
    else:
        cv2.imshow("YOLO", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()