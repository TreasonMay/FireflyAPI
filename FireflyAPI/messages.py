import requests
from FireflyAPI.authentication import *
from FireflyAPI import utils


class Message(DiscretelyAuthenticatedObject):
    def __init__(self, auth_blob, message_data):
        DiscretelyAuthenticatedObject.__init__(self, auth_blob)
        self.id = message_data["id"]
        self.message_text = message_data["body"]
        self.read = message_data["read"]
        self.sender = message_data["from"]["name"]
        self.archived = message_data["archived"]
        self.date = utils.firefly_timestamp_to_date_time(message_data["sent"])

    def __set_archive_status(self, archive):
        params = {"ffauth_device_id": self._DiscretelyAuthenticatedObject__device_id,
                  "ffauth_secret": self._DiscretelyAuthenticatedObject__device_token}
        data = {f"{'un' * (not archive)}archive": "yes"}
        requests.post(
            self._DiscretelyAuthenticatedObject__portal + "/messages/" + str(self.id),
            params=params, data=data)

    def archive(self):
        """
        Archives the message.
        """
        self.__set_archive_status(True)

    def unarchive(self):
        """
        Un-archives the message.
        """
        self.__set_archive_status(False)