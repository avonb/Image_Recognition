#import numpy as np
import os
import cv2
import csv

def detectSpeedLimitSign(imagepath, precision):
    """
    Provide your trained cascade here
    takes an image from ABSOLUTE path (bug in cv2 for windows -> relative paths not working...)
    and converts it to grayscale image, performs detection
    :param imagepath: path to the image
    :param precision: given threshhold to separate true/false positives, indicates
                      the number of neighbours that have to be present ("true" pattern machings) in the search tree
                      to identify an object
    :return:
    """
    speed_cascade = cv2.CascadeClassifier('cascade.xml')

    img = cv2.imread(imagepath)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    return speed_cascade.detectMultiScale(gray, 1.02, precision), img, gray



def markAndShowDetectedSpeedLimits(speed, img):
    """
    shows detected rectangles ("areas that are supposed to hold the desired object")
    :param speed: the numpy array to hold coordinates of the rectangle
    :param img: the image itself
    :return:
    """
    for (x, y, w, h) in speed:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

    cv2.imshow('img', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def iterateOverDataset():
    """
    method for testing purposes to see how many of the provided GTSRB images are correctly "detected"
    please adjust the path!
    :return:
    """
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
