import pyrebase
import requests
from flask import Flask,render_template,request,redirect,url_for,flash,session


config = {
     'apiKey': "AIzaSyAWSn6bz7FnBiLI2rfDsC007YRWuF2lqEw",
    'authDomain': "auth-753a0.firebaseapp.com",
    'projectId': "auth-753a0",
    'storageBucket': "auth-753a0.appspot.com",
    'messagingSenderId': "586710427740",
    'appId': "1:586710427740:web:0a9ec2988eec3c8e071e99",
    'measurementId': "G-D4HHWJ9MLB",
   'databaseURL':"https://auth-753a0-default-rtdb.firebaseio.com/"
}
firebase = pyrebase.initialize_app(config)
auth=firebase.auth()
db = firebase.database()


app=Flask(__name__,template_folder='template',static_url_path='/static')
app.secret_key='secret'
api_key='64b497fbf20a8bd6a9b6758e738bc6a1'

person = {"is_logged_in": False, "name": "", "email": "", "uid": ""}


@app.route('/index', methods=["GET","POST"])
def index():
    if person["is_logged_in"] == True:
        return render_template("index.html",name = person["name"])
    else:
        return redirect('login.html')
@app.route('/')
def first():
        return render_template('first.html')

@app.route('/login')
def login():
        return render_template('login.html')

@app.route('/signup')
def signup():
        return render_template('signup.html')

@app.route("/result", methods = ["POST", "GET"])
def result():
    if request.method == "POST":       
        result = request.form          
        email = result["email"]
        password = result["pass"]
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            session['user'] = email
            global person
            person["is_logged_in"] = True
            person["email"] = user["email"]
            person["uid"] = user["localId"]
            data = db.child("users").get()
            person["name"] = data.val()[person["uid"]]["name"]
            return redirect(url_for('index'))
        except:
            return render_template("mailer.html", email = email)
    else:
        if person["is_logged_in"] == True:
            return redirect(url_for('index'))
        else: 
             return render_template('mailer.html', email = email)
             
@app.route('/register',methods=["GET","POST"])
def register():
    if request.method == "POST":        
        result = request.form           
        email = result["email"]
        password = result["pass"]
        name = result["name"]
        try:
            auth.create_user_with_email_and_password(email, password)
            user = auth.sign_in_with_email_and_password(email, password)
            session['user'] = email
            global person
            person["is_logged_in"] = True
            person["email"] = user["email"]
            person["uid"] = user["localId"]
            person["name"] = name
            data = {"name": name, "email": email}
            db.child("users").child(person["uid"]).set(data)
            return redirect(url_for('index'))
        except:
            
            return render_template('regerr.html',email=email)
    else:
        if person["is_logged_in"] == True:
            return redirect(url_for('index'))
        else:
            return render_template('regerr.html',email=email)

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

@app.route("/logout")
def logout():
    session.pop('user')
    return redirect('/')

if __name__=='__main__':
    app.run(debug=True)