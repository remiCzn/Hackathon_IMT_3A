import requests

API_KEY="AIzaSyDlw0WI07LdmH6kOa-uM_JaJeiQAcaqZp8"
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
    return(response.json()["result"]["current_opening_hours"]["weekday_text"])


def encode_horaires(horaires):
    code=[]
    for d in horaires:
        day,times = str(d).split(':',1)
        times = times.strip().replace('\u2009','')
        if times == 'Open 24 hours':
            code.append(True)
        elif times == 'Closed':
            code.append(False)
        else:
            morning, evening = times.split('–',1)
            morning, evening = morning.split(' '), evening.split(' ')
            if len(morning)>1:
                morning_h,morning_t = morning[0], morning[1].split()[0]
                print(morning_h,morning_t)
            else:
                print(morning)
    print(code)


restaurant_name = "mcdo"
location = (47.218371,-1.553621)

id = get_id(restaurant_name,location)
print("ID:", id)
horaires =get_horaires(id)
print(horaires)
code = encode_horaires(horaires)