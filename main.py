# imports
import requests
import os
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

# twilio account sending SMS API
proxy_client = TwilioHttpClient()
proxy_client.session.proxies = {'https': os.environ['https_proxy']}

account_sid = 'AC908d470bc46518b482e838f5314cf40c'
auth_token = '866e57169e5758b67e4b04875fb8543d'

# connect to client of TWILIO
client = Client(account_sid, auth_token, http_client=proxy_client)

# these are the parameters for Ocean Weather Map API
my_api_key = '8f6465528ade9febb18c8d568aa53376'
parameters = {
    'lat': 14.599512,
    'lon': 120.984222,
    'appid': my_api_key,
    'exclude': 'current,minutely,daily,alerts'
}

# get the response from the requests to Open WeatherMap API
response = requests.get('http://api.openweathermap.org/data/2.5/onecall', params=parameters)
response.raise_for_status()

# get the data in json format
weather_data = response.json()

# get the weather data hourly
weather_hourly = weather_data['hourly']

will_rain = False
# iterate to all of the hours from in 48 hours
for weather in weather_hourly[:12]:
    # get the main weather condition and weather id for that time
    main_weather_thisTime = weather['weather'][0]['id']
    # check if you should bring an umbrella
    if main_weather_thisTime < 700:
        will_rain = True

if will_rain:
    # write the message
    message = client.messages.create(body="It Will Rain Today, Bring your Umbrella☔☔☔!!!", from_="+14808004636",
                                     to='+639989245999')
    print(message.status)
else:
    # write the message
    message = client.messages.create(body="It Will not Rain Today!!!", from_="+14808004636",
                                     to='+639989245999')
    print(message.status)