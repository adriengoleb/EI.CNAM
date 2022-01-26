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

# on instancie la fonction de finition du DataFrame
def finition(df):
    # on convertie les code ISO 3 en nom de pays
    df["Pays d'origine"] = df["Pays d'origine"].apply(lambda x: convert_pays(x))
    df["Nationalité du document"] = df["Nationalité du document"].apply(lambda x: convert_pays(x))
    # on convertie les dates au format universel
    df["Date de naissance"] = df["Date de naissance"].apply(lambda x: convert_date("19" + str(x)))
    df["Date d'expiration"] = df["Date d'expiration"].apply(lambda x: convert_date("20" + str(x)))
    # on rajoute deux colonnes pour spécifier l'existence du prénom et du nom
    df["Vrai prénom"] = df["Prénom"].apply(lambda x: "Oui" if x in list(prenom.prenom) else "Non")
    df["Vrai nom"] = df["Nom"].apply(lambda x: "Oui" if x in list(nom.nom) else "Non")

    return df

# on instancie la fonction de premier traitement
def traitement(type, liste_identified, liste_unidentified):
    # on va chercher l'ensemble des fichiers concernant les passeports
    liste_fichiers = glob.glob(f"./../src/Data/{type}/*.jpg")
    # on instancie un DataFrame pour rassembler les données récoltées
    df = pd.DataFrame(columns=["Fichier", "Type du document", "Nationalité du document", "Date d'expiration", "Pays d'origine", "Prénom", "Nom", "Sexe", "Date de naissance", "Numéro", "Score de lecture"])
    # on instancie un nombre pour se situer dans le dataframe
    ligne = -1

    # pour chaque fichier dans la liste des fichiers
    for i in range(len(liste_fichiers)):

        # on incremente la ligne de repere
        ligne += 1
        # on lit l'image et identifie les informations du Machine Readable Zone
        mrz = read_mrz(liste_fichiers[i])
        # on identifie le nom du fichier qui expose le résultat attendue du programme
        nom_fichier = liste_fichiers[i].split("\\")[-1]

        # on essaye de le transformer en dictionnaire de données
        try:
            mrz_data = mrz.to_dict()
            # on ajoute le fichier à notre liste des "identifiées"
            liste_identified.append(f"{nom_fichier}")
            # on renseigne le DataFrame
            df.loc[ligne] = [nom_fichier, mrz_data['type'], mrz_data['country'], mrz_data['expiration_date'],
                            mrz_data['nationality'], mrz_data['names'], mrz_data['surname'], mrz_data['sex'],
                            mrz_data['date_of_birth'], mrz_data['number'], int(mrz_data["valid_score"])/100]

        # si une erreur apparait, on affiche l'échec
        except:
            print(f"{bcolors.FAIL}{nom_fichier} n'a pas été identifié")
            # on ajoute le fichier à notre liste des "non identifiées"
            liste_unidentified.append(f"{nom_fichier}")
            # on renseigne le DataFrame uniquement du nom du fichier
            df.loc[ligne, "Fichier"] = nom_fichier

    # on traite les colonnes dates, pays, prenom et nom du DataFrame    
    df = finition(df)
    # on initialise les index par le nom du fichier
    df = df.set_index("Fichier")

    # on affiche le taux de réussite
    kpi = (len(liste_identified) / (len(liste_identified)+len(liste_unidentified))) * 100
    print(f"{bcolors.KPI}{kpi}% de réussite")

    return df, liste_identified, liste_unidentified

# on instancie la fonction de modification d'image
def modification_img(img):
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
        resized = cv2.resize(result, dim)
    else:
        resized = result
    # on sauvegarde l'image dans un chemin pour que ensuite la méthode read_mrz l'utilise
    cv2.imwrite("./../src/Data/Image/image.jpg", resized)

