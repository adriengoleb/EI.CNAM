# %%
import pytesseract as tess
from PIL import Image
import glob
tess.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
listeChemin = glob.glob("C:/Users/youssef.balti/Desktop/CNAM/Deuxieme_Annee/Donnees_temporelles_et_spatiales/Projet/General/General/Fichier_de_donnees/Passeport_interieur/*.jpg")
import cv2

for i in range(len(listeChemin)):
    img = cv2.imread(listeChemin[i])
    img = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
    #_, result = cv2.threshold(img,35,255,cv2.THRESH_BINARY)
    #result = cv2.adaptiveThreshold(img,155,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,81,4)
    result = cv2.threshold(img,0,255,cv2.THRESH_OTSU)
    #print('Original Dimensions : ', img.shape)
    scale_percent = 500  # percent of ori ginal size
    width = int(result.shape[1] * scale_percent / 100)
    height = int(result.shape[0] * scale_percent / 100)
    dim = (width, height)
    resized = cv2.cv2.resize(result, dim)
    #print('Resized Dimensions : ', resized.shape)
    cv2.imshow('Result', resized)
    cv2.waitKey(1000)
    text = tess.image_to_string(resized)
    if "PCBEL" in text or "P<BEL" in text:
        print(listeChemin[i].split("\\")[-1] + " est belge")
    if "PCGBR" in text or "P<GBR" in text:
        print(listeChemin[i].split("\\")[-1] + " est anglais")
    if "PCFRA" in text or "P<FRA" in text:
        print(listeChemin[i].split("\\")[-1] + " est français")
    if "PCDCC" in text or "P<D<<" in text:
        print(listeChemin[i].split("\\")[-1] + " est allemand")
    if "PCITA" in text or "P<ITA" in text:
        print(listeChemin[i].split("\\")[-1] + " est italien")
    if "PCPOL" in text or "P<POL" in text:
        print(listeChemin[i].split("\\")[-1] + " est polonais")
    if "PCPRT" in text or "P<PRT" in text:
        print(listeChemin[i].split("\\")[-1] + " est portugais")
    if "PCESP" in text or "P<ESP" in text:
        print(listeChemin[i].split("\\")[-1] + " est espagnol")
