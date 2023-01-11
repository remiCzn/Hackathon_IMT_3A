import requests
import json
import majDB
from datetime import datetime
from datetime import date
from tqdm import tqdm

URL = "https://data.nantesmetropole.fr/api/explore/v2.1/catalog/datasets/244400404_agenda-evenements-nantes-nantes-metropole/exports/json?lang=fr&timezone=Europe%2FBerlin"

#On récupère les données des restaurants depuis Nantes opendata
def getDataFromAPI():
    res = requests.get(URL)
    if not res.ok:
        return res.status_code
    return res.content

def formatSchedule(deb, fin, date):
    res = [0 for i in range(14)]
    day = datetime.strptime(date, "%Y-%m-%d").weekday()

    if fin=="NA": fin = "23:59"
    if deb=="NA": deb = "06:00"

    tDebut = datetime.strptime(deb, '%H:%M').time()
    tFin = datetime.strptime(fin, '%H:%M').time()

    if tDebut <datetime.strptime("12:00", "%H:%M").time(): res[day] = 1
    if tFin > datetime.strptime("12:00", "%H:%M").time() or datetime.strptime("05:00", "%H:%M").time()>tFin: res[day+1] = 1
    return res

def formatData(data):
    for k in data.keys():
        if not data[k]: data[k] = "NA"
    res = {}
    res["activityid"] = data['id_manif']
    res["name"] = data["nom"]
    res["category"] = data['rubrique']
    res["emetteur"] = data["emetteur"]
    res["address"] = data['lieu'] +" "+data['adresse']+" "+data["ville"]+" "+data["code_postal"]
    res["coordinate"]=data["location"]
    res["date"] = data['date']
    res["schedule"] = formatSchedule(data["heure_debut"] if "heure_debut" in data else "NA", data["heure_fin"] if "heure_fin" in data else "NA", data["date"])
    if "lieu_tel" in data: res["contact"] = data["lieu_tel"]
    elif "lieu_email" in data: res["contact"]= data["lieu_email"]
    else: data["contact"] = "NA"
    return res

### date sous format aaaa-mm-dd ou aa-mm-dd
def aVenir(data):
    try:
        dateEvent = datetime.strptime(data['date'], '%Y-%m-%d')
    except ValueError as e:
        print(e)
        dateEvent = datetime.strptime(data["date"], "%y-%m-%d")
        data["date"] = "20"+data["date"]
    return dateEvent.date()>date.today()

def main():
    data = getDataFromAPI()
    data = json.loads(data)
    data = list(filter(aVenir, data))
    data = list(map(formatData, data))
    for d in tqdm(data):
        majDB.addEquipementSpectacle(d)

if __name__=="__main__":
    main()
