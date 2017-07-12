#import numpy as np
import os
import cv2
import csv

def detectSpeedLimitSign(imagepath, precision):
    speed_cascade = cv2.CascadeClassifier('cascade.xml')

    img = cv2.imread(imagepath)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    return speed_cascade.detectMultiScale(gray, 1.02, precision), img, gray



def markAndShowDetectedSpeedLimits(speed, img):
    for (x, y, w, h) in speed:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

    cv2.imshow('img', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def iterateOverDataset():
    path = os.path.dirname(os.path.abspath(__file__))

    for group in ('00000','00001', '00001', '00002', '00003', '00004', '00005', '00007', '00008'):
        with open(path + "/GTSRB/Final_Training/Images/" + group + "/GT-" + group + ".csv", "r") as csvfile:
            reader = csv.DictReader(csvfile, delimiter=";")
            for row in reader:
                temppath = path + "\\GTSRB\\Final_Training\\Images\\" + group + "\\" + row['Filename']
                speed, img, gray = detectSpeedLimitSign(temppath, 5)
                markAndShowDetectedSpeedLimits(speed, img)


if __name__ == '__main__':
    iterateOverDataset()
    #speed, img, gray = detectSpeedLimitSign(os.path.dirname(os.path.abspath(__file__)) + "\\streetview\\img.jpg")
    #markAndShowDetectedSpeedLimits(speed, img)
