import datetime
import json
import pytz
import random
import requests
from base64 import b64decode

tz = pytz.timezone('UTC')
london_tz = pytz.timezone('Europe/London')


def get_session_token(auth_blob):
    auth_data = unpack_auth_blob(auth_blob)
    # Gets Firefly Cookie
    data = {"ffauth_device_id": auth_data["device_id"],
            "ffauth_secret": auth_data["device_token"]}
    result = requests.get(auth_data["portal"] + "/Login/api/getsession", data=data)
    return result.cookies.get_dict()["ASP.NET_SessionId"]


def unpack_auth_blob(auth_blob):
    return json.loads(b64decode(auth_blob))


def firefly_timestamp_to_date_time(timestamp):
    formats = ["%Y-%m-%dT%H:%M:%SZ",
               "%Y-%m-%dT%H:%M:%S",
               "%Y-%m-%dT%H:%M:%S.%fZ"]
    for date_format in formats:
        try:
            converted = datetime.datetime.strptime(timestamp, date_format)
            return tz.localize(converted).astimezone(london_tz)
        except ValueError:
            pass


def generate_device_id():
    alphabet = "0123456789ABCDEF"
    dash = [8, 13, 18, 23]
    device_id = ""
    for i in range(36):
        if i in dash:
            device_id += "-"
        else:
            device_id += random.choice(alphabet)
    return device_id
