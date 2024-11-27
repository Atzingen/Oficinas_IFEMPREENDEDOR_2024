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

cv2.namedWindow('tela')
cv2.createTrackbar('blur', 'tela', 1, 151, lambda x: None)  # Usando uma função vazia para a trackbar

while True:
    blur_par = cv2.getTrackbarPos('blur', 'tela')
    
    # O valor de blur precisa ser ímpar
    if blur_par % 2 == 0:
        blur_par += 1

    # Aplica o GaussianBlur na imagem carregada
    frame_blur = cv2.GaussianBlur(frame, (blur_par, blur_par), 0)
    
    # Exibe a imagem com blur
    cv2.imshow('tela', frame_blur)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
