# %% Preprocessing

# on crée un code couleur pour l'affichage des résultats
class bcolors:
    WIN = "\033[32m"  # Vert
    FAIL = "\033[91m"  # Rouge
    KPI = "\033[93m"  # Jaune


# on importe les libraries nécessaires
import pytesseract as tess
from PIL import Image
from passporteye import read_mrz
import glob
import pandas as pd
from translate import Translator
#tess.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'


# on instancie la base de donnée des code ISO 3
iso = pd.read_csv("./../src/Data/ISO.csv", sep=";")

# on instancie l'outil de traduction
translator = Translator(to_lang="fr")

# %% On utilise passportEye pour les Passeports

# on va chercher l'ensemble des fichiers concernant les passeports
liste_fichiers = glob.glob("./../src/Data/Passeport interieur/*.jpg")
# on instancie un kpi de réussite
res = 0
# on instancie une liste vide pour les nationalités identifiées sur les passeports
identified_passports = []
# on instancie une liste vide pour les nationalités non-identifiées sur les passeports
unidentified_passports = []

# pour chaque fichier dans la liste des fichiers
for i in range(len(liste_fichiers)):

    # on lit l'image et identifie les informations du Machine Readable Zone
    mrz = read_mrz(liste_fichiers[i])
    # on identifie le nom du fichier qui expose le résultat attendue du programme
    nom_fichier = liste_fichiers[i].split("\\")[-1]

    # on essaye de le transformer en dictionnaire de données
    try:
        mrz_data = mrz.to_dict()
        # si la transformation a fonctionné, on relève le code ISO 3 du document
        country = mrz_data['country']
        # on identifie le nom complet du pays grâce à la base de données des codes ISO 3
        pays = iso.loc[iso["code"] == country, "nationality"].values[0]
        # on traduit le nom du pays en français
        pays_fr = translator.translate(pays)

        # on affiche le résultat
        print(f"{bcolors.WIN}{nom_fichier} vient de {pays_fr} car {country}")
        # on ajoute le nationalité identifié à notre liste identifiées
        identified_passports.append(f"{nom_fichier}")
        # on incrémente le kpi
        res += 1

    # si une erreur apparait, on affiche l'échec
    except:
        print(f"{bcolors.FAIL}{nom_fichier} n'a pas été identifié")
        # on ajoute le nationalité à notre liste non identifiées
        unidentified_passports.append(f"{nom_fichier}")

# on affiche le taux de réussite
kpi = (res / len(liste_fichiers)) * 100
print(f"{bcolors.KPI}{kpi}% de réussite")

# %% On utilise passportEye pour les Visa

