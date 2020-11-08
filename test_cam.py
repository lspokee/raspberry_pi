from picamera import PiCamera
from time import sleep
import cv2 
import imutils

camera = PiCamera()
camera.start_preview()
sleep(5)
camera.capture('image.jpg')
camera.stop_preview()
   
#face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt_tree.xml')

# Read the input image
img = cv2.imread('image.jpg')
# Convert into grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# Detect faces
faces = face_cascade.detectMultiScale(gray, 1.1, 4)
# Draw rectangle around the faces
print(faces)
for (x, y, w, h) in faces:
    cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
# Display the output
cv2.imshow('img', img)
cv2.waitKey()