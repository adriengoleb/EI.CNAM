# %% Preprocessing

# on crée un code couleur pour l'affichage des résultats
class bcolors:
    WIN = "\033[32m"  # Vert
    FAIL = "\033[91m"  # Rouge
    KPI = "\033[93m"  # Jaune


# on importe les libraries nécessaires
from numpy.core.numeric import NaN
import pytesseract as tess
from PIL import Image
from passporteye import read_mrz
import glob
import pandas as pd
from translate import Translator
from datetime import datetime
import os
import cv2
#tess.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'


# on instancie la base de donnée des code ISO 3
iso = pd.read_csv("./../src/Data/ISO.csv", sep=";")
# on instancie la base de donnée des prénoms existants
prenom = pd.read_csv("./../src/Data/Prenom.csv", sep=";")
# on instancie la base de donnée des noms existants
nom = pd.read_csv("./../src/Data/Nom.csv", sep="\t")
# on instancie l'outil de traduction
translator = Translator(to_lang="fr")
#pays_fr = translator.translate(pays)
# on instancie la fonction de reconnaissance de pays
def convert_pays(value):
    try:
        return iso.loc[iso["code"] == value, "nationality"].values[0]
    except:
        return value

# on instancie la fonction de convertion de date
def convert_date(value):
    try:
        return datetime.strptime(value, "%Y%m%d")
    except:
        return value[2:]


# %% On utilise passportEye pour les Passeports

# on va chercher l'ensemble des fichiers concernant les passeports
liste_fichiers_passports = glob.glob("./../src/Data/Passeport interieur/*.jpg")
# on instancie une liste vide pour les nationalités identifiées sur les passeports
identified_passports = []
# on instancie une liste vide pour les nationalités non-identifiées sur les passeports
unidentified_passports = []
# on instancie un DataFrame pour rassembler les données récoltées
df_passports = pd.DataFrame(columns=["Fichier", "Type du document", "Nationalité du document", "Date d'expiration", "Pays d'origine", "Prénom", "Nom", "Sexe", "Date de naissance", "Numéro", "Score de lecture"])
# on instancie un nombre pour se situer dans le dataframe
ligne = -1

# pour chaque fichier dans la liste des fichiers
for i in range(len(liste_fichiers_passports)):

    # on incremente la ligne de repere
    ligne += 1
    # on lit l'image et identifie les informations du Machine Readable Zone
    mrz = read_mrz(liste_fichiers_passports[i])
    # on identifie le nom du fichier qui expose le résultat attendue du programme
    nom_fichier = liste_fichiers_passports[i].split("\\")[-1]

    # on essaye de le transformer en dictionnaire de données
    try:
        mrz_data = mrz.to_dict()
        # on ajoute le fichier à notre liste des "identifiées"
        identified_passports.append(f"{nom_fichier}")
        # on renseigne le DataFrame
        df_passports.loc[ligne] = [nom_fichier, mrz_data['type'], mrz_data['country'], mrz_data['expiration_date'],
                        mrz_data['nationality'], mrz_data['names'], mrz_data['surname'], mrz_data['sex'],
                        mrz_data['date_of_birth'], mrz_data['number'], int(mrz_data["valid_score"])/100]

    # si une erreur apparait, on affiche l'échec
    except:
        print(f"{bcolors.FAIL}{nom_fichier} n'a pas été identifié")
        # on ajoute le fichier à notre liste des "non identifiées"
        unidentified_passports.append(f"{nom_fichier}")
        # on renseigne le DataFrame uniquement du nom du fichier
        df_passports.loc[ligne, "Fichier"] = nom_fichier

# on convertie les code ISO 3 en nom de pays
df_passports["Pays d'origine"] = df_passports["Pays d'origine"].apply(lambda x: convert_pays(x))
df_passports["Nationalité du document"] = df_passports["Nationalité du document"].apply(lambda x: convert_pays(x))
# on convertie les dates au format universel
df_passports["Date de naissance"] = df_passports["Date de naissance"].apply(lambda x: convert_date("19" + str(x)))
df_passports["Date d'expiration"] = df_passports["Date d'expiration"].apply(lambda x: convert_date("20" + str(x)))
# on rajoute deux colonnes pour spécifier l'existence du prénom et du nom
df_passports["Vrai prénom"] = df_passports["Prénom"].apply(lambda x: "Oui" if x in list(prenom.prenom) else "Non")
df_passports["Vrai nom"] = df_passports["Nom"].apply(lambda x: "Oui" if x in list(nom.nom) else "Non")
# on initialise les index par le nom du fichier
df_passports = df_passports.set_index("Fichier")

