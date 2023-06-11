import cv2
import numpy as np
import json as js

class my_dictionary(dict):
	def __init__(self):
		self = dict()
	def add(self, key, value):
		self[key] = value


class TestCase():
     
     def __init__(self,vid):
        # Create mask for red color
        self.low_red = np.array([150, 50, 50])
        self.high_red = np.array([180, 255, 255])
        self.kf = cv2.KalmanFilter(4, 2)
        self.kf.measurementMatrix = np.array([[1, 0, 0, 0], [0, 1, 0, 0]], np.float32)
        self.kf.transitionMatrix = np.array([[1, 0, 1, 0], [0, 1, 0, 1], [0, 0, 1, 0], [0, 0, 0, 1]], np.float32)
        self.cap = vid
        self.json = my_dictionary()
        self.dp ={}
        self.i=1

     def detect(self, frame):
        hsv_img = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Create masks with color ranges
        mask = cv2.inRange(hsv_img, self.low_red, self.high_red)

        # Find Contours
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)

        box = (0, 0, 0, 0)
        for cnt in contours:
            (x, y, w, h) = cv2.boundingRect(cnt)
            box = (x, y, x + w, y + h)
            break
        return box
     
     def predict(self,coordX, coordY):
          measured = np.array([[np.float32(coordX)], [np.float32(coordY)]])
          self.kf.correct(measured)
          predicted = self.kf.predict()
          x, y = int(predicted[0]), int(predicted[1])
          return x, y
     
     def output_data(self):
        while True:
            ret, frame = self.cap.read()
            if ret is False:
                break
            x, y, x2, y2 = self.detect(frame)
            cx = int((x + x2) / 2)
            cy = int((y + y2) / 2)
            predicted = self.predict(cx, cy)
            cv2.circle(frame, (cx, cy), 20, (0, 0, 255), 4)
            cv2.circle(frame, (predicted[0], predicted[1]), 20, (255, 0, 0), 4)
            self.json.add(f"Point{self.i}",predicted)
            self.dp.update({self.i:predicted})
            self.i+=1
        return self.dp
     
