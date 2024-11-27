import cv2
import numpy as np
from matplotlib import pyplot as plt
import os

# Define o caminho da pasta onde o código está armazenado
current_directory = os.path.dirname(os.path.abspath(__file__))
folder_path = os.path.join(current_directory, '..', 'imgs') # local onde estão as imagens

# Pede ao usuário para digitar o nome da imagem no terminal
image_name = input("Digite o nome da imagem (com extensão, ex: imagem.jpg): ")
image_path = os.path.join(folder_path, image_name)

print(f"Tentando carregar a imagem de: {image_path}")

# Carrega a imagem em escala de cinza
image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

if image is None:
    print(f"Erro ao carregar a imagem: {image_name}. Verifique se o arquivo existe e o nome está correto.")
    exit()

# Aplica o desfoque Gaussiano e a detecção de bordas
blurred_image = cv2.GaussianBlur(image, (5, 5), 0)
edge_image = cv2.Canny(blurred_image, threshold1=55, threshold2=190)

# Exibe as imagens
plt.subplot(121), plt.imshow(image, cmap='gray')
plt.title('imagem original'), plt.xticks([]), plt.yticks([])

plt.subplot(122), plt.imshow(edge_image, cmap='gray')
plt.title('Imagem com detecção de bordas'), plt.xticks([]), plt.yticks([])

plt.show(block=True)
