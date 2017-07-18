import requests
import shutil
import os

########################################################
####                                                ####
####        Before beginning the crawling, an API   ####
####        key has to be requested by google and   ####
####        passed to the glob. variable "apiKey"   ####
####                                                ####
########################################################


apikey = ""
baseURL = "https://maps.googleapis.com/maps/api/streetview"
metaURL = baseURL + "/metadata"

# do ONLY call with meta URL!
def checkStreetviewImageAvailability(location, heading, pitch):
    """
    Takes a location heading and pitch and checks whether there is a google streetview image available
    :param location: String build by either @buildLocationFromCoordinates or @buildLocationFromAddress
    :param heading: cardinal direction
                    0/360: north
                    90:east
                    180: south
                    270:west
    :param pitch: change facing upwards or downwards (recommendation: 0)
    :return: True if there was an image available, False if not (console prints error)
    """
    url = metaURL + "?size=600x300&location=" + location + "&heading=" + str(heading) + "&pitch=" + str(pitch) + "&key=" +apikey
    print(url)
    try:
        response = requests.get(url)
        if response.status_code == requests.codes.ok:
            if response.json()['status'] == "OK":
                print response.json()
                return True
            else:
                print("Google returned the following Error:" + response.json()['status'])
                return False
        else:
            print("Error, the request returned the following status-code:" + str(response.status_code))
            return False
    except:
        print("Error, the request could not be executed! Most likely, there was no JSON Object to decode")
        return False


def requestAndWriteImage(path, location, heading, pitch):
    """
    Takes a path (disk), location and additional parameters to crawl a location's streetview and saves it to disk
    :param path: path on local disk where to vace the image (a sub directory crawledImages will be crated)
    :param location: String build by either @buildLocationFromCoordinates or @buildLocationFromAddress
    :param heading: cardinal direction
                    0/360: north
                    90:east
                    180: south
                    270:west
    :param pitch: change facing upwards or downwards (recommendation: 0)
    :return: True/False as feedback for operation success
    """


    url = baseURL + "?size=600x300&location=" + location + "&heading=" + str(heading) + "&pitch=" + str(pitch) + "&key=" +apikey
    #url2 = "https://maps.googleapis.com/maps/api/streetview?size=600x300&location=52.5339344,13.2990433&heading=87.32&pitch=-0.76&key=" + apikey
    #url = "https://maps.googleapis.com/maps/api/streetview?size=600x300&location=Friedrichstrasse 78, Berlin, Germany&key=" + apikey
    imagepath = ""
    imagename = ""
    # check image availability
    if checkStreetviewImageAvailability(location, heading, pitch):
        try:
            response = requests.get(url, stream=True)
            if response.status_code == requests.codes.ok:
                print ("Status Code == 200")
                #make sure directoy exists
                if not os.path.exists(os.path.join(path, 'crawledImages')):
                    os.makedirs(os.path.join(path, 'crawledImages'))
                imagepath = os.path.join(path,'crawledImages')
                imagename = locationToImgFileName(location, heading) + '.jpg'
                with open(os.path.join(imagepath, imagename), 'wb') as out_file:
                    shutil.copyfileobj(response.raw, out_file)
            del response
            print ("Done")
            return imagepath, imagename
        except:
            print("An error occurred processing the request")
            return "", ""
    else:
        return "", ""

def searchForSpeedLimitByLocation(path, location, pitch):
    """
    :param path: the path where to save the images
    :param location: String build by either @buildLocationFromCoordinates or @buildLocationFromAddress
    :param pitch: change facing upwards or downwards (recommendation: 0)
    :return: image names that were saved
    """
    images = []
    # all major cardinal directions
    for heading in [0, 90, 180, 270]:
        imagepath, imagename = requestAndWriteImage(path, location, heading, pitch)
        if imagepath != "" and imagename != "":
            images.append([imagepath, imagename])
    return images


def buildLocationFromAddress(street, city, zip=None, state=None):
    """
    builds an address string google can interprete by given substrings (simply comma separated)
    :param street: street
    :param city: city
    :param zip: zip
    :param state: state
    :return: concatenated string
    """
    location = street + ", " + city
    if zip is not None:
        location = location + ", " + zip
    if state is not None:
        location = location + ", " + state
    return location

def buildLocationFromCoordinates(lat, lng):
    return lat + "," + lng

def locationToImgFileName(locationString, heading):
    """
    helper method to build a valid filename from given parameters
    :param locationString: concatenated string by @buildLocationFromAddress
    :param heading: cardinal direction
    :return: filename that is valid
    """
    return "loc_" + locationString.replace(",", "_").replace(".", "_").replace(" ", "") + "head_" + str(heading).replace(".","")


