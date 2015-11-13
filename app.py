from flask import Flask, render_template, session, request
from flask import redirect, url_for
import api

app = Flask(__name__)

@app.route("/", methods = ['GET','POST'])
def index():
        if request.method == 'POST':
                zipc = request.form['zipcode']
                if api.weather(zipc) >= 20:
                        print api.weather(zipc)
                        return redirect("/nochill")
                else:
                        print api.weather(zipc)
                        return redirect("/chill")
        return render_template("dummy.html")
        
@app.route("/chill")
def chill():
        return "<h1><marquee scrollamount=15>c h i l l</marquee></h1>"

@app.route("/nochill")
def nochill():
        return "<h1>no chill...</h1>"

if __name__ == "__main__":
        app.secret_key = "hello"
        app.debug = True
        app.run(host='0.0.0.0', port=8000)
