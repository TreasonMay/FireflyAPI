from FireflyAPI.__init__ import *
import sys
from datetime import datetime
#api = UserIntegration("","kh2n1srandomrandomejjewj4", integration_name="FF API TEST2").createIntegration()
#print(api.auth_blob)
#sys.exit()
ab_file = open("my_auth_blob.txt", 'r')
my_ab = ab_file.read()
ab_file.close()
api = AuthenticatedUser(my_ab)
print(api.auth_blob)
ti = api.get_task_interface()
task = ti.get_task_by_id(156504)
file_submission = api.make_file_folder()
file_submission.upload_file(open("LICENSE.md",'rb'), "Test file")
file_submission.upload_file(open("README.md",'rb'), "Test file 2")
task.upload_file(file_submission)
#file_submission = files.FileSubmission(api.auth_blob)
#file_submission.upload_file(open("LICENSE.md",'rb'), "Test file")
#for message in api.get_messages()[:6]:
    # message.unarchive()
#    print(message.message_text)
#tt = api.get_timetable()
#start = datetime(2020, 11, 20)
#end = datetime(2020, 11, 30)
#lessons = tt.get_lessons(start, end)
#for lesson in lessons:
#    print(lesson.start)
'''hw = api.get_task_interface()
tasks = hw.get_tasks(TaskInterfaceFilter("AllIncludingArchived", read=True, results=100))
for task in tasks:
    print(task.title, task.personal_task)
    #task.mark_as_read()
'''
#tasks[3].add_comment("test comment")
# task.markAsDone()