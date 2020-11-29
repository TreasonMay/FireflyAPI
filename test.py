from FireflyAPI.init import *
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
tt = api.get_timetable()
start = datetime(2020, 11, 20)
end = datetime(2020, 11, 30)
lessons = tt.get_lessons(start, end)
for lesson in lessons:
    print(lesson.start)
hw = api.get_task_interface()
tasks = hw.get_tasks(TaskInterfaceFilter("AllIncludingArchived",results=50))
task = tasks[2]
print(task.can_mark_as_done())
print(task.title)
# task.markAsDone()