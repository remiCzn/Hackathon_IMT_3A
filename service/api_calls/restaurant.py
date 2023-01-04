import json
import os
import requests
import horaires
URL = "https://data.nantesmetropole.fr/explore/dataset/234400034_070-008_offre-touristique-restaurants-rpdl@paysdelaloire/download/?format=json&timezone=Europe/Berlin&lang=fr"
CACHE = "data/restaurant.json"


if not os.path.isdir("data"):
    os.mkdir('data')
    
def getDataFromAPI():
    res = requests.get(URL)
    if not res.ok:
        return res.status_code
    return res.content

def addHoraire(elem):
    idJson = horaires.get_infos(elem["fields"]["nomoffre"], elem["fields"]["localisation"])
    id = idJson["id"]
    if(id=="NA"):
        elem["fields"]["horaire"] = "NA"
        elem["fields"]["adresse"] = "NA"
        return elem
    adresse = idJson["address"]
    horaire, weekday = horaires.get_horaires(id)
    if(horaire=="NA"):
        elem["fields"]["horaire"] = "NA"
        elem["fields"]["adresse"] = "NA"
        return elem
    h = horaires.encode_horaires_restaurant(horaire, weekday)
    elem["fields"]["horaire"] = h
    elem["fields"]["adresse"] = adresse
    return elem

def addHoraireData(data):
    data = json.loads(data)
    return list(map(addHoraire, data))

def addresse(elem):
    if "adresse1" in elem["fields"]:
        elem["fields"]["adresse"] = elem["fields"]["adresse1"]
    elif "adresse2" in elem["fields"]:
        elem["fields"]["adresse"] = elem["fields"]["adresse2"]
    elif "adresse3" in elem["fields"]:
        elem["fields"]["adresse"] = elem["fields"]["adresse3"]

    return elem

def cacheData():
    dataRestau = getDataFromAPI()
    dataRestau = addHoraireData(dataRestau)
    dataRestau = json.loads(dataRestau)
    dataRestau = list(map(addresse, dataRestau))
    with open(CACHE, "w") as fichier:
        fichier.write(json.dumps(dataRestau))
    return True

if not os.path.isdir("data"):
    os.mkdir('data')

def getCachedDataRestaurant():
    with open(CACHE, 'r') as f:
        data = json.load(f)
    return list(filter(lambda x : "commune" in x["fields"] and x["fields"]["commune"]=="NANTES", data))

if __name__=="__main__":
    cacheData()
    res = getCachedDataRestaurant()
    addHoraire(res[0])
    print(res[0])