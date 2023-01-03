import json
import os
import requests

URL = "https://data.nantesmetropole.fr/explore/dataset/234400034_070-008_offre-touristique-restaurants-rpdl@paysdelaloire/download/?format=json&timezone=Europe/Berlin&lang=fr"
CACHE = "data/restaurant.json"

if not os.path.isdir("data"):
    os.mkdir('data')
    
def getDataFromAPI():
    res = requests.get(URL)
    if not res.ok:
        return res.status_code
    return res.content

def cacheData():
    dataRestau = getDataFromAPI()
    with open(CACHE, "wb") as fichier:
        fichier.write(dataRestau)
    return True

if not os.path.isdir("data"):
    os.mkdir('data')

def getCachedDataRestaurant():
    with open(CACHE, 'r') as f:
        #return json.load(f)
        data = json.load(f)
    return list(filter(lambda x : "commune" in x["fields"] and x["fields"]["commune"]=="NANTES", data))

if __name__=="__main__":
    cacheData()
    res = getCachedDataRestaurant()
    print(len(res))