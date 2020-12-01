import json
import warnings
from FireflyAPI import files
from FireflyAPI import utils


class TaskEvent:
    def __init__(self, event_data, is_student_event):
        self.read = event_data["latestRead"]
        self.edited = event_data["edited"]
        self.authorName = event_data["authorName"]
        self.eventReleased = event_data["released"]
        self.releasedTime = utils.firefly_timestamp_to_date_time(event_data["releasedTimestamp"])
        self.sentTime = utils.firefly_timestamp_to_date_time(event_data["sentTimeStamp"])
        self.createdTime = utils.firefly_timestamp_to_date_time(event_data["createdTimestamp"])
        self.is_student_event = is_student_event


class SetTaskEvent(TaskEvent):
    pass


class EditTaskEvent(TaskEvent):
    pass


class ArchiveTaskEvent(TaskEvent):
    pass


class UnarchiveTaskEvent(TaskEvent):
    pass


class AddFileTaskEvent(TaskEvent):
    def __init__(self, event_data, is_student_event):
        TaskEvent.__init__(self, event_data, is_student_event)
        self.file = files.File(event_data["file"])


class CommentTaskEvent(TaskEvent):
    def __init__(self, event_data, is_student_event):
        TaskEvent.__init__(self, event_data, is_student_event)
        self.message = event_data["message"]


class MarkAsDoneTaskEvent(TaskEvent):
    pass


class MarkAsUndoneTaskEvent(TaskEvent):
    pass


class MarkAndGradeTaskEvent(TaskEvent):
    def __init__(self, event_data, is_student_event):
        TaskEvent.__init__(self, event_data, is_student_event)
        self.message = event_data["message"]
        self.mark = None
        if event_data["mark"] is not None:
            self.mark = event_data["mark"]
        self.grade = None
        if event_data["grade"] is not None:
            self.grade = event_data["grade"]


class RequestedResubmissionTaskEvent(TaskEvent):
    def __init__(self, event_data, is_student_event):
        TaskEvent.__init__(self, event_data, is_student_event)
        self.message = event_data["message"]


class ConfirmCompletedTaskEvent(TaskEvent):
    def __init__(self, event_data, is_student_event):
        TaskEvent.__init__(self, event_data, is_student_event)
        self.message = event_data["message"]


class ExcusedTaskEvent(TaskEvent):
    def __init__(self, event_data, is_student_event):
        TaskEvent.__init__(self, event_data, is_student_event)
        self.message = event_data["message"]


class ReminderTaskEvent(TaskEvent):
    pass


event_types = {"set-task": SetTaskEvent,
               "edit-task": EditTaskEvent,
               "archive-task": ArchiveTaskEvent,
               "unarchive-task": UnarchiveTaskEvent,
               "add-file": AddFileTaskEvent,
               "comment": CommentTaskEvent,
               "mark-as-done": MarkAsDoneTaskEvent,
               "mark-as-undone": MarkAsUndoneTaskEvent,
               "mark-and-grade": MarkAndGradeTaskEvent,
               "request-resubmission": RequestedResubmissionTaskEvent,
               "confirm-task-is-complete": ConfirmCompletedTaskEvent,
               "confirm-student-is-excused": ExcusedTaskEvent,
               "send-reminder":ReminderTaskEvent}


class TaskEventStore:
    """
    The TaskEventStore Object stores events (such as a task being marked as done or being excused) related to a task.
    Attributes:
        events (array [TaskEvent Object]): An array of events that are related to the task.
        done (bool): Whether the task is marked as done or not.
        read (bool): Whether the latest updates of the task have been read.
        has_file_submission (bool): Whether a file has been submitted.
        mark (float): The mark for the task. Is None if no mark was given.
        grade (str): The grade for the task. Is None if no grade was given.
        added_files (array [File Object]): An array of files that have been submitted.
    Raises:
        Warning.warning: A prompt to submit a task event that has not been seen before. Follow instructions in warning.
    """
    def __init__(self, events_data, account_guid):
        self.events = []
        self.done = False
        # self.task_archived = False
        self.read = True
        self.has_file_submission = False
        self.grade = None
        self.mark = None
        self.added_files = []
        for event in events_data:
            is_student_event = False
            if account_guid == event["authorGuid"]:
                is_student_event = True
            if event["eventType"] not in event_types:
                warnings.warn(f"\nPlease raise an issue on the FireflyAPI GitHub repository with the following text attached (please remove any personal data): \n {json.dumps(event, indent=4, sort_keys=True)}")
            else:
                self.events.append(event_types[event["eventType"]](event, is_student_event))
        self.events.sort(key=lambda event: event.createdTime)
        for task_event in self.events:
            if type(task_event) == MarkAsDoneTaskEvent or type(task_event) == ConfirmCompletedTaskEvent:
                self.done = True
            elif type(task_event) == MarkAsUndoneTaskEvent:
                self.done = False
            # elif type(task_event) == ArchiveTaskEvent:
            #    self.task_archived = True
            # elif type(task_event) == UnarchiveTaskEvent:
            #    self.task_archived = False
            elif type(task_event) == AddFileTaskEvent:
                self.added_files.append(task_event.file)
            elif type(task_event) == MarkAndGradeTaskEvent:
                self.grade = task_event.grade
                self.mark = task_event.mark
            elif type(task_event) == AddFileTaskEvent:
                if task_event.is_student_event:
                    self.has_file_submission = True
            if not task_event.read:
                self.read = False
