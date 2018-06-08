#
# Helper for our API endpoint. Responsible for calling the right methods of the schedule controller
#

import scripts.Schedule.config as conf
import scripts.Schedule.model_weekly as controller
from firebase import firebase as firebase


# Generate a weekly schedule
def generate_one(id, next_week=False):
    cont = controller.ScheduleController()
    cont.set_user(id)
    cont.generate_schedule()
    return 0


# Generate a weekly schedule for every user who does not yet have one
def generate_all(next_week=False):
    fire = firebase.FirebaseApplication(conf.CONST_FIREBASE_URL, None)
    users = fire.get('/users/', None)
    cont = controller.ScheduleController()
    for id in users:
        cont.set_user(id)
        cont.generate_schedule()
    return 0


# This function is going to refactor the week including the previously missed workouts
def refactor_schedule():
    return 0


