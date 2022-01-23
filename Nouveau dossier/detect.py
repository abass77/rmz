try:
    from PIL import Image
except ImportError:
    import Image
import argparse
import cv2
import imutils
import numpy as np
import pandas as pd
import pytesseract
from imutils import paths


a = [1, 7, 2]

myvar = pd.Series(a, index = ["x", "y", "z"])

print(myvar)

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


# argument pour les lignes de commandes
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--images", required=True, help="path to images directory")
args = vars(ap.parse_args())


# initialisation du rectangle de kernel
rectKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (16,7 ))
sqKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 21))

# quelques modification sur les images path
for imagePath in paths.list_images(args["images"]):
    # charger image,le redimentionner,conversion en gray
    image = cv2.imread(imagePath)
    image = imutils.resize(image, height=600)
    image= cv2.medianBlur(image, 1)
    # image=cv2.threshold(image, 200, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    #image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY )
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


    # lisser l’image à l’aide d’un gaussien 3x3, puis appliquer le chapeau noir
    # opérateur morphologique pour trouver des régions sombres sur un fond clair
    gray = cv2.GaussianBlur(gray, (3, 3), 0)
    black_hat = cv2.morphologyEx(gray, cv2.MORPH_BLACKHAT, rectKernel)

    # calculer le dégradé scharr de l’image du chapeau noir et mettre à l’échelle le
    # résultat dans la plage [0, 255]

    gradX = cv2.Sobel(black_hat, ddepth=cv2.CV_32F, dx=1, dy=0, ksize=-1)
    gradX = np.absolute(gradX)
    (minVal, maxVal) = (np.min(gradX), np.max(gradX))
    gradX = (255 * ((gradX - minVal) / (maxVal - minVal))).astype("uint8")

    # appliquer une opération de fermeture à l’aide du noyau rectangulaire pour fermer
    # intervalles entre les lettres - puis appliquez la méthode de seuil d’Otsu]

    gradX = cv2.morphologyEx(gradX, cv2.MORPH_CLOSE, rectKernel)
    thresh = cv2.threshold(gradX, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    # effectuer une autre opération de fermeture, cette fois en utilisant le carré
    # noyau pour fermer les espaces entre les lignes de la MRZ, puis effectuer un
    # série d’érosion pour briser les composants connectés

    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, sqKernel)
    thresh = cv2.erode(thresh, None, iterations=4)

    # pendant le seuil, il est possible que les pixels de bordure aient été
    # inclus dans le seuil, alors définissons 5% de la gauche et
    # bordures droites à zéro

    p = int(image.shape[1] * 0.05)
    thresh[:, 0:p] = 0
    thresh[:, image.shape[1] - p:] = 0

    # trouver des contours dans l’image de seuil et les trier en par leur taille
    contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)[-2]
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    # boucle sur les contours
    for c in contours:
        # calculer le cadre de sélection du contour et utiliser le contour pour
        # calculer le rapport d’aspect et le rapport de couverture du cadre de sélection
        # largeur à la largeur de l’image
        (x, y, w, h) = cv2.boundingRect(c)
        ar = w / float(h)
        crWidth = w / float(gray.shape[1])

        # vérifier si le rapport d’aspect et la largeur de couverture sont dans
        # critères acceptables
        if ar > 5 and crWidth > 0.75:
            # tamponner le cadre de délimitation puisque nous avons appliqué l’érosion et que nous avons maintenant besoin
            # pour le faire repousser
            pX = int((x + w) * 0.03)
            pY = int((y + h) * 0.03)
            (x, y) = (x - pX, y - pY)
            (w, h) = (w + (pX * 2), h + (pY * 2))

            # extraire le retour sur investissement de l’image et dessiner un cadre de sélection
            # autour de la MRZ
            roi = image[y:y + h, x:x + w].copy()
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            break

    # show the output images
    cv2.imshow("Image", image)

    texte = pytesseract.image_to_string(roi)

    textes= texte.split("\n")

    print(roi)

    newlist = [x for x in textes if "<" in x or "NIN" in x]

    newlist="".join(str(x) for x in newlist)

    newlist=newlist.split("<")

    newlist = [i for i in newlist if i != '']

    chaine="".join(newlist)

    print(newlist)
    mydataset = {
              'NIN': ["BMW", "Volvo", "Ford"],
              'cor': [3, 7, 2]
    }
    myvar = pd.DataFrame(mydataset)

    #print(myvar)
    cv2.imshow("ROI", roi)
    cv2.waitKey(0)
