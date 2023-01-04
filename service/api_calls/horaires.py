import requests
from config import API_KEY

def get_id(name,coordonates):
    url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input=nantes%20restaurant%20"+name+"&inputtype=textquery&fields=place_id&locationbias=circle%3A10000%"+str(coordonates[0])+"%2C"+str(coordonates[1])+"&fields=formatted_address%2Cname%2Crating%2Copening_hours%2Cgeometry&key="+API_KEY
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    return response.json()["candidates"][0]["place_id"]


def get_horaires(id):
    url = "https://maps.googleapis.com/maps/api/place/details/json?place_id="+id+"&fields=current_opening_hours&key="+API_KEY
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    response = response.json()
    return response["result"]['current_opening_hours']['periods'], response["result"]['current_opening_hours']['weekday_text']


def encode_horaires_activity(periods,weekday):
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
    print(code)
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
    code = [[False, False], [False, False], [False, False], [False, False], [False, False], [False, False],
            [False, False]]
    for d in range(len(weekday)):
        h = weekday[d].split(':', 1)[1]
        if h == " Open 24 hours":
            if h == 6 :
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


restaurant_name = "sain"
location = (47.218371,-1.553621)

id = get_id(restaurant_name,location)
print("ID:", id)
periods,weekday =get_horaires(id)
print(periods, weekday)
code = encode_horaires_restaurant(periods, weekday)
print(code)