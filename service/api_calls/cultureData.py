import googleData
import requests
import majDB

URL = "https://data.nantesmetropole.fr/api/records/1.0/search/?dataset=244400404_equipements-publics-nantes-metropole&q=&rows=10000&facet=theme&facet=categorie&facet=type&facet=commune&refine.theme="

#Requête les données de la DB de Nantes
def getDataFromAPI(theme="Culture"):
    res = requests.get(URL+theme)
    if not res.ok:
        return res.status_code
    return res.json()

#Ajoute à un élément son horaire d'ouverture et renvoie cet element modifié
def formatData(elem):
    if("type" not in elem["fields"]):
        elem["fields"]["type"] = "NA"
    idJson = horaires.get_infos(elem["fields"]["nom_complet"], elem["fields"]["geo_shape"]["coordinates"])
    id = idJson["id"]
    #Si l'api google ne retourne aucun résultat
    if id=="NA":
        elem["fields"]["horaire"] = "NA"
        elem["fields"]["adresse"] = "NA"
        return elem
    adresse = idJson["address"]
    horaire, weekday = horaires.get_horaires(id)
    #Si on a pas d'horaire d'ouverture, on considère qu'il est fermé
    if(horaire=="NA"):
        elem["fields"]["horaire"] = "00000000000000"
        elem["fields"]["adresse"] = adresse
        return elem
    h = horaires.encode_horaires_restaurant(horaire, weekday)
    elem["fields"]["horaire"] = h
    elem["fields"]["adresse"] = adresse
    return elem

def addDataToDB(data):
    for d in data["records"]:
        i = formatData(d)
        majDB.addEquipementCulture(i)

def cacheData():
    dataCulture = getDataFromAPI()
    dataSport = getDataFromAPI("Sport et loisirs")
    #On concatène les données ayant pour thème Culture et Sport et Loisir
    dataSport["records"] += dataCulture["records"]
    
    addDataToDB(dataSport)
    return True

if __name__=="__main__":
    data = getDataFromAPI()
    exemple = data["records"][5]
    formatData(exemple)
    majDB.addEquipementCulture(exemple)