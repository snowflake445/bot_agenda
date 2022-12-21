import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta
import pandas as pd
import tweepy

api = tweepy.client(
    consumer_key="Juam1P5bI5ACvhjXMQst9yPz5",
    consumer_secret="LiBD9DTXyMrDkTC7piQTGbLDs9HVbIgtvRTKPsV5fNi1Cx1gqn",
    access_token = "1605571356330004482-nLvycMw0AqNUHma3J4AyExOtf7UTxY",
    access_token_secret = "Q8KaVgXWhmX5m8Zg9y5m2nqHDD1c6wHNn4msxlqeylPPz"
)


# Create a session and set the headers once
session = requests.Session()
session.headers = {'user-agent': 'Mozilla/5.0'}

# Get the response from the website
response = session.get('https://www.gov.br/planalto/pt-br/acompanhe-o-planalto/agenda-do-presidente-da-republica')

# Parse the HTML response
soup = BeautifulSoup(response.text, 'html.parser')

# Find the start and end times of the appointments
start_times = soup.find_all('time', {'class': re.compile('compromisso-inicio')})
end_times = soup.find_all('time', {'class': re.compile('compromisso-fim')})

if len(start_times) > 0:
    # Convert the start and end times to datetime objects
    start_times = [datetime.strptime(time.contents[0].text, '%Hh%M') for time in start_times]
    end_times = [datetime.strptime(time.contents[0].text, '%Hh%M') for time in end_times]

    # Calculate the total working time
    total_working_time = sum([end - start for start, end in zip(start_times, end_times)], timedelta())

    # Format the output message
    hours, minutes = divmod(total_working_time.total_seconds() / 60, 60)
    if hours >= 1:
        message = f'O Presidente Lula trabalhou {int(hours)} horas e {int(minutes)} minutos hoje.'
    else:
        message = f'O Presidente Lula trabalhou por {int(minutes)} minutos hoje.'
    print(message)
else:
    message= ("O Presidente Lula não trabalhou hoje.")
    print(message)

    try:
        tweet = api.create_tweet(text=message)
        print(tweet)
    except:
        print("erro")