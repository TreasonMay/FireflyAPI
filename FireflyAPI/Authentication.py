from FireflyAPI import Utils
class AuthenticatedObject:
    def __init__(self, auth_blob):
        self.auth_blob = auth_blob
        auth_data = Utils.unpackAuthBlob(auth_blob)
        self.device_id = auth_data["device_id"]
        self.device_token = auth_data["device_token"]
        self.portal = auth_data["portal"]
        self.guid = auth_data["guid"]
class DiscretelyAuthenticatedObject:
    def __init__(self, auth_blob):
        self.__auth_blob = auth_blob
        auth_data = Utils.unpackAuthBlob(auth_blob)
        self.__device_id = auth_data["device_id"]
        self.__device_token = auth_data["device_token"]
        self.__portal = auth_data["portal"]
        self.__guid = auth_data["guid"]