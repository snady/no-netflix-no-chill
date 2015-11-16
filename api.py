import urllib2, json
import datetime

################### Amazon Prime ##########################

def amazon():
    url = '''
    https://api-public.guidebox.com/v1.43/US/rKAvVCDsUeEZaNcv4AIfOvmw9SBdODY2/movies/all/1/25/amazon_prime/all
    '''
    request = urllib2.urlopen(url)
    result = request.read()
    r = json.loads(result)
    for i in r['results']:
        print i['title']
    return r['results']

def amazonGenre(id):
    url = '''
    https://api-public.guidebox.com/v1.43/US/rKAvVCDsUeEZaNcv4AIfOvmw9SBdODY2/movie/%s
    '''
    url = url%(str(id))
    request = urllib2.urlopen(url)
    result = request.read()
    r = json.loads(result)
    return r['genres']

def amazonPurchase(id):
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

################### Theatre Showtimes #####################

def showtimes(zipcode):
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
            #print theatres
        i['theatres'] = theatres
        print i['theatres']
            
    return r

#showtimes(11229)

################### OpenWeather #####################

def weather(zipcode):
    url = '''http://api.openweathermap.org/data/2.5/weather?zip=%s,us&appid=2de143494c0b295cca9337e1e96b00e0&units=metric''' #superior metric unit
    url = url%(zipcode)
    request = urllib2.urlopen(url)
    result = request.read()
    r = json.loads(result)
    return r['main']['temp']
    
################### Zippopotamus #####################

def zipcode(state,city):
    url = '''http://api.zippopotam.us/us/%s/%s'''
    url = url%(state,city)
    request = urllib2.urlopen(url)
    result = request.read()
    r = json.loads(result)
    if r == {}:
        return "error"
    return r['places'] #[{'place name': 'whitestone', 'post code': '11357'}], could be more than 1 element
