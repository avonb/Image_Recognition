import csv
import os
import operator

from PIL import Image
from PIL import ImageFilter

def getClass(num):
    if(num < 10):
        return "0000" + str(num)
    else:
        return "000" + str(num)

def resize(data, image ,height, width):
    area = map(float,(data['Roi.X1'],data['Roi.Y1'],data['Roi.X2'],data['Roi.Y2']))
    cropim = image.crop(area)
    out = cropim.resize((height,width))
    return out

#runs histogram equalization
def equalize(image):

    h = image.histogram()
    colors = []

    for b in range(0, len(h), 256):
        step = reduce(operator.add, h[b:b+256]) / 256

        n = 0
        for i in range(256):

            colors.append(n / step)
            n = n + h[i+b]

    return image.point(colors)

def save(path, data, image, step, filetype = None):
    img_path = path + '/' + step
    if not os.path.exists(img_path):
        os.makedirs(img_path)

    name = data['Filename']
    if filetype == "pgm":
        name = name[:-4] + ".pgm"

    image.save(img_path + '/' + name)


#Prepocess all images a class
def preprocess(clazz):
    #configure path
    path = os.path.dirname(os.path.abspath(__file__))
    path = path + "/GTSRB/Final_Training/Images/" + getClass(clazz)
    csv_file = "GT-"+getClass(clazz)+".csv"
    print "Preprocessing class " + getClass(clazz)

    with open(path + '/' + csv_file, 'rb') as dataoverview:
        reader = csv.DictReader(dataoverview, delimiter=';')
        for row in reader:
            im = Image.open(path + '/' + row['Filename'])

            im = resize(row, im, 40, 40)
            #print "Resized: " + row['Filename']
            save(path, row, im, "resize")

            im = equalize(im)
            #print "Equalized: " + row['Filename']
            save(path, row, im, "equalize")

            #adds smoothing
            im = im.filter(ImageFilter.SMOOTH_MORE)
            #print "Smoothed: " + row['Filename']
            save(path, row, im, "smooth")

            #converts image to greyscale
            im = im.convert("L")
            #print "Reduced colors: " + row['Filename']
            save(path, row, im, "grey", filetype = "pgm")

for i in range(1, 8):
    preprocess(i)
