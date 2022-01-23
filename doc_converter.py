import cv2
import imutils 
from flatten_doc import doc_perspective_transform
from skimage.filters import threshold_local


def converter(image):
    
    #Resizing
    ratio = image.shape[0] / 720.
    original = image.copy()
    image = imutils.resize(image, height = 720)
    
    #Edge Detection Phase
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(gray, 75, 200)
    
    #Finding largest contour in edged map
    cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:5]
    
    for c in cnts:
        
        #Smoothening/approximating the contour
        perimeter = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * perimeter, True)
        
        if len(approx) == 4:
            screenCnt = approx
            break
    
    #Marking document outline
    cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 2)
    
    #Changing perespective of image
    warped_image = doc_perspective_transform(original, screenCnt.reshape(4, 2) * ratio)
    warped_image = cv2.cvtColor(warped_image, cv2.COLOR_BGR2GRAY)
    T = threshold_local(warped_image, 11, offset = 10, method = "gaussian")
    warped_image = (warped_image > T).astype("uint8") * 255
    
    warped_image = imutils.resize(warped_image, height = 720)
    warped_image = cv2.cvtColor(warped_image, cv2.COLOR_GRAY2BGR)
    
    return image, warped_image