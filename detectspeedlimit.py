from streetview import googlestreetview
import preprocessing
import speedlimit
import sys, os


defaultpath = os.path.dirname(os.path.abspath(__file__))

def getdefaultlocations():
    """
    Default locations that have proven to show "decent" detection results to evaluate the cascade.xml provided
    :return: the array of locations in form : "lat,lng","heading"
    """
    return [
            ["52.5339344,13.2990433","87.32"],
            ["52.4327838,13.5005496","311.14"],
            ["48.1490762,11.5369588","359.58"],
            ["48.1241745,11.4916518","251.9"],
            ["51.2185806,6.7665308","180.59"],
            ["52.362024,4.8916571","208.16"],
            ["50.9593704,6.9634309","264.14"]
            ]

def detectspeedlimitonlocation():
    """
    User-assisted process of entering a location by street and city (plus optional arguments zip and country
    crawls the location from the google streetview api, presents detection results and saves the segment of the image including possible speed limits
    to disk
    :return: None
    """
    street = raw_input("Please provide a valid street name and number(no automated validation!):")
    city = raw_input("Please provide a valid city(no automated validation!):")
    zipOpt = raw_input("Please provide an OPTIONAL valid zip(no automated validation!):")
    countryOpt = raw_input("Please provide an OPTIONAL valid country(no automated validation!):")

    zipCode = None
    country = None

    if zipOpt !="":
        zipCode = zipOpt
    if countryOpt != "":
        country = countryOpt

    address = googlestreetview.buildLocationFromAddress(street,city,zipCode,country)
    print ("Querying street view for: " + address)

    imagepaths = googlestreetview.searchForSpeedLimitByLocation(defaultpath, address, 0)

    # detect speed limit signs
    for crawledimagepath in imagepaths:
        speed, img, gray = speedlimit.detectSpeedLimitSign(os.path.join(crawledimagepath[0],crawledimagepath[1]), 10)
        speedlimit.markAndShowDetectedSpeedLimits(speed, img)
        for (x,y,w,h) in speed:
            preprocessing.preprocessMultiple(crawledimagepath[0],crawledimagepath[1],x,y,(x+w),(y+h))

def detectspeedlimitondefault():
    """
    same as above, only takes predefined locations by lat,lng and heading
    see @getDefaultLocations
    :return:
    """
    defaults = getdefaultlocations()
    # path of the images written on disk within the current session
    imagepaths = []

    # crawl images
    for default in defaults:
        imagepath, imagename = googlestreetview.requestAndWriteImage(defaultpath,default[0],default[1],0)
        if imagepath != "" and imagename != "":
            imagepaths.append([imagepath, imagename])

    # detect speed limit signs
    for crawledimagepath in imagepaths:
        speed, img, gray = speedlimit.detectSpeedLimitSign(os.path.join(crawledimagepath[0], crawledimagepath[1]), 5)
        speedlimit.markAndShowDetectedSpeedLimits(speed, img)
        for (x,y,w,h) in speed:
            preprocessing.preprocessMultiple(crawledimagepath[0],crawledimagepath[1],x,y,(x+w),(y+h))

def detectspeedlimitonlocalpath(path, imagename):
    """
    given a local path and image name, detects, shows and saves speed limit signs
    :param path: the absolute pato of the FOLDER containing the image
    :param imagename: the image including datatype postfix, e.g. "image.png"
    :return: none
    """
    if not os.path.isfile(os.path.join(path, imagename)) or not os.path.isabs(path):
        print("Path " + str(os.path.join(path,imagename)) + " is not a valid absolute path")
    else:
        speed, img, gray = speedlimit.detectSpeedLimitSign(os.path.join(path,imagename), 15)
        speedlimit.markAndShowDetectedSpeedLimits(speed, img)
        for (x, y, w, h) in speed:
            preprocessing.preprocessMultiple(path, imagename, x, y, (x + w), (y + h))


def printusage(arg):
    print ("Python CLI Application to detect speed limitations based on google streetview images\n" \
          "Usage: %s manual -> to enter a location manually\n" \
          "       %s default -> to iterate over default locations\n" \
          "       %s path <your_img_path> <your_file_name> to inspect a locally available image" %(arg, arg, arg))



if __name__ == '__main__':
    if len(sys.argv) < 2:
        printusage(sys.argv[0])
    elif sys.argv[1] == "default":
        detectspeedlimitondefault()
    elif sys.argv[1] == "manual":
        detectspeedlimitonlocation()
    elif sys.argv[1] == "path" and len(sys.argv) == 4:
        detectspeedlimitonlocalpath(sys.argv[2], sys.argv[3])
    else:
        printusage(sys.argv[0])
