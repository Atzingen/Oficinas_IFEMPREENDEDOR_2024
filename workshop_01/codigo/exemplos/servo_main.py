import cv2
import numpy as np
# import serial
import time

# Configura a conexão serial com o Arduino (ajuste a porta conforme necessário)
# arduino = serial.Serial('COM3', 9600)  # Substitua 'COM3' pela porta correta
time.sleep(2)  # Aguarda a conexão estabilizar

# Dimensões desejadas da janela de exibição
hor = 660
vert = 330

# Função de callback para trackbars
def emtpy_callback(_):
    pass

# Função para converter a posição x em graus de 0 a 180, limitando a área útil
def posicao_para_graus(x, largura, margem_lateral):
    x_central = max(min(x - margem_lateral, largura - 2 * margem_lateral), 0)  # Limita x na área central
    return int(x_central * 180 / (largura - 2 * margem_lateral))

# Margem lateral para limitar a área útil de detecção
margem_lateral = 50

# Inicializa a captura de vídeo da webcam
cap = cv2.VideoCapture(0)
cv2.namedWindow('Filtros')
cv2.resizeWindow('Filtros', 640, 480)

# Trackbars para ajustar os limites HSV
cv2.createTrackbar("LH", "Filtros", 0, 179, emtpy_callback)
cv2.createTrackbar("LS", "Filtros", 0, 255, emtpy_callback)
cv2.createTrackbar("LV", "Filtros", 0, 255, emtpy_callback)
cv2.createTrackbar("UH", "Filtros", 179, 179, emtpy_callback)
cv2.createTrackbar("US", "Filtros", 255, 255, emtpy_callback)
cv2.createTrackbar("UV", "Filtros", 255, 255, emtpy_callback)

# Configurações do detector de blobs
params = cv2.SimpleBlobDetector_Params()
params.filterByArea = True
params.minArea = 1000
params.maxArea = 1000000
params.filterByCircularity = False
params.filterByConvexity = False
params.filterByInertia = False
detector = cv2.SimpleBlobDetector_create(params)

# Ajustes iniciais dos trackbars
cv2.setTrackbarPos("LH", "Filtros", 102)
cv2.setTrackbarPos("LS", "Filtros", 122)
cv2.setTrackbarPos("LV", "Filtros", 44)
cv2.setTrackbarPos("UH", "Filtros", 123)

while True:
    # Captura o quadro da webcam
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    if not ret:
        break
    
    # Converte o quadro para HSV e aplica o filtro de cores
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lh = cv2.getTrackbarPos("LH", "Filtros")
    ls = cv2.getTrackbarPos("LS", "Filtros")
    lv = cv2.getTrackbarPos("LV", "Filtros")
    uh = cv2.getTrackbarPos("UH", "Filtros")
    us = cv2.getTrackbarPos("US", "Filtros")
    uv = cv2.getTrackbarPos("UV", "Filtros")

    # Aplica a máscara com base nos limites definidos
    lower = np.array([lh, ls, lv])
    upper = np.array([uh, us, uv])
    mask = cv2.inRange(hsv, lower, upper)
    res = cv2.bitwise_and(frame, frame, mask=mask)

    # Obtém as dimensões da imagem
    height, width, _ = res.shape

    # Detecta blobs na máscara invertida
    inverted_mask = cv2.bitwise_not(mask)
    keypoints = detector.detect(inverted_mask)
    frame_with_keypoints = cv2.drawKeypoints(res, keypoints, np.array([]), (0, 255, 255),
                                             cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    # Para cada keypoint detectado, calcula o grau correspondente e envia para o Arduino
    for keypoint in keypoints:
        x = int(keypoint.pt[0])  # Coordenada x do centro do keypoint
        grau = posicao_para_graus(x, width, margem_lateral)  # Converte a posição x para o grau correspondente
        
        # Envia o ângulo via serial para o Arduino
        comando = f"{grau}\n"
        # arduino.write(comando.encode())
        
        # Exibe o ângulo correspondente na tela
        texto = f"{grau} graus"
        cv2.putText(frame_with_keypoints, texto, (x, int(keypoint.pt[1]) - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Redimensiona e exibe as janelas
    frame_with_keypoints = cv2.resize(frame_with_keypoints, (hor, vert))
    cv2.imshow("Filtros", frame_with_keypoints)

    # Interrompe o loop se a tecla 'q' for pressionada
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera os recursos
cap.release()
cv2.destroyAllWindows()
# arduino.close()