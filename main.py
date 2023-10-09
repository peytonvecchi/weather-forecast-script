import requests
import smtplib

def get_averages(w_data):

    num1=0
    num2=0 

    for data in range(len(w_data)):
        num1 += w_data[data]['temp']
        num2 += w_data[data]['pop']
    
    temp = round(num1 / 7, 2)
    precip = num2 / 7

    list = [temp, precip]

    return list
    
def get_min_max(w_data):

    temp_max=w_data[0]['temp']
    temp_min=w_data[0]['temp']
    precip_max = w_data[0]['pop']
    precip_min = w_data[0]['pop']

    for data in range(len(w_data)):
        if temp_max < w_data[data]['temp']:
            temp_max = w_data[data]['temp']

        if temp_min > w_data[data]['temp']:
            temp_min = w_data[data]['temp']

        if precip_max < w_data[data]['pop']:
            precip_max = w_data[data]['pop']

        if precip_min > w_data[data]['pop']:
            precip_min = w_data[data]['pop']        
        
    
    list = [temp_max, temp_min, precip_max, precip_min]
    return list   

def send_email(email_message):
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user='add your own email here', password='add your own password here')
        connection.sendmail(from_addr='add email here', to_addrs='add email here',
        msg=message)

API_KEY = "key from open weather"
SPACE_KEY = "key from geolocation"
LAT = #add lat here
LON = #add lon here
UNITS = "imperial"
COUNT = "7"
WEATHER_URL = f"https://api.openweathermap.org/data/2.5/forecast?lat={LAT}&lon={LON}&cnt={COUNT}&units={UNITS}&appid={API_KEY}"

weather_response = requests.get(url=WEATHER_URL)
weather_response.raise_for_status()
weather_data_json = weather_response.json()

sun_response = requests.get(url=f"https://api.ipgeolocation.io/astronomy?apiKey={SPACE_KEY}&lat={LAT}&long={LON}")
sun_response.raise_for_status()
space_data = sun_response.json()

weather_data = []
for time in range(len(weather_data_json['list'])):

    dict_for_weather_data = {
        "dt": weather_data_json['list'][time]['dt_txt'],
        "id": weather_data_json['list'][time]['weather'][0]['id'],
        "main": weather_data_json['list'][time]['weather'][0]['main'],
        "description": weather_data_json['list'][time]['weather'][0]['description'],
        "temp": weather_data_json['list'][time]['main']['temp'],
        "pop": weather_data_json['list'][time]['pop']
    }
    weather_data.append(dict_for_weather_data)

sunrise = space_data["sunrise"]
sunset = space_data["sunset"]

averages = get_averages(weather_data)

min_max = get_min_max(weather_data)

message = f"""Subject:Good Morning\n\n

forecast for today...

sunrise: {sunrise}, sunset: {sunset},

average temp: {averages[0]}
max temp: {min_max[0]}
min temp: {min_max[1]}

average precip: {averages[1]}
max precip: {min_max[2]}
min precip: {min_max[3]}
"""

send_email(email_message=message)
