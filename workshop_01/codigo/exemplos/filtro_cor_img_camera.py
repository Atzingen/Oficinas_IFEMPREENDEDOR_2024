import cv2
import numpy as np
import os

# Define the path to the folder where the image is stored
current_directory = os.path.dirname(os.path.abspath(__file__))
folder_path = os.path.join(current_directory, '..', 'imgs') # local onde estão as imagens

# Ask the user if they want to use an image or the camera
choice = input("Digite '1' para usar uma imagem ou '2' para usar a câmera: ")

# Initialize the frame based on the user's choice
if choice == '1':
    # Get the image name from the user if they choose to use an image
    image_name = input("Digite o nome da imagem (com extensão, ex: imagem.jpg): ")
    image_path = os.path.join(folder_path, image_name)
    
    # Load the image from the provided path
    frame = cv2.imread(image_path)

    if frame is None:
        print(f"Erro ao carregar a imagem: {image_name}")
        exit()

    frame = cv2.resize(frame, (640, 480))

elif choice == '2':
    # Use the camera (camera index 0)
    captura = cv2.VideoCapture(0)
    
    # Check if the camera was successfully opened
    if not captura.isOpened():
        print("Erro ao acessar a câmera.")
        exit()

    # Capture the first frame to get the frame size
    ret, frame = captura.read()
    if not ret:
        print("Erro ao capturar a imagem da câmera.")
        exit()

    frame = cv2.resize(frame, (800, 600))

else:
    print("Opção inválida.")
    exit()

# Convert the image to HSV color space
hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

# Create trackbars for adjusting the color range
cv2.namedWindow('Filtros')
cv2.createTrackbar("H_min", "Filtros", 0, 179, lambda x: None)
cv2.createTrackbar("S_min", "Filtros", 0, 255, lambda x: None)
cv2.createTrackbar("V_min", "Filtros", 0, 255, lambda x: None)
cv2.createTrackbar("H_max", "Filtros", 179, 179, lambda x: None)
cv2.createTrackbar("S_max", "Filtros", 255, 255, lambda x: None)
cv2.createTrackbar("V_max", "Filtros", 255, 255, lambda x: None)

while True:
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # Get the values of the trackbars
    h_min = cv2.getTrackbarPos("H_min", "Filtros")
    s_min = cv2.getTrackbarPos("S_min", "Filtros")
    v_min = cv2.getTrackbarPos("V_min", "Filtros")
    h_max = cv2.getTrackbarPos("H_max", "Filtros")
    s_max = cv2.getTrackbarPos("S_max", "Filtros")
    v_max = cv2.getTrackbarPos("V_max", "Filtros")

    # Define the color bounds
    lower_bound = np.array([h_min, s_min, v_min])
    upper_bound = np.array([h_max, s_max, v_max])

    # Create a mask to filter the image
    mask = cv2.inRange(hsv_frame, lower_bound, upper_bound)
    filtered_image = cv2.bitwise_and(frame, frame, mask=mask)

    # Show the filtered image
    cv2.imshow('Filtros', filtered_image)

    # Wait for a key press
    key = cv2.waitKey(1) & 0xFF
    
    # If 'q' is pressed, exit the program
    if key == ord('q'):
        break
    # If 'b' is pressed, reset values for blue
    elif key == ord('b'):
        cv2.setTrackbarPos("H_min", "Filtros", 96)
        cv2.setTrackbarPos("S_min", "Filtros", 148)
        cv2.setTrackbarPos("V_min", "Filtros", 0)
        cv2.setTrackbarPos("H_max", "Filtros", 120)
        cv2.setTrackbarPos("S_max", "Filtros", 255)
        cv2.setTrackbarPos("V_max", "Filtros", 255)

    # If 'g' is pressed, reset values for green
    elif key == ord('g'):
        cv2.setTrackbarPos("H_min", "Filtros", 21)
        cv2.setTrackbarPos("S_min", "Filtros", 85)
        cv2.setTrackbarPos("V_min", "Filtros", 0)
        cv2.setTrackbarPos("H_max", "Filtros", 79)
        cv2.setTrackbarPos("S_max", "Filtros", 255)
        cv2.setTrackbarPos("V_max", "Filtros", 255)

    # If 'r' is pressed, reset values for red
    elif key == ord('r'):
        cv2.setTrackbarPos("H_min", "Filtros", 0)
        cv2.setTrackbarPos("S_min", "Filtros", 63)
        cv2.setTrackbarPos("V_min", "Filtros", 0)
        cv2.setTrackbarPos("H_max", "Filtros", 28)
        cv2.setTrackbarPos("S_max", "Filtros", 255)
        cv2.setTrackbarPos("V_max", "Filtros", 255)

    # If 'n' is pressed, reset the values to default
    elif key == ord('n'):
        cv2.setTrackbarPos("H_min", "Filtros", 0)
        cv2.setTrackbarPos("S_min", "Filtros", 0)
        cv2.setTrackbarPos("V_min", "Filtros", 0)
        cv2.setTrackbarPos("H_max", "Filtros", 255)
        cv2.setTrackbarPos("S_max", "Filtros", 255)
        cv2.setTrackbarPos("V_max", "Filtros", 255)

    elif key == ord('v'):
        if choice=='2':
            _, frame = captura.read()


# Close all OpenCV windows
cv2.destroyAllWindows()
if choice == '2':
    captura.release()
