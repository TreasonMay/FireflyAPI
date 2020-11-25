import json, requests
from base64 import b64decode
def getSessionToken(auth_blob):
    auth_data = unpackAuthBlob(auth_blob)
    # Gets Firefly Cookie
    data = {"ffauth_device_id": auth_data["device_id"],
            "ffauth_secret": auth_data["device_token"]}
    result = requests.get(auth_data["portal"] + "/Login/api/getsession", data=data)
    return result.cookies.get_dict()["ASP.NET_SessionId"]
def unpackAuthBlob(auth_blob):
    return json.loads(b64decode(auth_blob))