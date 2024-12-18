import numpy as np
import tensorflow as tf
from tensorflow.keras.layers import Dense, Flatten, AvgPool2D, Conv2D, MaxPool2D, Dropout,  MaxPooling2D
import cv2
import matplotlib.pyplot as plt
import os
from tensorflow.keras.models import load_model

path = "modelos/best.h5"

model = load_model(path)
cap = cv2.VideoCapture(0)

# Obter a resolução da câmera
ret, frame = cap.read()
height, width, _ = frame.shape

# Definir o tamanho do quadrado
square_size = 150
start_x = (width - square_size) // 2
start_y = (height - square_size) // 2

while True:
    ret, frame = cap.read()
    if not ret:
        break
    cv2.rectangle(frame, (start_x, start_y), (start_x + square_size, start_y + square_size), (0, 255, 0), 2)
    cropped_frame = frame[start_y:start_y + square_size, start_x:start_x + square_size]
    gray = cv2.cvtColor(cropped_frame, cv2.COLOR_BGR2GRAY)  # Converter para escala de cinza
    resized = cv2.resize(gray, (28, 28))  # Redimensionar para 28x28 pixels
    normalized = resized / 255.0  # Normalizar
    reshaped = normalized.reshape(1, 28, 28, 1)  # Adicionar dimensão batch
    prediction = model.predict(reshaped, verbose=0)
    predicted_digit = np.argmax(prediction)
    cv2.putText(frame, f'Predicao: {predicted_digit}', (start_x, start_y - 10), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    cv2.imshow("Live Prediction", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
