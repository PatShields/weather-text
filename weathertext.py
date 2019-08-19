from dotenv import load_dotenv
from os import environ
from darksky import forecast
import time
from twilio.rest import Client

load_dotenv()

weather=forecast(environ.get('DARKSKY_API'), environ.get('LONGITUDE'), environ.get('LATITUDE'))     
weather_by_hour=weather['hourly']['data'][:13]
sorted_by_precip=sorted(weather_by_hour, key=lambda x: x['precipProbability'], reverse=True)
most_likely=sorted_by_precip[0]

message_body=''

if most_likely['precipProbability']>0.1:
	message_body=(
	    f"There is a chance of {most_likely['precipType']} today.\n"
	    f"It is most likely at "
	    f"{time.strftime('%I:00 %p', time.localtime(most_likely['time']))} "
	    f"where there is a {most_likely['precipProbability']} chance."
	)
	
if message_body:
    client = Client(environ.get('TWILIO_ACCOUNT_SID'), environ.get('TWILIO_AUTH_TOKEN'))

    message = client.messages.create(
                              body=message_body,
                              from_=environ.get('TWILIO_PHONE_NUM'),
                              to=environ.get('MY_PHONE')
                              )