# on affiche le taux de réussite
kpi = (len(identified_passports) / (len(identified_passports)+len(unidentified_passports))) * 100
print(f"{bcolors.KPI}{kpi}% de réussite")

# %% On utilise passportEye pour les Visa

# on va chercher l'ensemble des fichiers concernant les visas
liste_fichiers_visas = glob.glob("./../src/Data/Visa/*.jpg")
# on instancie une liste vide pour les nationalités identifiées sur les passeports
identified_visas = []
# on instancie une liste vide pour les nationalités non-identifiées sur les passeports
unidentified_visas = []
# on instancie un DataFrame pour rassembler les données récoltées
df_visas = pd.DataFrame(columns=["Fichier", "Type du document", "Nationalité du document", "Date d'expiration", "Pays d'origine", "Prénom", "Nom", "Sexe", "Date de naissance", "Numéro", "Score de lecture"])
# on instancie un nombre pour se situer dans le dataframe
ligne = -1

# pour chaque fichier dans la liste des fichiers
for i in range(len(liste_fichiers_visas)):

    # on incremente la ligne de repere
    ligne += 1
    # on lit l'image et identifie les informations du Machine Readable Zone
    mrz = read_mrz(liste_fichiers_visas[i])
    # on identifie le nom du fichier qui expose le résultat attendue du programme
    nom_fichier = liste_fichiers_visas[i].split("\\")[-1]

    # on essaye de le transformer en dictionnaire de données
    try:
        mrz_data = mrz.to_dict()
        # on ajoute le fichier à notre liste des "identifiées"
        identified_visas.append(f"{nom_fichier}")
        # on renseigne le DataFrame
        df_visas.loc[ligne] = [nom_fichier, mrz_data['type'], mrz_data['country'], mrz_data['expiration_date'],
                        mrz_data['nationality'], mrz_data['names'], mrz_data['surname'], mrz_data['sex'],
                        mrz_data['date_of_birth'], mrz_data['number'], int(mrz_data["valid_score"])/100]

    # si une erreur apparait, on affiche l'échec
    except:
        print(f"{bcolors.FAIL}{nom_fichier} n'a pas été identifié")
        # on ajoute le fichier à notre liste des "non identifiées"
        unidentified_visas.append(f"{nom_fichier}")
        # on renseigne le DataFrame uniquement du nom du fichier
        df_visas.loc[ligne, "Fichier"] = nom_fichier

# on convertie les code ISO 3 en nom de pays
df_visas["Pays d'origine"] = df_visas["Pays d'origine"].apply(lambda x: convert_pays(x))
df_visas["Nationalité du document"] = df_visas["Nationalité du document"].apply(lambda x: convert_pays(x))
# on convertie les dates au format universel
df_visas["Date de naissance"] = df_visas["Date de naissance"].apply(lambda x: convert_date("19" + str(x)))
df_visas["Date d'expiration"] = df_visas["Date d'expiration"].apply(lambda x: convert_date("20" + str(x)))
# on rajoute deux colonnes pour spécifier l'existence du prénom et du nom
df_visas["Vrai prénom"] = df_visas["Prénom"].apply(lambda x: "Oui" if x in list(prenom.prenom) else "Non")
df_visas["Vrai nom"] = df_visas["Nom"].apply(lambda x: "Oui" if x in list(nom.nom) else "Non")
# on initialise les index par le nom du fichier
df_visas = df_visas.set_index("Fichier")

# on affiche le taux de réussite
kpi = (len(identified_visas) / (len(identified_visas)+len(unidentified_visas))) * 100
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
        print(f"{bcolors.WIN}{nom_fichier} vient de Belgique")
        # on ajoute le nationalité identifié à notre liste identifiées
        identified_Ids.append(f"{nom_fichier}")
    elif "National Identity Card" in text or "British" in text:
        print(f"{bcolors.WIN}{nom_fichier} vient du Royaume-Uni")
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

# %% Récapitulatif

# on affiche les nationalités identifiées sur les passeports
print(f"{bcolors.WIN}Liste des passeports identifiées ({len(identified_passports)}): {identified_passports}")
# on affiche les nationalités non identifiées sur les passeports
print(f"{bcolors.FAIL}Liste des passeports non identifiées ({len(unidentified_passports)}): {unidentified_passports}")
# on affiche les nationalités identifiées sur les visas
print(f"{bcolors.WIN}Liste des visas identifiées ({len(identified_visas)}): {identified_visas}")
# on affiche les nationalités non identifiées sur les visas
print(f"{bcolors.FAIL}Liste des visas non identifiées ({len(unidentified_visas)}): {unidentified_visas}")
# on affiche les nationalités identifiées sur les cartes identitées
print(f"{bcolors.WIN}Liste des carte d'identitées identifiées ({len(identified_Ids)}): {identified_Ids}")
# on affiche les nationalités non identifiées sur les cartes identitées
print(f"{bcolors.FAIL}Liste des carte d'identitées non identifiées ({len(unidentified_Ids)}): {unidentified_Ids}")

