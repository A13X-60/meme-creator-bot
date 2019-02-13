import os
import json
import requests

analytics_api_key = os.environ['ANALYTICS_API_KEY']
analytics_incoming_url = 'https://tracker.dashbot.io/track?platform=universal&v=10.1.1-rest&type=incoming&apiKey='\
                         + analytics_api_key
analytics_outgoing_url = 'https://tracker.dashbot.io/track?platform=universal&v=10.1.1-rest&type=outgoing&apiKey='\
                         + analytics_api_key


# Send data about incoming messages
def send_in_analytics(data):
    data_json = json.dumps(data)
    requests.post(analytics_incoming_url, data=data_json, headers={'Content-Type': 'application/json'})


# Send data about outgoing messages
def send_out_analytics(data):
    data_json = json.dumps(data)
    requests.post(analytics_outgoing_url, data=data_json, headers={'Content-Type': 'application/json'})