import requests
from FireflyAPI.authentication import *
from FireflyAPI import utils


class Message(DiscretelyAuthenticatedObject):
    def __init__(self, auth_blob, message_data):
        DiscretelyAuthenticatedObject.__init__(self, auth_blob)
        self.id = message_data["id"]
        self.message_text = message_data["body"]
        self.is_read = message_data["read"]
        self.sender = message_data["from"]["name"]
        self.archived = message_data["archived"]
        self.date = utils.firefly_timestamp_to_date_time(message_data["sent"])

    def __set_archive_status(self, archive):
        params = {"ffauth_device_id": self._DiscretelyAuthenticatedObject__device_id,
                  "ffauth_secret": self._DiscretelyAuthenticatedObject__device_token}
        data = {"data": str(
            "mutation M { result: messages(ids: [" + str(self.id) + "], user_guid: \"" +
            self._DiscretelyAuthenticatedObject__guid + "\", new_archive: " + str(archive * 1) + ")")}
        requests.post(self._DiscretelyAuthenticatedObject__portal + "/_api/1.0/graphql", params=params, data=data)

    def __set_read_status(self, read):
        params = {"ffauth_device_id": self._DiscretelyAuthenticatedObject__device_id,
                  "ffauth_secret": self._DiscretelyAuthenticatedObject__device_token}
        data = {"data": str(
            "mutation M { result: messages(ids: ["+str(self.id)+"], user_guid: \"" +
            self._DiscretelyAuthenticatedObject__guid+"\", new_read: " + str(read * 1) + ")")}
        requests.post(self._DiscretelyAuthenticatedObject__portal + "/_api/1.0/graphql", params=params, data=data)

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

    def read(self):
        """
        Marks the message as read.
        """
        self.__set_read_status(True)

    def unread(self):
        """
        Marks the message as un-read.
        """
        self.__set_read_status(False)
