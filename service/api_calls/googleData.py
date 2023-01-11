import requests
from config import API_KEY

def get_infos(name,coordonates):
    """
    :param name: approximate name of a place
    :param coordonates: approximate coordinates of a place
    :return: information (id, address) about a restaurant or activity
    """
    url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input=nantes%20"+name+"&inputtype=textquery&fields=place_id%2Cformatted_address&locationbias=circle%3A10000"+str(coordonates[0])+"%2C"+str(coordonates[1])+"&fields=formatted_address%2Cname%2Crating%2Copening_hours%2Cgeometry&key="+API_KEY
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload).json()
    if(len(response["candidates"])==0):
        print(response)
        return {'id': "NA", 'address': "NA"}
    return {'id': response["candidates"][0]["place_id"], 'address': response["candidates"][0]["formatted_address"]}

def get_horaires(id):
    """
    :param id: id of a place on google maps
    :return: opening hours (periods in 24h format and weekday_text in more complicated format)
    """
    url = "https://maps.googleapis.com/maps/api/place/details/json?place_id="+str(id)+"&fields=current_opening_hours&key="+API_KEY
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    response = response.json()
    if("current_opening_hours" in response["result"]): return response["result"]['current_opening_hours']['periods'], response["result"]['current_opening_hours']['weekday_text']
    else: return "NA", "NA"

def encode_horaires_activity(periods,weekday):
    """
    :param periods: more classic format
    :param weekday: special format that contains the particular information for 24h/24h
    :return: opening periods (morning and evening) of an activity encoded on a 14-length string. 1 for open, 0 for closed. Begins with monday and ends with sunday
    """
    code=[[False, False],[False,False],[False,False],[False,False],[False,False],[False,False],[False,False]]
    for d in range(len(weekday)):
        h = weekday[d].split(':', 1)[1]
        if h == " Open 24 hours":
            if h == 6 :
                code[0] = [True,True]
            else:
                code[d+1]=[True,True]
    for d in periods:
        for action,time in d.items():
            if ((action == 'open') & (int(time['time'])>= 800) & (int(time['time'])<1100))|((action == 'close') & ((int(time['time'])>= 900) & (int(time['time'])<1300))):
                code[int(time['day'])][0]=True
            if ((action =='close') & (int(time['time'])>=1500 | (int(time['time'])<=500)))|((action =='open') & (int(time['time'])>=1300)):
                code[int(time['day'])][1]=True
    res = ""
    for day in code:
        for demi in day:
           if (demi):
               res+='1'
           else:
               res+='0'
    sunday = res[0]+res[1]
    res = res[2:] + sunday
    return res

def encode_horaires_restaurant(periods,weekday):
    """
    :param periods: more classic format
    :param weekday: special format that contains the particular information for 24h/24h
    :return: opening periods (lunch and dinner) encoded on a 14-length string. 1 for open, 0 for closed. Begins with monday and ends with sunday
    """
    code = [[False, False], [False, False], [False, False], [False, False], [False, False], [False, False],
            [False, False]]
    for d in range(len(weekday)):
        h = weekday[d].split(':', 1)[1]
        if h == " Open 24 hours":
            if d == 6:
                code[0] = [True,True]
            else:
                code[d+1]=[True,True]
    for d in periods:
        for action, time in d.items():
            if ((action == 'open') & (int(time['time']) <=1200)):
                code[int(time['day'])][0] = True
            if ((action == 'close') & (int(time['time']) >= 2000 | (int(time['time']) <= 500))) | (
                    (action == 'open') & (int(time['time']) >= 1700)):
                code[int(time['day'])][1] = True
            if ((action == 'close') & (int(time['time']) <= 500)):
                if int(time['day']) == 0 :
                    day = 6
                else:
                    day = int(time['day']) -1
                code[day][1] = True
    res = ""
    for day in code:
        for demi in day:
            if (demi):
                res += '1'
            else:
                res += '0'
    sunday = res[0] + res[1]
    return res[2:] + sunday


def get_distance(origin_id,destination_id,waypoints_id=[],mode="walking",optimize="false"):
    """
    :param origin_id: id du lieu d'origine
    :param destination_id: id du lieu destination
    :param waypoints_id: liste des id des lieux étapes
    :param mode: mode detransport (walking,bicycling,driving)
    :param optimize: trouver l'ordre d'enchainement des étapes pour obtenir le plus cours trajet
    :return: dict contenant {distance}
    """
    if len(waypoints_id)>0:
        text_waypoints = "&waypoints=optimize:" + optimize
        for id in waypoints_id:
            text_waypoints += "|place_id:"+str(id)
    else:
        text_waypoints = ""

    url = "https://maps.googleapis.com/maps/api/directions/json?origin=place_id:"+ origin_id + "&destination=place_id:" + destination_id + text_waypoints +"&mode=" + mode+"&%2Cdistance+"+"&key="+API_KEY
    print(url)
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    response = response.json()
    distance=0
    for i in response["routes"][0]["legs"]:
        distance += i["distance"]["value"]
    return {"distance":distance}

###TEST
if __name__=="__main__":
    restaurant_name = "sain"
    location = (47.218371,-1.553621)
    infos = get_infos(restaurant_name,location)
    print("address: ", infos['address'])
    print("ID:", infos['id'])
    id = infos['id ']
    periods,weekday =get_horaires(id)
    print(periods, weekday)
    code = encode_horaires_restaurant(periods, weekday)
    print(code)

    ###ROUTE TEST
    origin_id = get_infos("cinema ugc", (47.218371, -1.553621))["id"]
    destination_id = get_infos("mesopotamia", (47.218371, -1.553621))["id"]
    step1_id = get_infos("leclerc paridis", (47.218371, -1.553621))["id"]
    step2_id = get_infos("gare nantes", (47.218371, -1.553621))["id"]
    res = get_distance(origin_id, destination_id, waypoints_id=[step1_id, step2_id])
    print(res)

