import time

import cv2
import numpy as np

from csv_helper import csv
from img_encodings import encoding

path = 'student_imgs'
imgs, labels = encoding.read_imgs(path)

train_encodings = encoding.find_encoding(imgs)

frameWidth = 960
frameHeight = 720
frame_rate = 30

cap = cv2.VideoCapture(0)

prev = 0
RESIZE_FACTOR = 4

csv.initialize_csv()

while True:
    time_elapsed = time.time() - prev

    success, img = cap.read()

    if time_elapsed > 1. / frame_rate:
        prev = time.time()

        img_resized = cv2.resize(img.copy(), None, fx=1 / RESIZE_FACTOR, fy=1 / RESIZE_FACTOR)
        img_color = cv2.cvtColor(img_resized, cv2.COLOR_BGR2RGB)

        # find current face location and encodings
        face_location, face_encodings = encoding.find_location_and_encoding(img_color)

        # compare each face against the train_imgs
        for face_encode, face_loc in zip(face_encodings, face_location):
            matches, distance = encoding.find_location_and_distance(train_encodings, face_encode)
            best_index = np.argmin(distance)

            # if they exist
            if matches[best_index]:
                name = labels[best_index].upper()
                y1, x2, y2, x1 = list(map(lambda x: x * RESIZE_FACTOR, face_loc))
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 0, 255), cv2.FILLED)
                cv2.putText(img, name, (x1 + 5, y2 - 5), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 2)
                csv.mark_attendance(name)

        cv2.imshow('result', img)

    wait = cv2.waitKey(1)
    if wait & 0xFF == ord('q'):
        csv.prepare_final_report(labels)
        break

cv2.destroyAllWindows()
cap.release()
