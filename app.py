from flask import Flask,render_template,request
import requests
app=Flask(__name__,template_folder='template',static_url_path='/static')

api_key='64b497fbf20a8bd6a9b6758e738bc6a1'

@app.route('/', methods=["GET","POST"])
def weather():
   return render_template('index.html')

@app.route("/weather", methods =["GET","POST"])
def home():
    if request.method=='POST':
        cityname =request.form['cityname']
        url='https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid='+api_key
        res=requests.get(url.format(cityname)).json()
        
        temp=res['main']['temp']
        hmt=res['main']['humidity']
        weather=res['weather'][0]['description']
        sys=res['sys']['country']
        min=res['main']['temp_min']
        max=res['main']['temp_max']
        
        return render_template('weather.html',temp=temp,hmt=hmt,cityname=cityname,weather=weather,sys=sys,min=min,max=max)

if __name__=='__main__':
    app.run(debug=True)