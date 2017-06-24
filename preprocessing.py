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

def equalize2(image):
    h = image.histogram()
    colors = []
    h2=[]
    for b in range(0, len(h), 256):
        n = sum(h[b:b+256]) / 256 #eigentlich kein teilen
        h2.append(h[0]/n)
        for i in range(256)[1:256]:
            h2.append(h[i+b]/n)
            h2[i+b] = h2[i+b] + h2[i-1+b]
            colors.append(h2[i+b]) #eigentlich *256, aber stattdessen oben teilen
        print h2

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


def preprocess(clazz):
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

            im = im.filter(ImageFilter.SMOOTH_MORE)
            #print "Smoothed: " + row['Filename']
            save(path, row, im, "smooth")

            im = im.convert("L")
            #print "Reduced colors: " + row['Filename']
            save(path, row, im, "grey", filetype = "pgm")

for i in range(0, 6):
    preprocess(i)
