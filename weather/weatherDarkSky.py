import requests 
import json
import datetime
import math
from shutil import copyfile
import textwrap


def windDegreeSwitcher(argument): 
    if(argument >= 340):
        return "East"
    elif(argument >= 290):
        return "South East"
    elif(argument >= 250):
        return "South"
    elif(argument >= 200):
        return "South West"
    elif(argument >= 160):
        return "West"
    elif(argument >= 110):
        return "North West"
    elif(argument >= 70):
        return "North"
    elif(argument >= 20):
        return "North East"
    elif (argument > 0):
        return "East"
    return "Invalid Degrees"

def setIcons(**kwargs): 
    for key, value in kwargs.items(): 
        copyfile('/home/shafay/conkyConfigs/weather/icons/'+value+'.png', '/home/shafay/conkyConfigs/weather/icons/current/'+key +'.png') 

def getTimeSTR(time):
    return ('12am') if time == 0 else (str(time) + 'am') if time < 12 else (str(time-12) + 'pm') if time > 12 else (str(time) + 'pm')

def checkHourlySumLen(data):
    return len(data[1]['summary']) > 10 or len(data[2]['summary']) > 10 or len(data[3]['summary']) > 10

def fillTextLines(array, wrapped, prefix):
    lines = wrapped.split('\n')
    if len(array) < len(lines):
        for i in range(0, len(lines)-len(array)):
            array.append('')
    for i in range(0,len(lines)):
        array[i]+=prefix+lines[i]
    return array

def getString(arr):
    s = ''
    for i in arr:
        s+= i + '\n'
    return s

def addHourlyData(hourlyWeatherData,s):
    pos = ['c','r']
    time = '${color #7EC0EE}'
    desc = ['${color}']
    temps = '${color #ff6461}'
    atemps = '${color red}'
    for j in range(0,4):
        for i in range(1,4):
            if j == 0:
                time += ('' if i <=1 else ('${align' +pos[i-2]+ '}')) + getTimeSTR(datetime.datetime.fromtimestamp(hourlyWeatherData[i]['time']).hour)
            if j == 1:
                if checkHourlySumLen(hourlyWeatherData):
                    wrapped = textwrap.fill(hourlyWeatherData[i]['summary'].replace('and','&'),10)
                    desc = fillTextLines(desc, wrapped, '' if i <=1 else ('${align' +pos[i-2]+ '}'))
                else: 
                    desc += ('' if i <=1 else ('${align' +pos[i-2]+ '}')) + hourlyWeatherData[i]['summary']
            if j == 2:
                temps += ('' if i <=1 else ('${align' +pos[i-2]+ '}')) + str(hourlyWeatherData[i]['temperature']) + 'º'
            if j == 3:
                atemps += ('' if i <=1 else ('${align' +pos[i-2]+ '}')) + 'Feels Like ' + str(hourlyWeatherData[i]['apparentTemperature']) + 'º'
    
    s = time + '\n' + getString(desc) + temps + '\n' + atemps
    return s + '${color}'
def getMonth(i):
    switcher = {
        1: "January",
        2: "February",
        3: "March",
        4: "April",
        5: "May",
        6: "June",
        7: "July",
        8: "August",
        9: "September",
        10: "October",
        11: "November",
        12: "December",
    }
    return switcher.get(i, "Invalid Month")
def split(strng, sep, pos):
    strng = strng.split(sep)
    return [sep.join(strng[:pos]), sep.join(strng[pos:])]
def getParts(summary, sumparts, append):
    splitParts = split(summary,' ',math.ceil(summary.count(' ')/2))
    sumparts[0] = sumparts[0]+splitParts[0] + append
    sumparts[1] = sumparts[1]+splitParts[1] + append
    return sumparts
def addDailyData(hourlyWeatherData,s):
    i = 1
    pos = ['c','r']
    posTemps = ['temperature','apparentTemperature']
    append = ['', 'Feels Like ']
    k=0
    sumParts = ['','']
    while i<5:
        j = 1
        while j< 4:
            if(i==1):
                date = datetime.datetime.fromtimestamp(hourlyWeatherData[j]['time'])
                date = str(date.day) + ' ' + str(getMonth(date.month))
                s+= date + ('${align' + pos[j-1] + '}' if j <3 else '')
            elif(i==2):
                sumParts = getParts(hourlyWeatherData[j]['summary'], sumParts, ('${align' + pos[j-1] + '}' if j <3 else ''))
                if(j==3):
                    s+= sumParts[0] + '\n' + sumParts[1] 
            else:
                s+= append[k] + '{}º-{}º'.format(
                    hourlyWeatherData[j][posTemps[k]+'Low'],
                    hourlyWeatherData[j][posTemps[k]+'High']) + ('${align' + pos[j-1] + '}' if j <3 else '')
            j+=1
        s+= '\n'
        if(i>2):
            k+=1
        i+=1
    return s


