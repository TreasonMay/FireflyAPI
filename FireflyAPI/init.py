import requests, random
from base64 import b64encode
import xml.etree.ElementTree as ET
from FireflyAPI.Exceptions import *
from FireflyAPI.Timetable import *
from FireflyAPI.Tasks import *
from FireflyAPI.Authentication import *
from FireflyAPI import Utils


class UserIntegration:
    def __init__(self, school_code, session, integration_name="Firefly API"):
        '''
        The UserIntegration object is used to start an integration with the user's Firefly account.
        (call the createIntegration() method on this class to get an AuthenticatedUser class)
        Args:
            school_code (str): The School Code the user uses to log in to Firefly's mobile application.
            session (str): The value of the 'ASP.NET_SessionId' cookie when the user is logged in.
        Raises:
            InvalidSchoolCodeError: Thrown if the school_code provided is invalid.
            AuthenticationError: Invalid session token.
        '''
        self.school_code = school_code.upper()
        self.portal = self.getPortalURL()
        self.app_id = integration_name
        self.session = session
    def getPortalURL(self):
        # Get the URL of the school website from the school code
        response = requests.get("https://appgateway.fireflysolutions.co.uk/appgateway/school/" + self.school_code).text
        response = ET.fromstring(response)
        if response.get("exists") == "false":
            raise SchoolCodeError(f"'{self.school_code}' is an invalid school code.")
        address = response.find("address")
        return "http" + ((address.get("ssl") == "true") * "s") + "://" + address.text
    def createIntegration(self):
        # Use the session cookie in order to authenticate as the user and generate login credentials for next time
        device_id = self.generateDeviceID()
        data = {"ffauth_device_id": device_id,
                "ffauth_secret": "",
                "device_id": device_id,
                "app_id": self.app_id}
        cookies = {"ASP.NET_SessionId": self.session}
        result = requests.get(self.portal + "/Login/api/gettoken", data=data, cookies=cookies)
        if result.status_code != 200:
            raise AuthenticationError("ERROR: Session token is invalid!")
        auth_blob = {}
        xml_response = ET.fromstring(result.text)
        auth_blob["device_id"] = device_id
        auth_blob["device_token"] = xml_response.find("secret").text
        auth_blob["portal"] = self.portal
        auth_blob["guid"] = xml_response.find("user").get("guid")
        return AuthenticatedUser(str(b64encode(json.dumps(auth_blob).encode("utf-8")), "utf-8"))
    def generateDeviceID(self):
        alphabet = "0123456789ABCDEF"
        dash = [8, 13, 18, 23]
        device_id = ""
        for i in range(36):
            if i in dash:
                device_id += "-"
            else:
                device_id += random.choice(alphabet)
        return device_id
class AuthenticatedUser(AuthenticatedObject):
    '''
    The AuthenticatedUser object uses an integration to authenticate and perform actions as a user.
    Args:
        auth_blob (str): This is generated by the UserIntegration class, and is used to authenticate as a user.
    '''
    def getTimetable(self):
        return Timetable(self.auth_blob)
    def getTaskInterface(self):
        return TaskInterface(self.auth_blob)
    def getSessionToken(self):
        '''
        This methods gets a session token in order to log in to the school's Firefly website as the user
        Returns:
            str: The ASP.NET_SessionID cookie.
        '''
        return Utils.getSessionToken(self.auth_blob)