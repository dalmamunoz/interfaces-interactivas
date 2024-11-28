import cv2
import mediapipe as mp
import random
import time  # Para usar el temporizador

# Inicialización de MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_draw = mp.solutions.drawing_utils

# Función para contar los dedos levantados
def contar_dedos(landmarks):
    dedos = 0
    # Accede a los puntos de referencia usando su índice en lugar de como si fuera un diccionario
    if landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y < landmarks.landmark[mp_hands.HandLandmark.THUMB_MCP].y:
        dedos += 1
    if landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y < landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].y:
        dedos += 1
    if landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y < landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y:
        dedos += 1
    if landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y < landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP].y:
        dedos += 1
    if landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y < landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP].y:
        dedos += 1
    return dedos

# Inicializar cámara
cap = cv2.VideoCapture(0)

# Generar un número aleatorio entre 1 y 10 (o el rango que prefieras)
numero = random.randint(1, 10)
print(f"El número es: {numero}")

# Temporizador para esperar antes de cambiar el número
espera = False
tiempo_espera = 0  # Variable para controlar el tiempo de espera

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Convierte la imagen a RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Procesa la imagen para detectar las manos
    results = hands.process(frame_rgb)
    
    dedos_levantados = 0
    
    # Verifica cuántas manos se han detectado
    if results.multi_hand_landmarks:
        for landmarks in results.multi_hand_landmarks:
            # Cuenta los dedos levantados para cada mano detectada
            dedos_levantados += contar_dedos(landmarks)
            # Dibuja las marcas de los dedos
            mp_draw.draw_landmarks(frame, landmarks, mp_hands.HAND_CONNECTIONS)
    
    # Muestra el número en la pantalla
    cv2.putText(frame, f"Número mostrado: {numero}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    # Muestra la cantidad de dedos levantados
    cv2.putText(frame, f"Dedos levantados: {dedos_levantados}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    # Validación de la respuesta
    if dedos_levantados == numero:
        cv2.putText(frame, "¡Muy bien!", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        if not espera:
            tiempo_espera = time.time()  # Inicia el temporizador
            espera = True
    else:
        cv2.putText(frame, "Intenta de nuevo", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    
    # Verificar si se ha alcanzado el tiempo de espera
    if espera and time.time() - tiempo_espera >= 5:  # Espera de 2 segundos
        # Generar un nuevo número y reiniciar la espera
        numero = random.randint(1, 10)
        espera = False
    
    # Muestra la imagen
    cv2.imshow("Juego de Contar y Representar Números", frame)
    
    # Salir con la tecla ESC
    if cv2.waitKey(1) & 0xFF == 27:
        break

# Libera la cámara
cap.release()
cv2.destroyAllWindows()
