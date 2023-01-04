from db import db_connect
from api_calls import restaurant, cultureData

def initRestaurant():
    cursor = db_connect()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Restaurant(
        id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
        activityid VARCHAR,
        name VARCHAR,
        category VARCHAR,
        address TEXT,
        coordinate INTEGER ARRAY[2],
        schedule INTEGER ARRAY[14],
        contact TEXT
    )
    """)

def addEquipementRestaurant(elem):
    data = {}
    data["activityid"] = elem["recordid"]
    data["name"] = elem["fields"]["nomoffre"]
    data["category"] = elem["fields"]["categorie"]
    data["address"] = elem["fields"]["adresse"]
    data["coordinate"] = elem["fields"]["localisation"]
    data["schedule"] = elem["fields"]["horaire"]
    if "commtel" in elem["fields"]: data["contact"] = elem["fields"]["commtel"]
    elif "commmail" in elem["fields"]: data["contact"]= elem["fields"]["commmail"]
    else: data["contact"] = "NA"

    statement = """
        INSERT INTO Restaurant(activityid, name, category, address, coordinate, schedule, contact)
        VALUES (:activityid, :name, :category, :address, :coordinate, :schedule, :contact)
    """
    cursor = db_connect()
    cursor.execute(statement, data)
    return cursor.lastrowid

def addEquipementCulture(elem):
    data = {}
    data["name"] = elem["fields"]["nom_complet"]
    data["activityid"] = elem["recordid"]
    data["category"] = elem["fields"]["categorie"]
    data["type"] = elem["fields"]["type"]
    data["theme"] = elem["fields"]["theme"]
    data["address"] = elem["fields"]["adresse"]
    data["coordinate"] = elem["fields"]["geo_shape"]["coordinates"]
    data["schedule"] = elem["fields"]["horaire"]
    if "telephone" in elem["fields"]: data["contact"] = elem["fields"]["telephone"]
    else: data["contact"] = "NA"

    statement = """
        INSERT INTO equipement(activityid, name, category, type, theme, address, coordinate, schedule, contact)
        VALUES (:activityid, :name, :category, :type, :theme, :address, :coordinate, :schedule, :contact)
    """
    cursor = db_connect()
    cursor.execute(statement, data)
    return cursor.lastrowid


def majDB():
    initRestaurant()
    restaurant.cacheData()
    cultureData.cacheData()

if __name__=="__main__":
    majDB()