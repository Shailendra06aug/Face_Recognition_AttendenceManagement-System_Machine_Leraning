import cv2
import numpy as np
import csv
import cv2
import os
from datetime import datetime
import face_recognition

video_capture = cv2.VideoCapture(0)

amitabh_image = face_recognition.load_image_file("photos/amitabh.jpg")
amitabh_encoding = face_recognition.face_encodings(amitabh_image)[0]

monalisa_image = face_recognition.load_image_file("photos/monalisa.jpg")
monalisa_encoding = face_recognition.face_encodings(monalisa_image)[0]

ratanji_image = face_recognition.load_image_file("photos/ratanji.jpg")
ratanji_encoding = face_recognition.face_encodings(ratanji_image)[0]

shailendra_image = face_recognition.load_image_file("photos/shailendra.jpg")
shailendra_encoding = face_recognition.face_encodings(shailendra_image)[0]

known_face_encoding = [
    amitabh_encoding,
    monalisa_encoding,
    ratanji_encoding,
    shailendra_encoding
]

known_faces_names = [
    "amitabh",
    "monalisa",
    "ratan tata",
    "shailendra"
]

students = known_faces_names.copy()

face_locations = []
face_encodings = []
face_names = []
s = True

now = datetime.now()
current_date = now.strftime("%Y-%m-%d")

f = open(current_date + '.csv', 'w+', newline='')
lnwriter = csv.writer(f)

while True:
    _, frame = video_capture.read()
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    # rgb_small_frame = small_frame[:, :, ::-1]
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
    
    if s:
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encoding, face_encoding)
            name = ""
            face_distance = face_recognition.face_distance(known_face_encoding, face_encoding)
            best_match_index = np.argmin(face_distance)
            if matches[best_match_index]:
                name = known_faces_names[best_match_index]

            face_names.append(name)
            if name in known_faces_names:
                font = cv2.FONT_HERSHEY_SIMPLEX
                bottomLeftCornerOfText = (10, 100)
                fontScale = 1.5
                fontColor = (255, 0, 0)
                thickness = 3
                lineType = 2

                cv2.putText(frame, name + ' Present',
                            bottomLeftCornerOfText,
                            font,
                            fontScale,
                            fontColor,
                            thickness,
                            lineType)

                if name in students:
                    students.remove(name)
                    print(students)
                    current_time = now.strftime("%H-%M-%S")
                    lnwriter.writerow([name, current_time])
    cv2.imshow("attendence system", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
f.close()




