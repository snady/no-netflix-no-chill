from flask import Flask, render_template, session, request
from flask import redirect, url_for
import api

app = Flask(__name__)

######################## globals ##############################

thresh = 15
temp = -273 #temperature in celcius. If abs 0, then err
zipc = ""
genre = ""
rating = ""

@app.route("/", methods = ['GET','POST'])
def index():
        if request.method == 'POST':
                global zipc
                zipc = request.form['zipcode']
                global genre
                genre = request.form['genre']
                global rating
                rating = request.form['rating']
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
        if genre != 'no':
                movies = filterGenre(movies, genre)
        if rating != 'no':
                movies = filterRating(movies, rating)
        return render_template("chill.html", movies=movies, temp=temp)

@app.route("/nochill")
def nochill():
        print zipc
        movies = api.showtimes(zipc)
        if genre != 'no':
                movies = filterGenre(movies, genre)
        if rating != 'no':
                movies = filterRating(movies, rating)
        return render_template("nochill.html", movies=movies, temp=temp)

def filterGenre(json, genre):
        newjson = []
        for r in json:
                if 'id' not in r: #distinguishes between showtimes vs guidebox json formats
                        if 'genres' in r:
                                for t in r['genres']: #showtimes
                                        if t == genre:
                                                newjson.append(r)
                else:
                        print r['id']
                        for t in api.amazonGenre(r['id']): #guidebox
                                if t['title'] == genre:
                                        newjson.append(r)
        return newjson

def filterRating(json, rate): #rate = "R", "PG-13", so on
        newjson = []
        for r in json:
                if 'id' in r:
                        if r['rating'] == rate: #guidebox
                                newjson.append(r)
                else:
                        if 'ratings' in r:
                                for t in r['ratings']: #showtimes
                                        if t['code'] == rate:
                                                newjson.append(r)
        return newjson

if __name__ == "__main__":
        app.secret_key = "hello"
        app.debug = True
        app.run(host='0.0.0.0', port=8000)
