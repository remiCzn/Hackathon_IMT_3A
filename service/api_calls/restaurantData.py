import json
import requests
import googleData
import majDB

URL = "https://data.nantesmetropole.fr/explore/dataset/234400034_070-008_offre-touristique-restaurants-rpdl@paysdelaloire/download/?format=json&timezone=Europe/Berlin&lang=fr"

#On récupère les données des restaurants depuis Nantes opendata
def getDataFromAPI():
    """
    :return: all data available on restaurants in Loire-Atlantique
    """
    res = requests.get(URL)
    if not res.ok:
        return res.status_code
    return res.content

#Ajoute à un restaurant, son horaire d'ouverture et son adresse
def formatData(elem):
    """
    :param elem: restaurant
    :return: donnée formatée avec les données google (restaurant, son horaire d'ouverture et son adresse)
    """
    idJson = googleData.get_infos(elem["fields"]["nomoffre"], elem["fields"]["localisation"])
    id = idJson["id"]
    #Si l'api de google n'a pas trouvé de résultat
    if(id=="NA"):
        elem["fields"]["horaire"] = "NA"
        elem["fields"]["adresse"] = "NA"
        return elem
    adresse = idJson["address"]
    horaire, weekday = googleData.get_horaires(id)
    #Si il n'y a pas d'horaire d'ouverture, on considère que le lieu est ouvert
    if(horaire=="NA"):
        elem["fields"]["horaire"] = "00000000000000"
        elem["fields"]["adresse"] = adresse
        return elem
    h = googleData.encode_horaires_restaurant(horaire, weekday)
    elem["fields"]["horaire"] = h
    elem["fields"]["adresse"] = adresse
    return elem

#Supprime les addresses pour ne garder qu'un champ unique
#L'adresse est déterminé via les coordonnées en utilisant l'api google
def addresse(elem):
    if "adresse1" in elem["fields"]:
        elem["fields"].pop("adresse1")
    if "adresse2" in elem["fields"]:
        elem["fields"].pop("adresse2")
    if "adresse3" in elem["fields"]:
        elem["fields"].pop("adresse3")
    return elem

def addDataToDB(data):
    """
    :param data: restaurant name
    :return: nothing, add restaurant formated to database with google infos
    """
    for d in data["records"]:
        if "commune" in d["fields"] and d["fields"]["commune"]=="NANTES":
            i = formatData(d)
            i = addresse(i)
            majDB.addEquipementRestaurant(i)

#Stocke les données des restaurants dans un json
def cacheData():
    dataRestau = getDataFromAPI()
    dataRestau = json.loads(dataRestau)
    addDataToDB(dataRestau)
    return True

if __name__=="__main__":
    data = getDataFromAPI()
    data = json.loads(data)
    data = list(filter(lambda x: "commune" in x["fields"] and x["fields"]["commune"]=="NANTES", data))
    exemple = data[0]
    formatData(exemple)
    addresse(exemple)
    print(exemple)
    majDB.addEquipementRestaurant(exemple)