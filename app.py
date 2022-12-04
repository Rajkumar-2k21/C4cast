import requests

api_key='f8db2868af87e9e4244dcbd14f131c24'

user_input=input("enter the city name:")

weather_data=requests.get(
    f"https://api.openweathermap.org/data/2.5/weather?q={user_input}&appid={api_key}")


weather=weather_data.json()['weather'][0]['main']
temp=weather_data.json()['main']['temp']
hum=weather_data.json()['main']['humidity']
print("current weather is :",weather)
print("current temprature is :",temp)
print("current humadity is :",hum) 

