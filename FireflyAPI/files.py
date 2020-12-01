from FireflyAPI import utils


class File:
    def __init__(self, file_data):
        self.resource_id = file_data["resourceId"]
        self.fileName = file_data["fileName"]
        self.fileType = file_data["fileType"]
        self.etag = file_data["etag"]
        self.date_created = utils.firefly_timestamp_to_date_time(file_data["dateCreated"])

    @property
    def interactive_download_url(self):
        return f"https://westminster.fireflycloud.net/resource-download.aspx?id={self.resource_id}"

    @property
    def download_url(self):
        return f"https://westminster.fireflycloud.net/resource.aspx?id={self.resource_id}"
