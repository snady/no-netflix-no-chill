from flask import Flask, render_template, session, request
from flask import redirect, url_for
import api

app = Flask(__name__)

######################## globals ##############################

thresh = 0
temp = -273 #temperature in celcius. If abs 0, then err
zipc = ""

@app.route("/", methods = ['GET','POST'])
def index():
        if request.method == 'POST':
                global zipc
                zipc = request.form['zipcode']
                global temp
                temp = api.weather(zipc)
                if temp >= thresh:
                        return redirect("/nochill")
                else:
                        return redirect("/chill")
        return render_template("dummy.html")
        
@app.route("/chill")
def chill():
        movies = api.amazon()
        return render_template("chill.html", movies=movies, temp=temp)

@app.route("/nochill")
def nochill():
        print zipc
        movies = api.showtimes(int(zipc))
        return render_template("nochill.html", movies=movies, temp=temp)

if __name__ == "__main__":
        app.secret_key = "hello"
        app.debug = True
        app.run(host='0.0.0.0', port=8000)
