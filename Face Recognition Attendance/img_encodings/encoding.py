import face_recognition
import cv2
import os


def read_imgs(path):
    imgs = []
    labels = []

    for file in os.listdir(path):
        img = cv2.imread(f'{path}/{file}', cv2.COLOR_BGR2RGB)
        imgs.append(img)
        labels.append(file.split('.')[0].strip().upper())

    return imgs, labels


def find_encoding(imgs):
    encodings = []
    for img in imgs:
        encode = face_recognition.face_encodings(img)[0]
        encodings.append(encode)
    return encodings


def find_location_and_encoding(img):
    location = face_recognition.face_locations(img)
    encodings = face_recognition.face_encodings(img, location)
    return location, encodings


def find_location_and_distance(train_encodings, face_encoding):
    matches = face_recognition.compare_faces(train_encodings, face_encoding)
    distance = face_recognition.face_distance(train_encodings, face_encoding)
    return matches, distance
