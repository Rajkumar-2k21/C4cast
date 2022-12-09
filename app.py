import pyrebase
import requests
from flask import Flask,render_template,request


config = {
     'apiKey': "AIzaSyAWSn6bz7FnBiLI2rfDsC007YRWuF2lqEw",
    'authDomain': "auth-753a0.firebaseapp.com",
    'projectId': "auth-753a0",
    'storageBucket': "auth-753a0.appspot.com",
    'messagingSenderId': "586710427740",
    'appId': "1:586710427740:web:0a9ec2988eec3c8e071e99",
    'measurementId': "G-D4HHWJ9MLB",
   "databaseURL":"https://auth-753a0-default-rtdb.firebaseio.com/"
}
firebase = pyrebase.initialize_app(config)
auth=firebase.auth()
db = firebase.database()


app=Flask(__name__,template_folder='template',static_url_path='/static')

api_key='64b497fbf20a8bd6a9b6758e738bc6a1'

@app.route('/login',methods=["GET","POST"])
def login():
        return render_template('login.html')


@app.route('/index', methods=["GET","POST"])
def weather():
    
    return render_template('index.html')

@app.route('/')
def first():
    
    return render_template('first.html')

@app.route('/register',methods=["GET","POST"])
def register():
        return render_template('register.html')    

@app.route("/weather", methods =["GET","POST"])
def home():
    if request.method=='POST':
        cityname =request.form["cityname"]
        url='https://api.openweathermap.org/data/2.5/weather?q='+cityname+'&units=metric&appid='+api_key
        link=requests.get(url)
        res=link.json()
        if res['cod']=='404':
            return render_template('404.html')
        else:

            temp=res['main']['temp']
            hmt=res['main']['humidity']
            weather=res['weather'][0]['description']
            sys=res['sys']['country']
            min=res['main']['temp_min']
            max=res['main']['temp_max']
        
        return render_template('weather.html',temp=temp,hmt=hmt,cityname=cityname,weather=weather,sys=sys,min=min,max=max)


if __name__=='__main__':
    app.run(debug=True)