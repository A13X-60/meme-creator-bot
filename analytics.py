import os
import json
import requests

ANALYTICS_API_KEY = os.environ['ANALYTICS_API_KEY']
ANALYTICS_INCOMING_URL = 'https://tracker.dashbot.io/track?platform=universal&v=10.1.1-rest&type=incoming&apiKey='\
                         + ANALYTICS_API_KEY
ANALYTICS_OUTGOING_URL = 'https://tracker.dashbot.io/track?platform=universal&v=10.1.1-rest&type=outgoing&apiKey=' \
                         + ANALYTICS_API_KEY


# Send data about incoming messages
def send_in_analytics(data):
    data_json = json.dumps(data)
    requests.post(ANALYTICS_INCOMING_URL, data=data_json, headers={'Content-Type': 'application/json'})


# Send data about outgoing messages
def send_out_analytics(data):
    data_json = json.dumps(data)
    requests.post(ANALYTICS_OUTGOING_URL, data=data_json, headers={'Content-Type': 'application/json'})
