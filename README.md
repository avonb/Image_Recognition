# Image_Recognition

## Requirements

### basic module (without google street view extension)
 
* Python 2.7.x
* Python Image Library (PIL) -> http://www.pythonware.com/products/pil/

### street view extension

* Python Requests -> http://docs.python-requests.org/en/master/
```bash
python -m pip install requests
```
* Python OpenCV Interface (provides basic functionalities)
```bash
python -m pip install opencv-python
```
this will also install other required libraries if not available yet (e.g. numpy)


## Setup on local machine:

1. Download/Clone Repo
2. Download Training Data Set -> http://benchmark.ini.rub.de/?section=gtsrb&subsection=dataset#Downloads (Images and annotations [84MB])
3. unzip into Repositories Folder "GTSRB", so that the following is a valid path: 
[...]/ImageRecognition/GTSRB/Final_Training/Images/<all the image classes/sub-folders available here
4. preprocess the images (make sure to be in the root directory of the project "/ImageRecognition":
```bash
python ./preprocess.py
```
* This will ultimatively generate grayscale images from the first 8 classes   
5. run the provided r script "sign_recognition.r" -> main block provided at the end

## Using the street view extension

1. Acquire an API-Key from google -> https://developers.google.com/maps/documentation/streetview/?hl=de
* Don't worry: up to 2.500 downloads are for free! If you exceed that limit, google will simply block your IP for one day (no, that totally did *NOT* happen to us!)
2. Enter the obtained Key in streetview/googlestreetview.py -> global variable "apikey"
* If you object to steps 1. and 2., google may block your IP already after ~100 request for a longer time than 1 day (did not try that ourselves)
3. Run it!:
```bash
python ./detectspeedlimit.py <option>
```
* various operations are supported (therefore, you need to specify <option>)  
if you just execute without \<option\>, information on the detailled usage, and what to specify for \<option\> is displayed


##
