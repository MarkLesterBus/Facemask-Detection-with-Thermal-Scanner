from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
from pyzbar.pyzbar import ZBarSymbol
from os.path import dirname, join
import pyzbar.pyzbar as pyzbar
from threading import Thread
from serial import Serial
import numpy as np
import pyttsx3
import imutils
import cv2



class VideoStream:
    Path = dirname(__file__) + '/face_detector/'
    protoPath = join(Path, "deploy.prototxt")
    weightsPath = join(Path, "res10_300x300_ssd_iter_140000.caffemodel")
    Model = join(Path, "mobilenet_v2.model")
    Facenet = cv2.dnn.readNetFromCaffe(protoPath, weightsPath)
    Masknet = load_model(Model)

    def __init__(self, src=0, url=''):
        if src == 0:
            self.stream = cv2.VideoCapture(src)
        if src == 1:
            self.stream = cv2.VideoCapture(url)
            self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        (self.grabbed, self.frame) = self.stream.read()
        self.stopped = False
        self.tts = pyttsx3.init()
        self.tts.setProperty('rate', 140)
        self.tts.setProperty('volume', 1.0)

    def start(self):
        Thread(target=self.get, args=()).start()
        return self

    def get(self):
        while not self.stopped:
            if not self.grabbed:
                self.stop()
            else:
                (self.grabbed, self.frame) = self.stream.read()

    def stop(self):
        self.stopped = True

    def resize(self):
        frame = imutils.resize(self.frame, width=760)
        return frame

    def draw(self, img, pt1, pt2, color, thickness, r, d):
        x1, y1 = pt1
        x2, y2 = pt2
        # Top left
        cv2.line(img, (x1 + r, y1), (x1 + r + d, y1), color, thickness)
        cv2.line(img, (x1, y1 + r), (x1, y1 + r + d), color, thickness)
        cv2.ellipse(img, (x1 + r, y1 + r), (r, r), 180, 0, 90, color, thickness)
        # Top right
        cv2.line(img, (x2 - r, y1), (x2 - r - d, y1), color, thickness)
        cv2.line(img, (x2, y1 + r), (x2, y1 + r + d), color, thickness)
        cv2.ellipse(img, (x2 - r, y1 + r), (r, r), 270, 0, 90, color, thickness)
        # Bottom left
        cv2.line(img, (x1 + r, y2), (x1 + r + d, y2), color, thickness)
        cv2.line(img, (x1, y2 - r), (x1, y2 - r - d), color, thickness)
        cv2.ellipse(img, (x1 + r, y2 - r), (r, r), 90, 0, 90, color, thickness)
        # Bottom right
        cv2.line(img, (x2 - r, y2), (x2 - r - d, y2), color, thickness)
        cv2.line(img, (x2, y2 - r), (x2, y2 - r - d), color, thickness)
        cv2.ellipse(img, (x2 - r, y2 - r), (r, r), 0, 0, 90, color, thickness)

    def predict(self, frame):
        # grab the dimensions of the frame and then construct a blob
        (h, w) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300), (104.0, 177.0, 123.0))

        VideoStream.Facenet.setInput(blob)
        detections = VideoStream.Facenet.forward()

        # initialize our list of faces, their corresponding locations and list of predictions
        faces = []
        locs = []
        preds = []

        for i in range(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]

            if confidence > 0.5:
                # we need the X,Y coordinates
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype('int')

                # ensure the bounding boxes fall within the dimensions of the frame
                (startX, startY) = (max(0, startX), max(0, startY))
                (endX, endY) = (min(w - 1, endX), min(h - 1, endY))

                # extract the face ROI, convert it from BGR to RGB channel, resize it to 224,224 and preprocess it
                face = frame[startY:endY, startX:endX]
                face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
                face = cv2.resize(face, (224, 224))
                face = img_to_array(face)
                face = preprocess_input(face)

                faces.append(face)
                locs.append((startX, startY, endX, endY))

        # only make a predictions if atleast one face was detected
        if len(faces) > 0:
            faces = np.array(faces, dtype='float32')
            preds = VideoStream.Masknet.predict(faces, batch_size=12)

        return (locs, preds)

    def process(self):
        # detect faces in the frame and preict if they are waring masks or not
        frame = self.resize()
        frame = cv2.flip(frame, 1)
        (locs, preds) = self.predict(frame)

        # loop over the detected face locations and their corrosponding loactions

        for (box, pred) in zip(locs, preds):
            (startX, startY, endX, endY) = box
            (mask, withoutMask) = pred

            # determine the class label and color we will use to draw the bounding box and text
            label = 'Mask' if mask > withoutMask else 'No Mask'
            color = (0, 255, 0) if label == 'Mask' else (0, 0, 255)

            # display the label and bounding boxes
            cv2.putText(frame, label, (startX, startY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 1)

            self.draw(frame, (startX, startY), (endX, endY), color, 1, 3, 10)
        return frame

    def detect_mask(self):
        label = []
        frame = self.resize()
        (locs, preds) = self.predict(frame)

        # loop over the detected face locations and their corrosponding loactions
        for (box, pred) in zip(locs, preds):
            (mask, withoutMask) = pred
            # determine the class label and color we will use to draw the bounding box and text
            label.append('Mask' if mask > withoutMask else 'No Mask')
        return label


    def detect_temp(self):
        data = ""
        sr = Serial('COM3', 9600)
        if sr.isOpen():
            data = sr.readline()
            data = data.strip()
            data = data.decode()
            sr.close()
        return data

    def detect_qr(self):
        data = ""
        result = pyzbar.decode(self.frame, symbols=[ZBarSymbol.QRCODE])
        for rs in result:
            if rs is not None:
                data = rs.data
                data = data.decode()
                data = str(data)
            else:
                data = ""
        return data



