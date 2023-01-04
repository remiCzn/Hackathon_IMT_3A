import json
import os
import requests
import horaires
URL = "https://data.nantesmetropole.fr/explore/dataset/234400034_070-008_offre-touristique-restaurants-rpdl@paysdelaloire/download/?format=json&timezone=Europe/Berlin&lang=fr"
CACHE = "data/restaurant.json"


if not os.path.isdir("data"):
    os.mkdir('data')

#On récupère les données des restaurants depuis Nantes opendata
def getDataFromAPI():
    res = requests.get(URL)
    if not res.ok:
        return res.status_code
    return res.content

#Ajoute à un restaurant, son horaire d'ouverture et son adresse
def addHoraire(elem):
    idJson = horaires.get_infos(elem["fields"]["nomoffre"], elem["fields"]["localisation"])
    id = idJson["id"]
    #Si l'api de google n'a pas trouvé de résultat
    if(id=="NA"):
        elem["fields"]["horaire"] = "NA"
        elem["fields"]["adresse"] = "NA"
        return elem
    adresse = idJson["address"]
    horaire, weekday = horaires.get_horaires(id)
    #Si il n'y a pas d'horaire d'ouverture, on considère que le lieu est ouvert
    if(horaire=="NA"):
        elem["fields"]["horaire"] = "11111111111111"
        return elem
    h = horaires.encode_horaires_restaurant(horaire, weekday)
    elem["fields"]["horaire"] = h
    elem["fields"]["adresse"] = adresse
    return elem

def addHoraireData(data):
    data = json.loads(data)
    return list(map(addHoraire, data))

#Supprime les addresses pour ne garder qu'un champ unique
#L'adresse est déterminé via les coordonnées en utilisant l'api google
def addresse(elem):
    if "adresse1" in elem["fields"]:
        elem["fields"].pop("adresse1")
    elif "adresse2" in elem["fields"]:
        elem["fields"].pop("adresse2")
    elif "adresse3" in elem["fields"]:
        elem["fields"].pop("adresse3")

    return elem

#Stocke les données des restaurants dans un json
def cacheData():
    dataRestau = getDataFromAPI()
    dataRestau = addHoraireData(dataRestau)
    dataRestau = json.loads(dataRestau)
    dataRestau = list(map(addresse, dataRestau))
    with open(CACHE, "w") as fichier:
        fichier.write(json.dumps(dataRestau))
    return True

#Retourne l'ensemble des restaurants de Nantes
def getCachedDataRestaurant():
    with open(CACHE, 'r') as f:
        data = json.load(f)
    return list(filter(lambda x : "commune" in x["fields"] and x["fields"]["commune"]=="NANTES", data))

if __name__=="__main__":
    cacheData()
    res = getCachedDataRestaurant()
    addHoraire(res[0])
    print(res[0])