# on va chercher l'ensemble des fichiers concernant les visas
liste_fichiers = glob.glob(("./../src/Data/Fichier_de_donnees/Visa/*.jpg")
# on instancie un kpi de réussite
res = 0
# on instancie une liste vide pour les nationalités identifiées sur les visas
identified_visas = []
# on instancie une liste vide pour les nationalités non identifiées sur les visas
unidentified_visas = []
# pour chaque fichier dans la liste des fichiers
for i in range(len(liste_fichiers)):

    # on identifie le nom du fichier qui expose le résultat attendue du programme
    nom_fichier = liste_fichiers[i].split("\\")[-1]

    # on essaye de le transformer en dictionnaire de données
    try:
        # on lit l'image et identifie les informations du Machine Readable Zone
        mrz = read_mrz(liste_fichiers[i])
        mrz_data = mrz.to_dict()
        # si la transformation a fonctionné, on relève le code ISO 3 du document
        country = mrz_data['country']
        # on identifie le nom complet du pays grâce à la base de données des codes ISO 3
        pays = iso.loc[iso["code"] == country, "nationality"].values[0]
        # on traduit le nom du pays en français
        pays_fr = translator.translate(pays)

        # on affiche le résultat
        print(f"{bcolors.WIN}{nom_fichier} vient de {pays_fr} car {country}")
        # on ajoute le nationalité identifié à notre liste
        identified_visas.append(f"{nom_fichier}")
        # on incrémente le kpi
        res += 1

    # si une erreur apparait, on affiche l'échec
    except:
        print(f"{bcolors.FAIL}{nom_fichier} n'a pas été identifié")
        # on ajoute le nationalité  à notre liste non identifiées
        unidentified_visas.append(f"{nom_fichier}")

# on affiche le taux de réussite
kpi = (res / len(liste_fichiers)) * 100
print(f"{bcolors.KPI}{kpi}% de réussite")

# %% On utilise pytesseract pour les Carte d'identité

# on va chercher l'ensemble des fichiers concernant les cartes d'identité
liste_fichiers = glob.glob("./../src/Data/Carte ID/*.jpg")

# on instancie un kpi de réussite
res = len(liste_fichiers)
# on instancie une liste vide pour les nationalités identifiées sur les cartes d'identités
identified_Ids = []
# on instancie une liste vide pour les nationalités non identifiées sur les cartes d'identités
unidentified_Ids = []

# pour chaque fichier dans la liste des fichiers
for i in range(len(liste_fichiers)):
    # on lit l'image et identifie les informations du Machine Readable Zone
    img = Image.open(liste_fichiers[i])
    # on la transforme en chaine de caractère
    text = tess.image_to_string(img)
    # on identifie le nom du fichier qui expose le résultat attendue du programme
    nom_fichier = liste_fichiers[i].split("\\")[-1]

    # on test la présence des mots clés et on affiche le résultat
    if "BELGIË" in text or "BELGIQUE" in text or "BELGIEN" in text or "BELGIUM" in text:
        print(f"{bcolors.WIN}{nom_fichier} est belge")
        # on ajoute le nationalité identifié à notre liste identifiées
        identified_Ids.append(f"{nom_fichier}")
    elif "National Identity Card" in text or "British" in text:
        print(f"{bcolors.WIN}{nom_fichier} est anglais")
        # on ajoute le nationalité identifié à notre liste identifiées
        identified_Ids.append(f"{nom_fichier}")
    elif "IDFRA" in text or "FRANÇAISE" in text:
        print(f"{bcolors.WIN}{nom_fichier} vient de France")
        # on ajoute le nationalité identifié à notre liste identifiées
        identified_Ids.append(f"{nom_fichier}")
    elif "DEUTSCH" in text:
        print(f"{bcolors.WIN}{nom_fichier} vient d'Allemagne")
        # on ajoute le nationalité identifié à notre liste identifiées
        identified_Ids.append(f"{nom_fichier}")
    elif "ITALIANA" in text:
        print(f"{bcolors.WIN}{nom_fichier} vient d'Italie")
        # on ajoute le nationalité identifié à notre liste identifiées
        identified_Ids.append(f"{nom_fichier}")
    elif "Reeczpospolita" in text or "Polska" in text:
        print(f"{bcolors.WIN}{nom_fichier} vient de Pologne")
        # on ajoute le nationalité identifié à notre liste identifiées
        identified_Ids.append(f"{nom_fichier}")
    elif "PORTUGAL" in text or "PRT" in text:
        print(f"{bcolors.WIN}{nom_fichier} vient du Portugal")
        # on ajoute le nationalité identifié à notre liste identifiées
        identified_Ids.append(f"{nom_fichier}")
    elif "ESPANA" in text:
        print(f"{bcolors.WIN}{nom_fichier} vient d'Espagne")
        # on ajoute le nationalité identifié à notre liste identifiées
        identified_Ids.append(f"{nom_fichier}")
    # sinon on affiche l'échec
    else:
        print(f"{bcolors.FAIL}{nom_fichier} n'a pas été identifié")
        # on ajoute le nationalité à notre liste non identifiées
        unidentified_Ids.append(f"{nom_fichier}")
        # on décrémente le kpi
        res -= 1

# on affiche le taux de réussite
kpi = (res / len(liste_fichiers)) * 100
print(f"{bcolors.KPI}{kpi}% de réussite")
# on affiche les nationalités identifiées sur les passeports
print(f"{bcolors.WIN}liste des passeports identifiées: {identified_passports}")
# on affiche les nationalités non identifiées sur les passeports
print(f"{bcolors.FAIL}liste des passeports non identifiées: {unidentified_passports}")
# on affiche les nationalités identifiées sur les visas
print(f"{bcolors.WIN}liste des visas identifiées: {identified_visas}")
# on affiche les nationalités non identifiées sur les visas
print(f"{bcolors.FAIL}liste des visas non identifiées: {unidentified_visas}")
# on affiche les nationalités identifiées sur les cartes identitées
print(f"{bcolors.WIN}liste des carte d'identitées identifiées: {identified_Ids}")
# on affiche les nationalités non identifiées sur les cartes identitées
print(f"{bcolors.FAIL}liste des carte d'identitées non identifiées: {unidentified_Ids}")

# %%
# On fait le traitement sur les images: redimensionnement , thresholding pour les passeports
import os
import cv2
# on recupere les chemins des fichiers non identifiées pour les passeports à partir de la liste unidentified_passports
CheminUnidentifiedPassports=[]
for l in range(len(unidentified_passports)):
    CheminUnidentifiedPassports.append(os.path.join("./../src/Data/Passeport interieur/",unidentified_passports[l]))

# on recupere les images des passeports non identifiées
for i in range(len(CheminUnidentifiedPassports)):
    img = cv2.imread(CheminUnidentifiedPassports[i])
    #transformation des images en niveaux de gris
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    #on fait le thresholding avec l'algorithme thresh binary
    result = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 81, 4)
    # on redimensionne l'image
    scale_percent = 500  # percent of ori ginal size
    width = int(result.shape[1] * scale_percent / 100)
    height = int(result.shape[0] * scale_percent / 100)
    dim = (width, height)
    # on redimensionne la taille de l'image si elle ne depasse pas 360000 pixels
    if (result.shape[1] * result.shape[0] < 360000):
        resized = cv2.cv2.resize(result, dim)
    else:
        resized = result
    # on sauvegarde l'image dans un chemin pour que ensuite la méthode read_mrz l'utilise
    cv2.imwrite("image.jpg", resized)
    mrz = read_mrz("image.jpg")
    # on identifie le nom du fichier qui expose le résultat attendue du programme. dans ce cas on a pas \\ donc je precise tout le debut du nom du fichier.
    nom_fichier = CheminUnidentifiedPassports[i].split("C:/Users/youssef.balti/Desktop/CNAM/Deuxieme_Annee/Donnees_temporelles_et_spatiales/Projet/General/General/Fichier_de_donnees/Passeport_interieur/")[-1]

    # on essaye de le transformer en dictionnaire de données
    try:
        mrz_data = mrz.to_dict()
        # si la transformation a fonctionné, on relève le code ISO 3 du document
        country = mrz_data['country']
        # on identifie le nom complet du pays grâce à la base de données des codes ISO 3
        pays_fr = iso.loc[iso["code"] == country, "nationality"].values[0]
        # on traduit le nom du pays en français
        # pays_fr = translator.translate(pays)

        # on affiche le résultat
        print(f"{bcolors.WIN}{nom_fichier} vient de {pays_fr} car {country}")
        # on rajoute les nationalitées identifiées apres la transofrmation à la liste identified_passports
        identified_passports.append(f"{nom_fichier}")
        # et on enleve de la liste unidentified_passports
        unidentified_passports.remove(f"{nom_fichier}")

    # si une erreur apparait, on affiche l'échec
    except:
        print(f"{bcolors.FAIL}{nom_fichier} n'a pas été identifié")

