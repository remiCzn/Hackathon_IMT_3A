import json
import os
import requests

URL = "https://data.nantesmetropole.fr/api/records/1.0/search/?dataset=244400404_equipements-publics-nantes-metropole&q=&rows=10000&facet=theme&facet=categorie&facet=type&facet=commune&refine.theme="
CACHE = "data/culture.json"

if not os.path.isdir("data"):
    os.mkdir('data')
    
def getDataFromAPI(theme="Culture"):
    res = requests.get(URL+theme)
    if not res.ok:
        return res.status_code
    return res.json()

def cacheData():
    dataCulture = getDataFromAPI()
    dataSport = getDataFromAPI("Sport et loisirs")
    dataSport["records"] += dataCulture["records"]
    with open(CACHE, "w") as fichier:
        fichier.write(json.dumps(dataSport))
    return True

def getCachedData():
    with open(CACHE, 'r') as f:
        return json.load(f)["records"]

if __name__=="__main__":
    cacheData()
    res = getCachedData()
    print(res[0])
