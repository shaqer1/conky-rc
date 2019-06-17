import requests 
import json
import datetime
import math
from shutil import copyfile


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

def setIcons(**kwargs): # TODO
    for key, value in kwargs.items(): 
        copyfile('/home/shafay/conkyConfigs/weather/icons/'+value+'.png', '/home/shafay/conkyConfigs/weather/icons/current/'+key +'.png') 

def addHourlyData(hourlyWeatherData,s):
    i = 1
    while i<4:
        time = datetime.datetime.fromtimestamp(hourlyWeatherData[i]['time']).hour
        time = (str(time) + 'am') if time < 12 else (str(time-12) + 'pm') if time > 12 else (str(time) + 'pm')
        s += '{}\n{}\n{}º\nFeels Like {}º\n'.format(
            time,hourlyWeatherData[i]['summary'],hourlyWeatherData[i]['temperature'],hourlyWeatherData[i]['apparentTemperature'])
        i+=1
    return s
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
        """ s += '{}\n{}\n{}º-{}º\nFeels Like {}º-{}º\n'.format(
            date,
            hourlyWeatherData[i]['summary'],
            hourlyWeatherData[i]['temperatureLow'],
            hourlyWeatherData[i]['temperatureHigh'],
            hourlyWeatherData[i]['apparentTemperatureLow'],
            hourlyWeatherData[i]['apparentTemperatureHigh']) """
        i+=1
    return s


def main():   
    with open("/home/shafay/conkyConfigs/weather/APIKeyDarkSky.json") as config_file:
        APIKeyData = json.load(config_file)
    APIkey = APIKeyData['key']

    ip_request = requests.get('https://get.geojs.io/v1/ip.json')
    my_ip = ip_request.json()['ip']  # ip_request.json() => {ip: 'XXX.XXX.XX.X'}
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
    humidity = currentWeather['humidity']*100
    
    precipIntensity = currentWeather['precipIntensity']
    precipProbability = currentWeather['precipProbability']
    precipType = 'N/A' if precipIntensity == 0 else currentWeather['precipType']

    UVIndex = currentWeather['uvIndex']

    currentIcon = currentWeather['icon']
    s = "{}\n{}º    Feels like: {}º\nWind: {} {}\nClouds: {}%      Pressure: {}mmHg       Humidity: {}%\n".format(
        weatherDesc, temp, feelsLikeTemp, windSpeed,windDegrees,cloudsPerc,pressure,humidity)
    s += "{} at {}mm probability of {}\nUV Index: {}   \n".format(
        precipType,precipIntensity,precipProbability, UVIndex)

    s = addHourlyData(hourlyWeatherData, s)

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