# on recupere les images des visas non identifiées
CheminUnidentifiedVisas=[]
for l in range(len(unidentified_visas)):
    CheminUnidentifiedVisas.append(os.path.join("./../src/Data/Visa/",unidentified_visas[l]))

# on effectue les transformations pour les visas
for i in range(len(CheminUnidentifiedVisas)):
    img = cv2.imread(CheminUnidentifiedVisas[i])
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    result = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 81, 4)
    scale_percent = 500  # percent of ori ginal size
    width = int(result.shape[1] * scale_percent / 100)
    height = int(result.shape[0] * scale_percent / 100)
    dim = (width, height)
    # on redimensionne la taille de l'image si elle ne depasse pas 360000 pixels
    if (result.shape[1] * result.shape[0] < 360000):
        resized = cv2.cv2.resize(result, dim)
    else:
        resized = result
    cv2.imwrite("./../src/Data/image.jpg", resized)
    # on identifie le nom du fichier qui expose le résultat attendue du programme
    nom_fichier = CheminUnidentifiedVisas[i].split("./../src/Data/Visa/")[-1]
    # on essaye de le transformer en dictionnaire de données
    try:
        mrz = read_mrz("./../src/Data/image.jpg")
        mrz_data = mrz.to_dict()
        # si la transformation a fonctionné, on relève le code ISO 3 du document
        country = mrz_data['country']
        # on identifie le nom complet du pays grâce à la base de données des codes ISO 3
        pays_fr = iso.loc[iso["code"] == country, "nationality"].values[0]
        # on traduit le nom du pays en français
        # pays_fr = translator.translate(pays)

        # on affiche le résultat
        print(f"{bcolors.WIN}{nom_fichier} vient de {pays_fr} car {country}")
        # on le rajoute à notre liste idetifiée s'il est detecté et on l'enleve de la liste non identifié
        identified_passports.append(f"{nom_fichier}")
        unidentified_passports.remove(f"{nom_fichier}")


    # si une erreur apparait, on affiche l'échec
    except:
        print(f"{bcolors.FAIL}{nom_fichier} n'a pas été identifié")

