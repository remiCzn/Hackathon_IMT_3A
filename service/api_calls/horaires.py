import requests
from config import API_KEY

#returns the informations (id, address) about a restaurant or activity given its name and approximate location)
def get_infos(name,coordonates):
    url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input=nantes%20"+name+"&inputtype=textquery&fields=place_id%2Cformatted_address&locationbias=circle%3A10000%"+str(coordonates[0])+"%2C"+str(coordonates[1])+"&fields=formatted_address%2Cname%2Crating%2Copening_hours%2Cgeometry&key="+API_KEY
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload).json()
    if(len(response["candidates"])==0): return {'id': "NA", 'address': "NA"}
    return {'id': response["candidates"][0]["place_id"], 'address': response["candidates"][0]["formatted_address"]}

#returns the opening hours (periods in 24h format and weekday_text in more complicated format) given the id of a place on google maps
def get_horaires(id):
    url = "https://maps.googleapis.com/maps/api/place/details/json?place_id="+id+"&fields=current_opening_hours&key="+API_KEY
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    response = response.json()
    if("current_opening_hours" in response["result"]): return response["result"]['current_opening_hours']['periods'], response["result"]['current_opening_hours']['weekday_text']
    else: return "NA", "NA"
#returns the opening periods (morning and evening) of an activity given its periods and weekday_text
#the answer is encoded on a 14-length string. 1 for open, 0 for closed. Begins with monday and ends with sunday
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

#returns the opening periods (lunch and dinner) of a restaurant given its periods and weekday_text
#the answer is encoded on a 14-length string. 1 for open, 0 for closed. Begins with monday and ends with sunday
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

if __name__=="__main__":
    restaurant_name = "sain"
    location = (47.218371,-1.553621)


###TEST
if __name__=="__main__":
    restaurant_name = "sain"
    location = (47.218371,-1.553621)
    infos = get_infos(restaurant_name,location)
    print("address: ", infos['address'])
    print("ID:", infos['id'])
    periods,weekday =get_horaires(id)
    print(periods, weekday)
    code = encode_horaires_restaurant(periods, weekday)
    print(code)

