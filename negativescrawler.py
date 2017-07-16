from streetview import googlestreetview
import os

########################################################
####                                                ####
####        Helper script to crawl ~1000 images     ####
####        which possibly do not include street    ####
####        signs to train the cascade              ####
####                                                ####
########################################################

path = os.path.dirname(os.path.abspath(__file__))




locations = []

# Berlin Locations

locations.append("1 Friedrichstrasse, Berlin")
for i in range(5, 151,5):
    locations.append(str(i) + " Friedrichstrasse, Berlin")

# Duesseldorf Locations

locations.append("1 Koenigsallee, Duesseldorf")
for i in range(5, 151,5):
    locations.append(str(i) + " Koenigsallee, Duesseldorf")

# Hamburg Locations


locations.append("1 St. Pauli Hafenstrasse, Hamburg")
for i in range(5, 121,5):
    locations.append(str(i) + " St. Pauli Hafenstrasse, Hamburg")

# Koeln Locations

locations.append("1 Aachener Strasse, Koeln")
for i in range(5, 401,5):
    locations.append(str(i) + " Aachener Strasse, Koeln")

locations.append("1 Innere Kanalstrasse, Koeln")
for i in range(5, 401,5):
    locations.append(str(i) + " Innere Kanalstrasse, Koeln")

for location in locations:
    print location

print len(locations)
images = []
for location in locations:
    images.append(googlestreetview.searchForSpeedLimitByLocation(path, location, 0))

with open (path + "/negativetrain.txt", "w") as infofile:
    for img in images:
        infofile.write(str(os.path.join(img[0], img[1])))

