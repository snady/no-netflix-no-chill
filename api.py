import urllib2, json
import datetime, random

####################################### Amazon Prime ##############################################

def amazon():
    '''
    Does an api call of recent popular movies that are available in amazon prime.
    First the link is requested with urllib2, then the returning string is parsed in json format.
    
    return list of all movies in json format
    '''
    url = '''
    https://api-public.guidebox.com/v1.43/US/rKAvVCDsUeEZaNcv4AIfOvmw9SBdODY2/movies/all/%s/15/amazon_prime/all
    '''
    random.seed()
    url = url%(random.randrange(60))
    request = urllib2.urlopen(url)
    result = request.read()
    r = json.loads(result)
    for i in r['results']:
        print i['title']
    return r['results']

def amazonGenre(id):
    '''
    Does an api call of a single movie in order to access the genre.
    
    :param id: id of a single movie

    return list of genres
    '''
    url = '''
    https://api-public.guidebox.com/v1.43/US/rKAvVCDsUeEZaNcv4AIfOvmw9SBdODY2/movie/%s
    '''
    url = url%(str(id))
    request = urllib2.urlopen(url)
    result = request.read()
    r = json.loads(result)
    return r['genres']

def amazonPurchase(id):
    '''
    Returns a link of movie if available in amazon prime, otherwise returns 'nop'

    return link of movie or 'nop'
    '''
    url = '''
    https://api-public.guidebox.com/v1.43/US/rKAvVCDsUeEZaNcv4AIfOvmw9SBdODY2/movie/%s
    '''
    url = url%(str(id))
    request = urllib2.urlopen(url)
    result = request.read()
    r = json.loads(result)
    for source in r['subscription_web_sources']:
        if source['source'] == 'amazon_prime':
            return source['link']
    return "nop"

####################################### Theatre Showtimes ##########################################

def showtimes(zipcode):
    '''
    Does an api call of showtimes to get the list of movies in theaters nearby.
    Has 3 different api keys to account for 50 daily limit per key.
    Adds a reformatted array of showtimes so that times are grouped by theatre.

    :param zipcode: zipcode for location

    returns list of all movies in json format
    '''
    url = '''
    http://data.tmsapi.com/v1.1/movies/showings?startDate=%s&zip=%s&api_key=wzkewgxzuwv4fzh88f8cazfp
    '''
    d = datetime.datetime.now()
    date = d.strftime('%Y-%m-%d')
    try:
        url = url%(date, zipcode)
        request = urllib2.urlopen(url)
    except urllib2.HTTPError:
        try:
            url = '''
            http://data.tmsapi.com/v1.1/movies/showings?startDate=%s&zip=%s&api_key=e4gyb2hr7uxmxpq7c8csddd7
            '''
            url = url%(date, zipcode)
            request = urllib2.urlopen(url)
        except urllib2.HTTPError:
            url = '''
            http://data.tmsapi.com/v1.1/movies/showings?startDate=%s&zip=%s&api_key=jfbmt6ypxpuqhh5q46t3emhc
            '''
            url = url%(date, zipcode)
            request = urllib2.urlopen(url)
    result = request.read()
    r = json.loads(result)
    for i in r:
        theatres = []
        n = 0;
        temp = ""
        for t in i['showtimes']:
            if t['theatre']['name'] == temp:
                theatres[-1]['times'].append(t['dateTime'].split('T')[1])
            else:
                theatres.append({})
                temp = t['theatre']['name']
                theatres[-1]['name'] = temp
                theatres[-1]['times'] = [t['dateTime'].split('T')[1]]
        i['theatres'] = theatres
        print i['theatres']
    return r

#showtimes(11229)

######################################## OpenWeather #############################################

def weather(zipcode):
    '''
    :param zipcode: zipcode for location

    return temperature in celsius of a zipcode
    '''
    url = '''http://api.openweathermap.org/data/2.5/weather?zip=%s,us&appid=2de143494c0b295cca9337e1e96b00e0&units=metric''' #superior metric unit
    url = url%(zipcode)
    request = urllib2.urlopen(url)
    result = request.read()
    r = json.loads(result)
    if r['cod'] == 200:
        return r['main']['temp']
    else:
        return -1000
    
########################################## Filters ################################################

def filterGenre(json, genre):
        '''
        Filters the list of movies in json format by matching genre
        
        :param json, genre: list of movies in json format, genre name (Comedy, Horror, etc)

        return list of movies with matching genre
        '''
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
        '''
        Filters the list of movies by rating

        :param json, rate: list of movies in json format, rating name

        return list of movies with matching rating
        '''
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
