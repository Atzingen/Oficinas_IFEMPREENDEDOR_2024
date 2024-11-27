import cv2
import numpy as np

captura = cv2.VideoCapture(0)

cv2.namedWindow('tela', cv2.WINDOW_NORMAL)
cv2.resizeWindow('tela', 800, 600)

while True:
    _, frame1 = captura.read()
    _, frame2 = captura.read()
    frame = cv2.absdiff(frame1, frame2)
    frame_cinza = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    
    cv2.imshow('tela', frame_cinza)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

captura.release()