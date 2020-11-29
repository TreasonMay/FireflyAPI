import FireflyAPI
import datetime

# Replace with your own Authentication Blob
auth_blob = "eyJkZ...UwMSJ9"

# In this example we will try to:
# - Get all your lessons for today.
# - Get all your lessons for this week.

# Lets start by getting your timetable.
user_integration = FireflyAPI.AuthenticatedUser(auth_blob)
timetable = user_integration.get_timetable()

# Now that we have your timetable, lets get all the lessons you have today.

lessons_today = timetable.today()
for lesson in lessons_today:
    print(lesson)

# Now let's get the lessons you have this week.
# First we need to set out start and end times:

today = datetime.datetime.now()  # This is the time right now
start = today - datetime.timedelta(days=today.weekday())  # Start of this week
end = start + datetime.timedelta(days=6)  # End of this week

# Now we can get all the lessons between 'start' and 'end'.

lessons_this_week = timetable.get_lessons(start, end)
for lesson in lessons_today:
    print(
        f""" {lesson.subject}
          Starts: {lesson.start}, Ends: {lesson.end}.
          Teachers: {", ".join(lesson.teachers)}.
          Class: {", ".join(lesson.lesson_groups)}
          Location: {lesson.location}
        """)

# For more information on lessons, check the documentation for the Timetable and Lesson objects.