# %% On fait le traitement sur les images: redimensionnement , thresholding pour les passeports

# on recupere les chemins des fichiers non identifiées pour les passeports à partir de la liste unidentified_passports
path_unidentified_passports=[]
for l in range(len(unidentified_passports)):
    path_unidentified_passports.append(os.path.join("./../src/Data/Passeport interieur/",unidentified_passports[l]))

# on recupere les images des passeports non identifiées
for i in range(len(path_unidentified_passports)):
    img = cv2.imread(path_unidentified_passports[i])
    # transformation des images en niveaux de gris
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    # on fait le thresholding avec l'algorithme thresh binary
    result = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 81, 4)
    # on redimensionne l'image
    scale_percent = 500  # percent of original size
    width = int(result.shape[1] * scale_percent / 100)
    height = int(result.shape[0] * scale_percent / 100)
    dim = (width, height)
    # on redimensionne la taille de l'image si elle ne depasse pas 360000 pixels
    if (result.shape[1] * result.shape[0] < 360000):
        resized = cv2.cv2.resize(result, dim)
    else:
        resized = result
    # on sauvegarde l'image dans un chemin pour que ensuite la méthode read_mrz l'utilise
    cv2.imwrite("./../src/Data/Image/image.jpg", resized)
    mrz = read_mrz("./../src/Data/Image/image.jpg")
    # on identifie le nom du fichier qui expose le résultat attendue du programme
    nom_fichier = path_unidentified_passports[i].split("/")[-1]

    # on essaye de le transformer en dictionnaire de données
    try:
        mrz_data = mrz.to_dict()
        # on ajoute le fichier à notre liste des "identifiées"
        identified_passports.append(f"{nom_fichier}")
        # on enleve le fichier de notre liste des "non identifiées"
        unidentified_passports.remove(f"{nom_fichier}")
        # on renseigne le DataFrame
        df_passports.loc[nom_fichier] = [mrz_data['type'], mrz_data['country'], mrz_data['expiration_date'],
                        mrz_data['nationality'], mrz_data['names'], mrz_data['surname'], mrz_data['sex'],
                        mrz_data['date_of_birth'], mrz_data['number'], int(mrz_data["valid_score"])/100,
                        "", ""]
        
        # on affiche qu'on a réussi
        print(f"{bcolors.WIN}{nom_fichier} a maintenant été identifié")

    # si une erreur apparait, on affiche l'échec
    except:
        print(f"{bcolors.FAIL}{nom_fichier} n'a toujours pas été identifié")
        
# on convertie les code ISO 3 en nom de pays
df_passports["Pays d'origine"] = df_passports["Pays d'origine"].apply(lambda x: convert_pays(x))
df_passports["Nationalité du document"] = df_passports["Nationalité du document"].apply(lambda x: convert_pays(x))
# on convertie les dates au format universel
df_passports["Date de naissance"] = df_passports["Date de naissance"].apply(lambda x: convert_date("19" + str(x)))
df_passports["Date d'expiration"] = df_passports["Date d'expiration"].apply(lambda x: convert_date("20" + str(x)))
# on rajoute deux colonnes pour spécifier l'existence du prénom et du nom
df_passports["Vrai prénom"] = df_passports["Prénom"].apply(lambda x: "Oui" if x in list(prenom.prenom) else "Non")
df_passports["Vrai nom"] = df_passports["Nom"].apply(lambda x: "Oui" if x in list(nom.nom) else "Non")

# on affiche le taux de réussite
kpi = (len(identified_passports) / (len(identified_passports)+len(unidentified_passports))) * 100
print(f"{bcolors.KPI}{kpi}% de réussite")
# %%

# on recupere les images des visas non identifiées
path_unidentified_visas=[]
for l in range(len(unidentified_visas)):
    path_unidentified_visas.append(os.path.join("./../src/Data/Visa/",unidentified_visas[l]))

