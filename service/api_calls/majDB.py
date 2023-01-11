from db import db_connect, db_close
import restaurantData, cultureData

def initActivity():
    statement = """
    CREATE TABLE IF NOT EXISTS Activity(
        id INTEGER PRIMARY KEY AUTO_INCREMENT UNIQUE,
        activityid VARCHAR(255),
        name VARCHAR(255),
        category VARCHAR(255),
        theme VARCHAR(255),
        type VARCHAR(255),
        address TEXT,
        coordinate VARCHAR(255),
        schedule VARCHAR(20),
        contact VARCHAR(255)
    )
    
    """
    conn = db_connect()
    cursor = conn.cursor()
    cursor.execute(statement)
    conn.commit()
    db_close(conn)

def initRestaurant():
    conn = db_connect()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Restaurant(
        id INTEGER PRIMARY KEY AUTO_INCREMENT UNIQUE,
        activityid VARCHAR(255),
        name VARCHAR(255),
        category VARCHAR(255),
        address TEXT,
        coordinate VARCHAR(255),
        schedule VARCHAR(255),
        contact VARCHAR(255)
    )
    """)
    conn.commit()
    db_close(conn)
    

def initSpectacle():
    statement = """
        CREATE TABLE IF NOT EXISTS Spectacle(
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
            activityid VARCHAR(255),
            name VARCHAR(255),
            category VARCHAR(255),
            emetteur VARCHAR(255)
            address TEXT,
            date VARCHAR(255),
            coordinate VARCHAR(255),
            schedule VARCHAR(20),
            contact VARCHAR(255),
        )
    """

def addEquipementSpectacle(data):
    statement = f"""
        INSERT INTO Restaurant(activityid, name, category, emetteur,address, date, coordinate, schedule, contact)
        VALUES ("{data['activityid']}", "{data['name']}", "{data['category']}", "{data["emetteur"]}", "{data['address']}", "{data["date"]}", "{data['coordinate']}", "{data['schedule']}", "{data['contact']}")
    """

def addEquipementRestaurant(elem):
    data = {}
    data["activityid"] = elem["recordid"]
    data["name"] = elem["fields"]["nomoffre"]
    data["category"] = elem["fields"]["categorie"] if "categorie" in elem["fields"] else "NA"
    data["address"] = elem["fields"]["adresse"]
    data["coordinate"] = str(elem["fields"]["localisation"][0])+', '+str(elem["fields"]["localisation"][1])
    data["schedule"] = elem["fields"]["horaire"]
    if "commtel" in elem["fields"]: data["contact"] = elem["fields"]["commtel"]
    elif "commmail" in elem["fields"]: data["contact"]= elem["fields"]["commmail"]
    else: data["contact"] = "NA"

    statement = f"""
        INSERT INTO Restaurant(activityid, name, category, address, coordinate, schedule, contact)
        VALUES ("{data['activityid']}", "{data['name']}", "{data['category']}", "{data['address']}", "{data['coordinate']}", "{data['schedule']}", "{data['contact']}")
    """
    conn = db_connect()
    cursor = conn.cursor()
    cursor.execute(statement)
    conn.commit()
    db_close(cursor)

def addEquipementCulture(elem):
    data = {}
    data["name"] = elem["fields"]["nom_complet"]
    data["activityid"] = elem["recordid"]
    data["category"] = elem["fields"]["categorie"]
    data["type"] = elem["fields"]["type"]
    data["theme"] = elem["fields"]["theme"]
    data["address"] = elem["fields"]["adresse"]
    data["coordinate"] = str(elem["fields"]["geo_shape"]["coordinates"][1])+', '+str(elem["fields"]["geo_shape"]["coordinates"][0])
    data["schedule"] = elem["fields"]["horaire"]
    if "telephone" in elem["fields"]: data["contact"] = elem["fields"]["telephone"]
    else: data["contact"] = "NA"

    statement = f"""
        INSERT INTO Activity(activityid, name, category, type, theme, address, coordinate, schedule, contact)
        VALUES ("{data['activityid']}", "{data["name"]}", "{data['category']}", "{data['type']}", "{data['theme']}", "{data['address']}", "{data['coordinate']}", "{data['schedule']}", "{data['contact']}")
    """
    #print(statement)
    conn = db_connect()
    cursor = conn.cursor()
    cursor.execute(statement)
    conn.commit()
    db_close(conn)


def majDB():
    initRestaurant()
    restaurantData.cacheData()
    cultureData.cacheData()

def dropTable():
    conn = db_connect()
    cursor = conn.cursor()
    cursor.execute("DROP TABLE Activity")
    cursor.execute("DROP TABLE Restaurant")
    cursor.execute("DROP TABLE Spectacle")
    conn.commit()
    db_close(conn)

if __name__=="__main__":
    #dropTable()
    #initActivity()
    #initRestaurant()
    initSpectacle()
    cursor = db_connect().cursor()
    statement = """
       SELECT * FROM Activity
    """
    cursor.execute(statement)
    print(cursor.fetchall())
    db_close(cursor)