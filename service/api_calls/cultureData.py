import json
import os
import horaires
import requests

URL = "https://data.nantesmetropole.fr/api/records/1.0/search/?dataset=244400404_equipements-publics-nantes-metropole&q=&rows=10000&facet=theme&facet=categorie&facet=type&facet=commune&refine.theme="
CACHE = "data/culture.json"

#Créer le fichier data pour stocker les données
if not os.path.isdir("data"):
    os.mkdir('data')

#Requête les données de la DB de Nantes
def getDataFromAPI(theme="Culture"):
    res = requests.get(URL+theme)
    if not res.ok:
        return res.status_code
    return res.json()

#Ajoute à un élément son horaire d'ouverture et renvoie cet element modifié
def addHoraire(elem):
    idJson = horaires.get_infos(elem["fields"]["nom_complet"], elem["fields"]["geo_shape"]["coordinates"])
    id = idJson["id"]
    #Si l'api google ne retourne aucun résultat
    if id=="NA":
        elem["fields"]["horaire"] = "NA"
        elem["fields"]["adresse"] = "NA"
        return elem
    adresse = idJson["address"]
    horaire, weekday = horaires.get_horaires(id)
    #Si on a pas d'horaire d'ouverture, on considère qu'il est ouvert
    if(horaire=="NA"):
        elem["fields"]["horaire"] = "11111111111111"
        return elem
    h = horaires.encode_horaires_restaurant(horaire, weekday)
    elem["fields"]["horaire"] = h
    elem["fields"]["adresse"] = adresse
    return elem

def addHoraireData(data):
    return list(map(addHoraire, data))

#Stocke l'ensemble des données de l'API de Nantes dans un Json
def cacheData():
    dataCulture = getDataFromAPI()
    dataSport = getDataFromAPI("Sport et loisirs")
    #On concatène les données ayant pour thème Culture et Sport et Loisir
    dataSport["records"] += dataCulture["records"]
    dataSport["records"] = addHoraireData(dataSport["records"])
    with open(CACHE, "w") as fichier:
        fichier.write(json.dumps(dataSport))
    return True

#Retourne l'ensemble des données
def getCachedData():
    with open(CACHE, 'r') as f:
        return json.load(f)["records"]

if __name__=="__main__":
    cacheData()
    res = getCachedData()
    print(res[0])
