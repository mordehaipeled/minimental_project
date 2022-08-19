# Importing Necessary Modules
import requests  # to get image from the web
import shutil  # to save it locally
import numpy as np
import argparse
from PIL import Image
import cv2
from matplotlib import pyplot as plt

# this page was ment to handel the img tests ... but we ended up not doing it.
def get_image_by_url(url):
    # filename = url.split("/")[-1]
    # Open the url image, set stream to True, this will return the stream content.
    r = Image.open(requests.get(url, stream=True).raw)
    # if r.status_code == 200:
    #     # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
    #     r.raw.decode_content = True

        # # Open a locale file with wb ( write binary ) permission.
        # with open(filename, 'wb') as f:
        #     shutil.copyfileobj(r.raw, f)

    #     print('Image sucessfully Downloaded: ', filename)
    # else:
    #     print('Image Couldn\'t be retreived')
    return r


def determine_shapes_in_img(img_url):
    img = get_image_by_url(img_url)
    print(img)
    img2 = cv2.imread(img)
    # converting image into grayscale image
    gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    # setting threshold of gray image
    _, threshold = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    # using a findContours() function
    contours, _ = cv2.findContours(
        threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    i = 0
    quadrilateral = False
    decagon = False
    # list for storing names of shapes
    for contour in contours:

        # here we are ignoring first counter because
        # findcontour function detects whole image as shape
        if i == 0:
            i = 1
            continue
        else:
            i = i + 1

        # cv2.approxPloyDP() function to approximate the shape
        approx = cv2.approxPolyDP(
            contour, 0.01 * cv2.arcLength(contour, True), True)

        # using drawContours() function
        cv2.drawContours(img, [contour], 0, (0, 0, 255), 5)

        # finding center point of shape
        M = cv2.moments(contour)
        if M['m00'] != 0.0:
            x = int(M['m10'] / M['m00'])
            y = int(M['m01'] / M['m00'])
            # putting shape name at center of each shape
            if len(approx) == 3:
                cv2.putText(img, 'Triangle', (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

            elif len(approx) == 4:
                cv2.putText(img, 'Quadrilateral', (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                quadrilateral = True

            elif len(approx) == 5:
                cv2.putText(img, 'Pentagon', (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

            elif len(approx) == 6:
                cv2.putText(img, 'Hexagon', (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

            elif len(approx) == 10:
                cv2.putText(img, 'decagon', (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                decagon = True
            else:
                cv2.putText(img, 'circle', (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    # displaying the image after drawing contours
    cv2.imshow('shapes', img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()