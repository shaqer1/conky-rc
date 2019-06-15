import requests 
import json
import urllib.request

def windDegreeSwitcher(argument):
    switcher = {
        0: "East",
        90: "North",
        180: "West",
        270: "South",
    }
    return switcher.get(argument, "Invalid Degrees")

def downloader(image_url):
    urllib.request.urlretrieve(image_url,'/home/shafay/conkyConfigs/weather/weatherDesc.png')

def main():   
    with open("/home/shafay/conkyConfigs/weather/APIKey.json") as config_file:
        APIKeyData = json.load(config_file)
    APIkey = APIKeyData['key']

    ip_request = requests.get('https://get.geojs.io/v1/ip.json')
    my_ip = ip_request.json()['ip']  # ip_request.json() => {ip: 'XXX.XXX.XX.X'}

    geo_request_url = 'https://get.geojs.io/v1/ip/geo/' + my_ip + '.json'
    geo_request = requests.get(geo_request_url)
    lat = geo_request.json()['latitude']
    lat = lat[0:-2]

    lon = geo_request.json()['longitude']
    lon = lon[0:-2]

    # print(lat,lon)

    # print(lat, lon)
    BASEURL = 'http://api.openweathermap.org/data/2.5/'

    PARAMS = {
        'appid': APIkey,
        'lat': lat,
        'lon': lon
    }

    currentWeatherData = requests.get(url = BASEURL + 'weather', params = PARAMS).json()
    # print(currentWeatherData)
    
    
    windSpeed = currentWeatherData['wind']['speed']
    windDegrees = currentWeatherData['wind']['deg']
    windDegrees = windDegreeSwitcher(windDegrees)


    weatherDesc = currentWeatherData['weather'][0]['main']

    cloudsPerc = currentWeatherData['clouds']['all']

    currentWeather = currentWeatherData['main']
    temp = currentWeather['temp']
    temp = ((temp - 273.15)*(9.0/5))+32

    pressure = currentWeather['pressure']
    humidity = currentWeather['humidity']
    tempMin = currentWeather['temp_min']
    tempMin = ((tempMin - 273.15)*(9.0/5))+32
    tempMax = currentWeather['temp_max']
    tempMax = ((tempMax - 273.15)*(9.0/5))+32

    cityname = currentWeatherData['name']

    photoUrl = 'http://openweathermap.org/img/w/' + currentWeatherData['weather'][0]['icon'] +'.png'

    downloader(photoUrl)

    s = ""
    # temp = '{}'.format(
    s = ('{}\n{}\n{}\n{} {}\n{}\n{} {}\n{} {}\n'.format(cityname, 
        str(round(temp,0)) + 'ºF', 
        weatherDesc,
        'Pressure:  ' + str(pressure) + 'hPa       ',
        'Humidity: ' + str(humidity) + '%     ',
         'Clouds%:     ' + str(cloudsPerc) + '%',
          'MinTemp:   ' + str(tempMin) + 'ºF', 
          '     MaxTemp:     ' + str(tempMax) + 'ºF',
           'Wind Speed: ' + str(windSpeed) + 'm/s     ',
            'Direction: ' + str(windDegrees)))

    # TODO get 3 day forecast

    forecastData = requests.get(url = BASEURL + 'forecast/daily', params = PARAMS).json()


    hourlyData = requests.get(url = BASEURL + 'forecast', params = PARAMS).json()

    
    f = open("/home/shafay/conkyConfigs/weather/weatherDat","w+")

    f.write(s)
    f.close()

    # print(s)



if __name__ == "__main__":
   main()