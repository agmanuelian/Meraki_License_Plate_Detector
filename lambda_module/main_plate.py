import json
import time
from urllib.request import urlopen
import requests
import configparser
import sys
import base64
import urllib.request

# MERAKI
api_key = 'YOUR_MERAKI_API_KEY'
MV_Camera_SN = "YOUR_MV-CAMERA_SERIAL_NUMBER"
base_url = f"https://api.meraki.com/api/v1/devices/{MV_Camera_SN}/camera/generateSnapshot"
plate_key = "YOUR_PLATE_RECOGNIZER_API_KEY"

# WEBEX
access_token = "YOUR_WEBEX_ACCESS_TOKEN"
teams_room = "YOUR_WEBEX_ROOM_ID" 

def plate_handler(event):
    try:
        if event["alertData"]["trigger_data"][0]["trigger"]["sensor_value"] == 1:
            msg = "### Garage door opened!\n"
        else:
            msg = "### Garage door closed!\n"

        snapshot_url = camera_snapshot(event["occurredAt"])

        print(f"\nIMAGE URL: {snapshot_url}")
        print("Processing snapshot!...")
        time.sleep(6)

        plate_url = 'https://api.platerecognizer.com/v1/plate-reader/'
        headers={'Authorization': 'Token ' + plate_key}

        response = requests.post(url=plate_url, headers=headers, files= dict(upload=image_encoder(snapshot_url))).json()

        try:
            print(f"\nLicense Plate: {response['results'][0]['plate'].upper()}")
            msg += f"\nLicense Plate: **{response['results'][0]['plate'].upper()}**"
            messenger(snapshot_url, msg)
            print("License plate detected. Webex Teams message sent")
        except:
            msg += "No license plate has been identified"
            messenger(snapshot_url, msg)
            print(msg)
    except:
        print("Error detected")

def image_encoder(url):
    contents = urlopen(url).read()
    return contents

def camera_snapshot(timestamp):
    headers = {
            'X-Cisco-Meraki-API-Key' : api_key
            }
    
    payload = {
    #"timestamp": timestamp
    }
    
    image_url = requests.post(url= base_url, headers=headers, data= payload).json()["url"]
    return image_url

def messenger(url_snapshot, msg):
    url = 'https://webexapis.com/v1/messages'

    headers =  {'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'}
    
    body = {
    "roomId": teams_room,
    "markdown": msg,
    "files": [url_snapshot]
    }

    action = requests.post(url=url, headers=headers, data=json.dumps(body))
    print(action.status_code)
