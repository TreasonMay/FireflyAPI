import datetime, json, requests, pytz
from base64 import b64decode
from FireflyAPI import Utils
class Timetable:
    '''
    The Timetable class is used to get information about lessons.
    This object can either be created via the AuthenticatedUser class or created by passing the auth_blob value upon creation.
    Args:
        auth_blob (str): This is generated by the UserIntegration class, and is used to authenticate as a user.
    '''
    def __init__(self, auth_blob):
        self.__auth_blob = auth_blob
        auth_data = json.loads(b64decode(auth_blob))
        self.__device_id = auth_data["device_id"]
        self.__device_token = auth_data["device_token"]
        self.__portal = auth_data["portal"]
        self.__guid = auth_data["guid"]
    def getLessons(self, start, end):
        '''
        Gets the timetable for the days between the given start and end times.
        Args:
            start (datetime Object): The first day from which to get the timetable.
            end (datetime Object): The last day  from which to get the timetable.
        Returns:
            array [day Object]: The days between start and end date.
        '''
        start_day = start.replace(hour=0, minute=0, second=0, microsecond=0)
        end_day = end.replace(hour=23, minute=59, second=59, microsecond=999999)
        start_day = start_day.strftime("%Y-%m-%dT%H:%M:%S%Z")
        end_day = end_day.strftime("%Y-%m-%dT%H:%M:%S%Z")
        params = {"ffauth_device_id": self.__device_id,
                  "ffauth_secret": self.__device_token}
        data = {
            "data": "query Query { events(start: \"" + start_day + "Z\", for_guid: \"" + self.__guid + "\", end: \"" + end_day + "Z\") { end, location, start, subject, description, guid, attendees { role, principal { guid, name } } } }"}
        response = requests.post(self.__portal + "/_api/1.0/graphql", params=params, data=data).text
        response = json.loads(response)
        lessons_data = response["data"]["events"]
        lessons = []
        for lesson_data in lessons_data:
            lessons.append(Lesson(lesson_data))
        return lessons
    def today(self):
        return self.getLessons(datetime.datetime.now(), datetime.datetime.now())
class Lesson:
    '''
    The Lesson object contains information on a particular lesson.
    This object can be created from the Timetable class.
    Args:
        lesson_data (dict Object): Lesson data in a dictionary format.
    Attributes:
        lesson_data (dict Object): Lesson data in a dictionary format.
        start (datetime Object): The start time of the lesson.
        end (datetime Object): The end time of the lesson.
        location (str): The location/room of the lesson.
        description (str): Further details about the lesson.
        guid (str): Firefly's internal identifier for the lesson.
        lesson_groups (dict Object): The people/classes attending the lesson, in a dictionary format.
        teachers (array [str]): An array of names of the teachers attending the lesson.
        students (array [str]): An array of names of the students attending the lesson.
    '''
    def __init__(self, lesson_data):
        self.lesson_data = lesson_data
        self.start = Utils.fireflyTimestampToDateTime(lesson_data["start"])
        self.end = Utils.fireflyTimestampToDateTime(lesson_data["end"])
        self.location = lesson_data["location"]
        self.subject = lesson_data["subject"]
        self.description = lesson_data["description"]
        self.guid = lesson_data["guid"]
        self.lesson_groups = lesson_data["attendees"]
        self.teachers = []
        self.students = []
        for group in self.lesson_groups:
            if group["role"] == "Chairperson":
                self.teachers.append(group["principal"]["name"])
            elif group["role"] == "Required":
                self.students.append(group["principal"]["name"])
    def __str__(self):
        return f"{self.subject}, {self.location}"
