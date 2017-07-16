import csv
import os
import shutil
import numpy as np

########################################################
####                                                ####
####        Helper script to create the required    ####
####        positive image file for opencv by given ####
####        GTSRB street sign images                ####
####        path has to be adjusted...              ####
####                                                ####
########################################################


path = os.path.dirname(os.path.abspath(__file__))
with open (path + "/info.txt", "w") as infofile:

    for group in ('00000','00001','00002','00003','00004','00005','00007','00008'):
        with open (path + "/GTSRB/Final_Training/Images/" + group + "/GT-" + group +".csv", "r") as csvfile:

            #i=0

            readertemp = csv.reader(csvfile, delimiter=",")
            data = list(readertemp)
            #retrieve length of data tranche
            row_count = len(data) -1
            #print row_count
            probability = float(200)/float(row_count)
            #print probability
            #print(np.random.binomial(1, probability,1))
            #mandatory file reset
            csvfile.seek(0)
            reader = csv.DictReader(csvfile, delimiter=";")
            for row in reader:
                #print("row")
                Y = int(np.random.binomial(1, probability, 1))
            #    #pre = (row['Filename'][0:4])
            #    #post = int(row['Filename'][6:10])
                #Y.__contains__(1)
                if Y == 1:
                    #print("ok")
                    infofile.write("PositiveImagesSpeedLimit\\" + group + "_" + row['Filename'] +" 1 "+ row['Roi.X1'] + " " + row['Roi.Y1'] + " " + row['Width'] + " " + row['Height'] + "\n" )
                    shutil.copy(path+"/GTSRB/Final_Training/Images/" + group +"/" + row['Filename'], path + "/PositiveImagesSpeedLimit/" + group + "_" + row['Filename'])
            #    i=i+1

