import cv2
import dlib
import numpy as np
from imutils import face_utils

# Paths to the trained model files
predictor_path = "shape_predictor_68_face_landmarks.dat"
face_rec_model_path = "dlib_face_recognition_resnet_model_v1.dat"

# Initialize dlib's face detector and create facial landmark predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(predictor_path)
face_rec_model = dlib.face_recognition_model_v1(face_rec_model_path)

# Load known faces and their names
known_face_encodings = []
known_face_names = []


def load_known_faces(images_paths, names):
    global known_face_encodings, known_face_names
    for image_path, name in zip(images_paths, names):
        img = cv2.imread(image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)
        for face in faces:
            shape = predictor(gray, face)
            face_descriptor = face_rec_model.compute_face_descriptor(img, shape)
            known_face_encodings.append(np.array(face_descriptor))
            known_face_names.append(name)

def recognize_face():
    global name
    # Example paths and names (replace with your data)
    image_paths = ["merix.jpg"]  # Update with paths to known images
    names = ["Merix"]  # Update with names corresponding to the images
    load_known_faces(image_paths, names)

    # Initialize video capture
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = detector(gray_frame)

        for face in faces:
            shape = predictor(gray_frame, face)
            face_descriptor = face_rec_model.compute_face_descriptor(frame, shape)
            face_descriptor = np.array(face_descriptor)

            # Compare this face with known faces
            distances = []
            for known_face_encoding in known_face_encodings:
                distance = np.linalg.norm(face_descriptor - known_face_encoding)
                distances.append(distance)

            # Find the closest match
            if distances:
                min_distance = min(distances)
                if min_distance < 0.6:  # Threshold for matching (adjust as needed)
                    best_match_index = distances.index(min_distance)
                    name = known_face_names[best_match_index]
                else:
                    name = "Unknown"
            else:
                name = "Unknown"

            # Draw rectangle around face
            (x, y, w, h) = (face.left(), face.top(), face.right(), face.bottom())
            #cv2.rectangle(frame, (x, y), (w, h), (0, 255, 0), 2)

            # Draw facial landmarks
            shape = face_utils.shape_to_np(shape)
            for (x, y) in shape:
                cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)

            # Put text with the name
            cv2.putText(frame, name, (x + 6, y - 6), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)

        # Show the output frame
        cv2.imshow("Face Recognition", frame)
        break
        # Exit on 'ESC'
        #if cv2.waitKey(1) & 0xFF == 27:
        #    break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()
    try:
        return name
    except NameError:
        return "Unknown"