# on effectue les transformations pour les visas
for i in range(len(path_unidentified_visas)):
    img = cv2.imread(path_unidentified_visas[i])
    # transformation des images en niveaux de gris
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    # on fait le thresholding avec l'algorithme thresh binary
    result = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 81, 4)
    # on redimensionne l'image
    scale_percent = 500  # percent of original size
    width = int(result.shape[1] * scale_percent / 100)
    height = int(result.shape[0] * scale_percent / 100)
    dim = (width, height)
    # on redimensionne la taille de l'image si elle ne depasse pas 360000 pixels
    if (result.shape[1] * result.shape[0] < 360000):
        resized = cv2.cv2.resize(result, dim)
    else:
        resized = result
    # on sauvegarde l'image dans un chemin pour que ensuite la méthode read_mrz l'utilise
    cv2.imwrite("./../src/Data/Image/image.jpg", resized)
    mrz = read_mrz("./../src/Data/Image/image.jpg")
    # on identifie le nom du fichier qui expose le résultat attendue du programme
    nom_fichier = path_unidentified_visas[i].split("/")[-1]

    # on essaye de le transformer en dictionnaire de données
    try:
        mrz_data = mrz.to_dict()
        # on ajoute le fichier à notre liste des "identifiées"
        identified_visas.append(f"{nom_fichier}")
        # on enleve le fichier de notre liste des "non identifiées"
        unidentified_visas.remove(f"{nom_fichier}")
        # on renseigne le DataFrame
        df_visas.loc[nom_fichier] = [mrz_data['type'], mrz_data['country'], mrz_data['expiration_date'],
                        mrz_data['nationality'], mrz_data['names'], mrz_data['surname'], mrz_data['sex'],
                        mrz_data['date_of_birth'], mrz_data['number'], int(mrz_data["valid_score"])/100,
                        "", ""]
        
        # on affiche qu'on a réussi
        print(f"{bcolors.WIN}{nom_fichier} a maintenant été identifié")

    # si une erreur apparait, on affiche l'échec
    except:
        print(f"{bcolors.FAIL}{nom_fichier} n'a toujours pas été identifié")
        
# on convertie les code ISO 3 en nom de pays
df_visas["Pays d'origine"] = df_visas["Pays d'origine"].apply(lambda x: convert_pays(x))
df_visas["Nationalité du document"] = df_visas["Nationalité du document"].apply(lambda x: convert_pays(x))
# on convertie les dates au format universel
df_visas["Date de naissance"] = df_visas["Date de naissance"].apply(lambda x: convert_date("19" + str(x)))
df_visas["Date d'expiration"] = df_visas["Date d'expiration"].apply(lambda x: convert_date("20" + str(x)))
# on rajoute deux colonnes pour spécifier l'existence du prénom et du nom
df_visas["Vrai prénom"] = df_visas["Prénom"].apply(lambda x: "Oui" if x in list(prenom.prenom) else "Non")
df_visas["Vrai nom"] = df_visas["Nom"].apply(lambda x: "Oui" if x in list(nom.nom) else "Non")

# on affiche le taux de réussite
kpi = (len(identified_visas) / (len(identified_visas)+len(unidentified_visas))) * 100
print(f"{bcolors.KPI}{kpi}% de réussite")
# %%
# on recupere les images des ID non identifiées
path_unidentified_IDs=[]
for l in range(len(unidentified_Ids)):
    path_unidentified_IDs.append(os.path.join("./../src/Data/Carte ID/",unidentified_Ids[l]))

# pour chaque fichier dans la liste des fichiers
for i in range(len(path_unidentified_IDs)):
    img = cv2.imread(path_unidentified_IDs[i])
    img = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
    result = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,81,4)
    scale_percent = 500  # percent of original size
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
    nom_fichier = path_unidentified_IDs[i].split("./../src/Data/Carte ID/")[-1]

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

# %%
#On supprime les doublons si jamais le code a été executé plus qu'une fois
identified_passports=list(set(identified_passports))
unidentified_passports=list(set(unidentified_passports))
identified_visas=list(set(identified_visas))
unidentified_visas=list(set(unidentified_visas))
identified_Ids=list(set(identified_Ids))
unidentified_Ids=list(set(unidentified_Ids))

# %%
# on affiche le taux de réussite apres les transformations
kpi = round(len(identified_passports) / (len(identified_passports)+len(unidentified_passports))) * 100
print(f"{bcolors.KPI}{kpi}% de réussite pour les passeports")
kpi = (len(identified_visas) / (len(identified_visas)+len(unidentified_visas))) * 100
print(f"{bcolors.KPI}{kpi}% de réussite pour les visas")
kpi = (len(identified_Ids) / (len(identified_Ids)+len(unidentified_Ids))) * 100
print(f"{bcolors.KPI}{kpi}% de réussite pour les IDs")



# %%
