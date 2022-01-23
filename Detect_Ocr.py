# import the necessary packages
from imutils.contours import sort_contours
import numpy as np
import pytesseract
import argparse
import imutils
import sys
import cv2
import json
import jsonpickle
from flask import Flask, request, Response



image = cv2.imread("Capture.PNG")
image = cv2.resize(image, (1000, 450))
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
(H, W) = gray.shape
# initialize a rectangular and square structuring kernel
rectKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 7))
sqKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 21))
# smooth the image using a 3x3 Gaussian blur and then apply a
# blackhat morpholigical operator to find dark regions on a light
# background
gray = cv2.GaussianBlur(gray, (3, 3), 0)
blackhat = cv2.morphologyEx(gray, cv2.MORPH_BLACKHAT, rectKernel)
cv2.imshow("Blackhat", blackhat)

# compute the Scharr gradient of the blackhat image and scale the
# result into the range [0, 255]
grad = cv2.Sobel(blackhat, ddepth=cv2.CV_32F, dx=1, dy=0, ksize=-1)
grad = np.absolute(grad)
(minVal, maxVal) = (np.min(grad), np.max(grad))
grad = (grad - minVal) / (maxVal - minVal)
grad = (grad * 255).astype("uint8")
cv2.imshow("Gradient", grad)

# apply a closing operation using the rectangular kernel to close
# gaps in between letters -- then apply Otsu's thresholding method
grad = cv2.morphologyEx(grad, cv2.MORPH_CLOSE, rectKernel)
thresh = cv2.threshold(grad, 0, 255,
                       cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
cv2.imshow("Rect Close", thresh)
# perform another closing operation, this time using the square
# kernel to close gaps between lines of the MRZ, then perform a
# series of erosions to break apart connected components
thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, sqKernel)
thresh = cv2.erode(thresh, None, iterations=2)
cv2.imshow("Square Close", thresh)

# find contours in the thresholded image and sort them from bottom
# to top (since the MRZ will always be at the bottom of the passport)
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                        cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
cnts = sort_contours(cnts, method="bottom-to-top")[0]
# initialize the bounding box associated with the MRZ
mrzBox = None

# loop over the contours
for c in cnts:
    # compute the bounding box of the contour and then derive the
    # how much of the image the bounding box occupies in terms of
    # both width and height
    (x, y, w, h) = cv2.boundingRect(c)
    percentWidth = w / float(W)
    percentHeight = h / float(H)
    # if the bounding box occupies > 80% width and > 4% height of the
    # image, then assume we have found the MRZ
    if percentWidth > 0.8 and percentHeight > 0.04:
        mrzBox = (x, y, w, h)
        break

# if the MRZ was not found, exit the script
if mrzBox is None:
	print("[INFO] MRZ could not be found")
	sys.exit(0)
# pad the bounding box since we applied erosions and now need to
# re-grow it
(x, y, w, h) = mrzBox
pX = int((x + w) * 0.03)
pY = int((y + h) * 0.03)
(x, y) = (x - pX, y - pY)
(w, h) = (w + (pX * 2), h + (pY * 2))
# extract the padded MRZ from the image
mrz = image[y:y + h, x:x + w]



# OCR the
# MRZ region of interest using Tesseract, removing any
# occurrences of spaces

mrzText = pytesseract.image_to_string(mrz)


#texte = pytesseract.image_to_string(mrz)
#texte= texte.split("\n")
# print(textes)
# newlist = [x for x in textes if "<" in x or "NIN" in x]
# print(newlist)
# newlist="".join(str(x) for x in newlist)

# newlist=newlist.split("<")
# newlist = [i for i in newlist if i != '']

# chaine="".join(newlist)

# print(newlist)

mrzText = mrzText.replace (' ', '')

print(mrzText)
mrzText = mrzText.replace ('<<', '#')
print('Après replace de << par # :')
print(mrzText)
mrzText=mrzText.replace ('\n', '#')
print('Après replace de \\n par # :')
print(mrzText)
x = filter(None,mrzText.split("#"))
print('Après split et filter :')
mrz_list = list(x)
print(mrz_list)
mrz_list[0] = mrz_list[0].replace ('<', ' ')
mrz_list[4] = mrz_list[4].replace ('<', ' ')
mrz_list[3] = mrz_list[3].replace ("'", "")
mrz_list[0] = mrz_list[0].replace (" ", "")
mrz_list_0 = mrz_list[0]
mrz_list[0] = mrz_list_0[1:len(mrz_list_0)-1]
mrz_list_1=mrz_list[1]

print("A la fin:")
print(mrz_list_1[:6])
print(mrz_list_1[7])
print(mrz_list_1[8:14])
print(mrz_list_1[15:18])
print(mrz_list[0])
print(mrz_list[1])
print(mrz_list[2])
print(mrz_list[3])
print(mrz_list[4])


# show the MRZ image
cv2.imshow("MRZ", mrz)
cv2.waitKey(0)