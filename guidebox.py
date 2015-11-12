import urllib2, json
import datetime

################### Amazon Prime ##########################

url = '''
https://api-public.guidebox.com/v1.43/US/rKAvVCDsUeEZaNcv4AIfOvmw9SBdODY2/movies/all/1/25/%s/all
'''
tag = 'amazon_prime'

url = url%(tag)
request = urllib2.urlopen(url)
result = request.read()
r = json.loads(result)

for i in r['results']:
    print i['title']

################### Theatre Showtimes #####################

url = '''
http://data.tmsapi.com/v1.1/movies/showings?startDate=%s&zip=%s&api_key=wzkewgxzuwv4fzh88f8cazfp
'''

d = datetime.datetime.now()
date = d.strftime('%Y-%d-%m')
code = '11229'
url = url%(date, code)
#print url
request = urllib2.urlopen(url)
result = request.read()
r = json.loads(result)

for i in r:
    print i['title']
    for t in i['showtimes']:
        print t['theatre']['name'], 
        print t['dateTime'].split('T') 
    print '\n'

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
    return r['places'] #{'city name': 'whitestone', 'post code': '11357'}
