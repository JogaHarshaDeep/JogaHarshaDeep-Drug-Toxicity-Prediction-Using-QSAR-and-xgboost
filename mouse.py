import cv2  
import mediapipe as mp  

# Initialize FaceMesh model
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh()

# Open webcam
cam = cv2.VideoCapture(0)

while cam.isOpened():  
    ret, frame = cam.read() 
    if not ret:
        break  

    frame = cv2.flip(frame, 1) 
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  
    output = face_mesh.process(rgb)  
    lm_points = output.multi_face_landmarks  

    frame_h, frame_w, _ = frame.shape  
    if lm_points:
        for face_landmarks in lm_points:
            for landmark in face_landmarks.landmark:
                x = int(landmark.x * frame_w)
                y = int(landmark.y * frame_h)
                cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)  

    cv2.imshow('Face Mesh', frame) 

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cam.release()
cv2.destroyAllWindows()
