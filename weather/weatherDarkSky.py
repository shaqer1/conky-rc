import requests 
import json
import datetime
from shutil import copyfile


def windDegreeSwitcher(argument): # TODO
    switcher = {
        0: "East",
        90: "North",
        180: "West",
        270: "South",
    }
    return switcher.get(argument, "Invalid Degrees")

def setIcons(**kwargs): # TODO
    for key, value in kwargs.items(): 
        copyfile('/home/shafay/conkyConfigs/weather/icons/'+value+'.png', '/home/shafay/conkyConfigs/weather/'+key +'.png') 

def addHourlyData(hourlyWeatherData,s):
    i = 1
    while i<4:
        time = datetime.datetime.fromtimestamp(hourlyWeatherData[i]['time']).hour
        time = (str(time) + 'am') if time < 12 else (str(time-12) + 'pm') if time > 12 else (str(time) + 'pm')
        s += '{}\n{}\n{}º\nFeels Like {}º\n'.format(
            time,hourlyWeatherData[i]['summary'],hourlyWeatherData[i]['temperature'],hourlyWeatherData[i]['apparentTemperature'])
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
    currentWeather = weatherData['currently']
    # print(currentWeather)
    
    temp = currentWeather['temperature']
    feelsLikeTemp = currentWeather['apparentTemperature']

    weatherDesc = currentWeather['summary']

    windSpeed = currentWeather['windSpeed']
    windDegrees = currentWeather['windBearing']
    windDegrees = windDegreeSwitcher(windDegrees) # 240 degrees

    cloudsPerc = currentWeather['cloudCover']*100

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
    
    
    #TODO
    hourlyWeatherData = weatherData['hourly']['data']

    s = addHourlyData(hourlyWeatherData, s)

    kwargs = {
        "hour1" : hourlyWeatherData[1]['icon'],
        "hour2" : hourlyWeatherData[2]['icon'],
        "hour3" : hourlyWeatherData[3]['icon'],
        "currentIcon" : currentIcon,
    }
    setIcons(**kwargs)
  

    
    f = open("/home/shafay/conkyConfigs/weather/weatherDat","w+")

    f.write(s)
    f.close()

    # print(s)



if __name__ == "__main__":
   main()