def main():   
    with open("/home/shafay/conkyConfigs/weather/APIKeyDarkSky.json") as config_file:
        APIKeyData = json.load(config_file)
    APIkey = APIKeyData['key']

    ip_request = requests.get('https://get.geojs.io/v1/ip.json')
    my_ip = ip_request.json()['ip']  
    geo_request_url = 'https://get.geojs.io/v1/ip/geo/' + my_ip + '.json'
    geo_request = requests.get(geo_request_url)
    lat = geo_request.json()['latitude']
    lon = geo_request.json()['longitude']
    # print(lat,lon)

    BASEURL = 'https://api.darksky.net/forecast/{key}/{lat},{lon}'.format(key = APIkey, lat = lat, lon = lon)
    # print(BASEURL)
    PARAMS = {
        'exclude': ['minutely','flags'],
        'units': 'us', # auto, etc
    }

    weatherData = requests.get(url = BASEURL, params = PARAMS).json()
    dailyForecast = weatherData['daily']
    hourlyWeather = weatherData['hourly']
    hourlyWeatherData = hourlyWeather['data']
    currentWeather = weatherData['currently']
    # print(currentWeather)
    
    temp = currentWeather['temperature']
    feelsLikeTemp = currentWeather['apparentTemperature']

    weatherDesc = hourlyWeather['summary']

    windSpeed = currentWeather['windSpeed']
    windDegrees = currentWeather['windBearing']
    windDegrees = windDegreeSwitcher(windDegrees) # 240 degrees

    cloudsPerc = round(currentWeather['cloudCover']*100,0)

    pressure = currentWeather['pressure']
    humidity = round(currentWeather['humidity']*100,0)
    
    precipIntensity = currentWeather['precipIntensity']
    precipProbability = currentWeather['precipProbability']
    precipType = 'N/A' if precipIntensity == 0 else currentWeather['precipType']

    UVIndex = currentWeather['uvIndex']

    currentIcon = currentWeather['icon']
    s = "{}\n{}{}º Feels like: {}º\n{}Wind:{} {}\n{}Clouds:{}% {}Pressure: {}mmHg     {}Humidity: {}%\n".format(
        '${alignr}'+ weatherDesc,'${color red}', '${alignr}'+ str(temp), feelsLikeTemp,'${alignr}${color #7EC0EE}',str(windSpeed),windDegrees,'${alignr}${color #7EC0EE}',str(cloudsPerc),"${color}",pressure,'${color red}',humidity)
    s += "{}{} at {}mm probability of {}\n{}UV Index: {}   {}\n".format(
        "${color #7EC0EE}", '${alignr}'+ precipType,precipIntensity,precipProbability,'${alignr}', str(UVIndex), '${color}')

    s += '\n\n\n\n' + addHourlyData(hourlyWeatherData, s)

    kwargs = {
        "hour1" : hourlyWeatherData[1]['icon'],
        "hour2" : hourlyWeatherData[2]['icon'],
        "hour3" : hourlyWeatherData[3]['icon'],
        "day1" : dailyForecast['data'][1]['icon'],
        "day2" : dailyForecast['data'][2]['icon'],
        "day3" : dailyForecast['data'][3]['icon'],
        "day4" : dailyForecast['data'][4]['icon'],
        "day5" : dailyForecast['data'][5]['icon'],
        "day6" : dailyForecast['data'][6]['icon'],
        "day7" : dailyForecast['data'][7]['icon'],
        "currentIcon" : currentIcon,
    }
    setIcons(**kwargs)
 
    f = open("/home/shafay/conkyConfigs/weather/weatherDat","w+")

    f.write(s)
    f.close()

    # print(s)
    s1 = '{summary}\n'.format(summary = dailyForecast['summary'])
    s1 = addDailyData(dailyForecast['data'], s1)

    f = open("/home/shafay/conkyConfigs/weather/weatherDailyDat","w+")
    f.write(s1)
    f.close()
    
if __name__ == "__main__":
   main()