# on instancie la fonction de deuxième traitement (redimensionnement, thresholding)
def retraitement(df, type, liste_identified, liste_unidentified):
    # on recupere les chemins des fichiers non identifiées pour les passeports à partir de la liste unidentified_passports
    path_unidentified=[]
    for l in range(len(liste_unidentified)):
        path_unidentified.append(os.path.join(f"./../src/Data/{type}/",liste_unidentified[l]))

    # on recupere les images des passeports non identifiées
    for i in range(len(path_unidentified)):
        img = cv2.imread(path_unidentified[i])
        # on modifie l'image et la sauvergarde
        modification_img(img)
        # on lit l'image sauvegardée
        mrz = read_mrz("./../src/Data/Image/image.jpg")
        # on identifie le nom du fichier
        nom_fichier = path_unidentified[i].split("/")[-1]

        # on essaye de le transformer en dictionnaire de données
        try:
            mrz_data = mrz.to_dict()
            # on ajoute le fichier à notre liste des "identifiées"
            liste_identified.append(f"{nom_fichier}")
            # on enleve le fichier de notre liste des "non identifiées"
            liste_unidentified.remove(f"{nom_fichier}")
            # on renseigne le DataFrame
            df.loc[nom_fichier] = [mrz_data['type'], mrz_data['country'], mrz_data['expiration_date'],
                            mrz_data['nationality'], mrz_data['names'], mrz_data['surname'], mrz_data['sex'],
                            mrz_data['date_of_birth'], mrz_data['number'], int(mrz_data["valid_score"])/100,
                            "", ""]
            
            # on affiche qu'on a réussi
            print(f"{bcolors.WIN}{nom_fichier} a maintenant été identifié")

        # si une erreur apparait, on affiche l'échec
        except:
            print(f"{bcolors.FAIL}{nom_fichier} n'a toujours pas été identifié")

    # on traite les colonnes dates, pays, prenom et nom du DataFrame    
    df = finition(df)

    # on affiche le taux de réussite
    kpi = (len(liste_identified) / (len(liste_identified)+len(liste_unidentified))) * 100
    print(f"{bcolors.KPI}{kpi}% de réussite")

    return df, liste_identified, liste_unidentified

# on instancie la fonction de récapitulatif
def recapitulatif(liste_identified, liste_unidentified):
    # on affiche les bons résultats
    print(f"{bcolors.WIN}Liste des passeports identifiées ({len(liste_identified)}): {liste_identified}")
    # on affiche les mauvais résultats
    print(f"{bcolors.FAIL}Liste des passeports non identifiées ({len(liste_unidentified)}): {liste_unidentified}")


# %% Premier traitement pour les Passeports
df_passports, identified_passports, unidentified_passports = traitement("Passeport interieur", [], [])

# %% Premier traitement pour les Visas
df_visas, identified_visas, unidentified_visas = traitement("Visa", [], [])

# %% Premier récapitulatif: on affiche les nationalités identifiées/non identifiées
# Pour les passeports
recapitulatif(identified_passports, unidentified_passports)
# Pour les visas
recapitulatif(identified_visas, unidentified_visas)

# %% Deuxième traitement pour les Passeports: redimensionnement, thresholding
df_passports, identified_passports, unidentified_passports = retraitement(df_passports, "Passeport interieur", identified_passports, unidentified_passports)

# %% Deuxième traitement pour les Visas: redimensionnement, thresholding
df_visas, identified_visas, unidentified_visas = retraitement(df_visas, "Visa", identified_visas, unidentified_visas)

# %% Deuxième récapitulatif: on affiche les nationalités identifiées/non identifiées
# Pour les passeports
recapitulatif(identified_passports, unidentified_passports)
# Pour les visas
recapitulatif(identified_visas, unidentified_visas)

# %% Export CSV
df_passports.to_csv("./../src/Data/Sortie/Passeport.csv", sep=';', encoding='utf-8', index=True)
df_visas.to_csv("./../src/Data/Sortie/Visa.csv", sep=';', encoding='utf-8', index=True)

# %% Premier traitement pour les ID

# on va chercher l'ensemble des fichiers concernant les cartes d'identité
liste_fichiers = glob.glob("./../src/Data/Carte ID/*.jpg")

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

# on affiche le taux de réussite
kpi = (len(identified_Ids) / (len(identified_Ids)+len(unidentified_Ids))) * 100
print(f"{bcolors.KPI}{kpi}% de réussite pour les IDs")

# %% Deuxième traitement pour les ID

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

# on affiche le taux de réussite
kpi = (len(identified_Ids) / (len(identified_Ids)+len(unidentified_Ids))) * 100
print(f"{bcolors.KPI}{kpi}% de réussite pour les IDs")
# %%