# on recupere les images des ID non identifiées
CheminUnidentifiedIDs=[]
for l in range(len(unidentified_Ids)):
    CheminUnidentifiedIDs.append(os.path.join("./../src/Data/Carte ID/",unidentified_Ids[l]))

# pour chaque fichier dans la liste des fichiers
for i in range(len(CheminUnidentifiedIDs)):
    img = cv2.imread(CheminUnidentifiedIDs[i])
    img = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
    result = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,81,4)
    scale_percent = 500  # percent of ori ginal size
    width = int(result.shape[1] * scale_percent / 100)
    height = int(result.shape[0] * scale_percent / 100)
    dim = (width, height)
    if(result.shape[1]*result.shape[0]<360000):
        resized = cv2.cv2.resize(result, dim)
    else:
        resized = result
    # on la transforme en chaine de caractère
    text = tess.image_to_string(img)
    # on identifie le nom du fichier qui expose le résultat attendue du programme
    nom_fichier = CheminUnidentifiedIDs[i].split("./../src/Data/Carte ID/")[-1]

    # on test la présence des mots clés et on affiche le résultat
    if "BELGIË" in text or "BELGIQUE" in text or "BELGIEN" in text or "BELGIUM" in text:
        identified_Ids.append(f"{nom_fichier}")
        unidentified_Ids.remove(f"{nom_fichier}")
        print(f"{bcolors.WIN}{nom_fichier} est belge")
    elif "National Identity Card" in text or "British" in text:
        identified_Ids.append(f"{nom_fichier}")
        unidentified_Ids.remove(f"{nom_fichier}")
        print(f"{bcolors.WIN}{nom_fichier} est anglais")
    elif "IDFRA" in text or "FRANÇAISE" in text:
        identified_Ids.append(f"{nom_fichier}")
        unidentified_Ids.remove(f"{nom_fichier}")
        print(f"{bcolors.WIN}{nom_fichier} vient de France")
    elif "DEUTSCH" in text:
        identified_Ids.append(f"{nom_fichier}")
        unidentified_Ids.remove(f"{nom_fichier}")
        print(f"{bcolors.WIN}{nom_fichier} vient d'Allemagne")
    elif "ITALIANA" in text:
        identified_Ids.append(f"{nom_fichier}")
        unidentified_Ids.remove(f"{nom_fichier}")
        print(f"{bcolors.WIN}{nom_fichier} vient d'Italie")
    elif "Reeczpospolita" in text or "Polska" in text:
        print(f"{bcolors.WIN}{nom_fichier} vient de Pologne")
        identified_Ids.append(f"{nom_fichier}")
        unidentified_Ids.remove(f"{nom_fichier}")
    elif "PORTUGAL" in text or "PRT" in text:
        print(f"{bcolors.WIN}{nom_fichier} vient du Portugal")
        identified_Ids.append(f"{nom_fichier}")
        unidentified_Ids.remove(f"{nom_fichier}")
    elif "ESPANA" in text:
        print(f"{bcolors.WIN}{nom_fichier} vient d'Espagne")
        identified_Ids.append(f"{nom_fichier}")
        unidentified_Ids.remove(f"{nom_fichier}")
    # sinon on affiche l'échec
    else:
        print(f"{bcolors.FAIL}{nom_fichier} n'a pas été identifié")

#On supprime les doublons si jamais le code a été executé plus qu'une fois
identified_passports=list(set(identified_passports))
unidentified_passports=list(set(unidentified_passports))
identified_visas=list(set(identified_visas))
unidentified_visas=list(set(unidentified_visas))
identified_Ids=list(set(identified_Ids))
unidentified_Ids=list(set(unidentified_Ids))
# on affiche le taux de réussite apres les transformations
kpi = round(len(identified_passports) / (len(identified_passports)+len(unidentified_passports))) * 100
print(f"{bcolors.KPI}{kpi}% de réussite pour les passeports")
kpi = (len(identified_visas) / (len(identified_visas)+len(unidentified_visas))) * 100
print(f"{bcolors.KPI}{kpi}% de réussite pour les visas")
kpi = (len(identified_Ids) / (len(identified_Ids)+len(unidentified_Ids))) * 100
print(f"{bcolors.KPI}{kpi}% de réussite pour les IDs")



# %%
