import cv2
import numpy as np
from keras.models import load_model

classifier = load_model(r'D:\CODES\satis-face-tion\ai_trained_model\model.h5')
emotion_labels = ['Unsatisfied', 'Unsatisfied', 'Satisfied', 'Satisfied', 'Unsatisfied', 'Satisfied']
count = 0

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    labels = []
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    face_classifier = cv2.CascadeClassifier(r'D:\CODES\satis-face-tion\ai_trained_model\haarcascades\haarcascade_frontalface_default.xml')
    faces = face_classifier.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 255), 2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_gray = cv2.resize(roi_gray, (48, 48), interpolation=cv2.INTER_AREA)

        if np.sum([roi_gray]) != 0:
            roi = roi_gray.astype('float') / 255.0
            roi = np.expand_dims(roi, axis=0)
            prediction = classifier.predict(roi)[0]
            label = emotion_labels[prediction.argmax()]
            label_position = (x, y)
            cv2.putText(frame, label, label_position, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Check satisfaction level and save image
            if label == 'Satisfied':
                print("Satisfied!")
                filename = f'/d/CODES/satis-face-tion/Person/satisfied_{count}.jpg'
            else:
                print("Unsatisfied!")
                filename = f'/d/CODES/satis-face-tion/Person/unsatisfied_{count}.jpg'

            cv2.imwrite(filename, frame)
            count += 1

        else:
            cv2.putText(frame, 'No Faces', (30, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow('Emotion Detector', frame)

    if not ret:
        break

    k = cv2.waitKey(1)

    if k % 256 == 27:
        print("Close")
        break

cap.release()
cv2.destroyAllWindows()
