import cv2
import numpy as np
import os

# Define o caminho da pasta onde o código está armazenado
current_directory = os.path.dirname(os.path.abspath(__file__))
folder_path = os.path.join(current_directory, '..', 'imgs') # local onde estão as imagens

# Pede ao usuário para digitar o nome da imagem no terminal
image_name = input("Digite o nome da imagem (com extensão, ex: imagem.jpg): ")
image_path = os.path.join(folder_path, image_name)

# Carrega a imagem a partir do caminho fornecido
frame = cv2.imread(image_path)

if frame is None:
    print(f"Erro ao carregar a imagem: {image_name}")
    exit()

frame = cv2.resize(frame, (640, 480))

# Converte a imagem para o espaço de cor HSV
hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

# Cria janelas de trackbars para ajustar os limites da cor
cv2.namedWindow('Filtros')
cv2.createTrackbar("H_min", "Filtros", 0, 179, lambda x: None)
cv2.createTrackbar("S_min", "Filtros", 0, 255, lambda x: None)
cv2.createTrackbar("V_min", "Filtros", 0, 255, lambda x: None)
cv2.createTrackbar("H_max", "Filtros", 179, 179, lambda x: None)
cv2.createTrackbar("S_max", "Filtros", 255, 255, lambda x: None)
cv2.createTrackbar("V_max", "Filtros", 255, 255, lambda x: None)


while True:
    # Obtém os valores das trackbars
    h_min = cv2.getTrackbarPos("H_min", "Filtros")
    s_min = cv2.getTrackbarPos("S_min", "Filtros")
    v_min = cv2.getTrackbarPos("V_min", "Filtros")
    h_max = cv2.getTrackbarPos("H_max", "Filtros")
    s_max = cv2.getTrackbarPos("S_max", "Filtros")
    v_max = cv2.getTrackbarPos("V_max", "Filtros")

    # Define os limites de cor
    lower_bound = np.array([h_min, s_min, v_min])
    upper_bound = np.array([h_max, s_max, v_max])

    # Cria uma máscara para filtrar a imagem
    mask = cv2.inRange(hsv_frame, lower_bound, upper_bound)
    filtered_image = cv2.bitwise_and(frame, frame, mask=mask)

    # Exibe a imagem filtrada
    cv2.imshow('Filtros', filtered_image)

    # Espera por uma tecla pressionada
    key = cv2.waitKey(1) & 0xFF
    
    # Se a tecla 'q' for pressionada, encerra o programa
    if key == ord('q'):
        break
    # Se a tecla 'b' for pressionada, redefine os valores para azul
    elif key == ord('b'):
        cv2.setTrackbarPos("H_min", "Filtros", 96)
        cv2.setTrackbarPos("S_min", "Filtros", 148)
        cv2.setTrackbarPos("V_min", "Filtros", 0)
        cv2.setTrackbarPos("H_max", "Filtros", 120)
        cv2.setTrackbarPos("S_max", "Filtros", 255)  # Ajuste S_max para 255 para o azul
        cv2.setTrackbarPos("V_max", "Filtros", 255)  # Ajuste V_max para 255 para o azul

    # Se a tecla 'g' for pressionada, redefine os valores para verde
    elif key == ord('g'):
        cv2.setTrackbarPos("H_min", "Filtros", 21)
        cv2.setTrackbarPos("S_min", "Filtros", 85)
        cv2.setTrackbarPos("V_min", "Filtros", 0)
        cv2.setTrackbarPos("H_max", "Filtros", 79)
        cv2.setTrackbarPos("S_max", "Filtros", 255)  # Ajuste S_max para 255 para o verde
        cv2.setTrackbarPos("V_max", "Filtros", 255)  # Ajuste V_max para 255 para o verde

    # Se a tecla 'r' for pressionada, redefine os valores para vermelho
    elif key == ord('r'):
        cv2.setTrackbarPos("H_min", "Filtros", 0)
        cv2.setTrackbarPos("S_min", "Filtros", 63)
        cv2.setTrackbarPos("V_min", "Filtros", 0)
        cv2.setTrackbarPos("H_max", "Filtros", 28)
        cv2.setTrackbarPos("S_max", "Filtros", 255)  # Ajuste S_max para 255 para o vermelho
        cv2.setTrackbarPos("V_max", "Filtros", 255)  # Ajuste V_max para 255 para o vermelho

    # Se a tecla 'n' for pressionada, redefine os limites para valores padrão
    elif key == ord('n'):
        cv2.setTrackbarPos("H_min", "Filtros", 0)
        cv2.setTrackbarPos("S_min", "Filtros", 0)
        cv2.setTrackbarPos("V_min", "Filtros", 0)
        cv2.setTrackbarPos("H_max", "Filtros", 255)
        cv2.setTrackbarPos("S_max", "Filtros", 255)  # Ajuste S_max para 255 para o vermelho
        cv2.setTrackbarPos("V_max", "Filtros", 255)  # Ajuste V_max para 255 para o vermelho


cv2.destroyAllWindows()
