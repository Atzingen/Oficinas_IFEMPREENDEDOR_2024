import cv2
import os

# Define o caminho da pasta onde o código está armazenado
current_directory = os.path.dirname(os.path.abspath(__file__))
folder_path = os.path.join(current_directory, '..', 'imgs') # local onde estão as imagens

# Pede ao usuário para digitar o nome da imagem no terminal
image_name = input("Digite o nome da imagem (com extensão, ex: imagem.jpg): ")
image_path = os.path.join(folder_path, image_name)

# Carrega a imagem a partir do caminho fornecido
frame = cv2.imread(image_path)

frame = cv2.resize(frame, (640, 480))

if frame is None:
    print(f"Erro ao carregar a imagem: {image_name}")
    exit()

# Converte a imagem para escala de cinza
frame_cinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

# Exibe a imagem inicial (colorida)
cv2.imshow('tela', frame)

# Variável para controlar o estado da imagem
modo_cinza = False

while True:
    # Alterna entre a imagem original e a cinza com base na tecla pressionada
    if modo_cinza:
        cv2.imshow('tela', frame_cinza)
    else:
        cv2.imshow('tela', frame)

    # Espera por uma tecla pressionada
    key = cv2.waitKey(1) & 0xFF
    
    # Se a tecla 'g' for pressionada, alterna para a imagem cinza
    if key == ord('g'):
        modo_cinza = True
    
    # Se a tecla 'n' for pressionada, volta para a imagem colorida (normal)
    elif key == ord('n'):
        modo_cinza = False

    # Se a tecla 'q' for pressionada, encerra o programa
    elif key == ord('q'):
        break

cv2.destroyAllWindows()
