from FireflyAPI import Utils


class File:
    def __init__(self, file_data):
        self.resource_id = file_data["resourceId"]
        self.fileName = file_data["fileName"]
        self.fileType = file_data["fileType"]
        self.etag = file_data["etag"]
        self.date_created = Utils.firefly_timestamp_to_date_time(file_data["dateCreated"])
