#
# Abstract class
# Head of schedule controller hierarchy
#
# Created by Samuel Dufresne on 2018-04-13
#

from abc import ABCMeta, abstractmethod
from firebase import firebase as firebase
import config as conf
import math


class ScheduleModel(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        self.f_b = firebase.FirebaseApplication(conf.CONST_FIREBASE_URL, None)
        self.user_repo = self.f_b.get('/users/', None, connection=None)
        self.all_exercises = self.f_b.get('/exercises', None, connection=None)
        self.muscles = conf.CONST_MUSCLES
        self.user_id = None
        self.user = None
        self.training_days = None
        self.goal = None
        self.muscles = None
        self.activity_count = None
        self.exercises = None
        self.adapt_flag = None
        self.previously_missed = None
        self.settings = None
        self.difficulty = None

    @abstractmethod
    def set_user(self, user_id): pass

    @abstractmethod
    def generate_schedule(self): pass

    # Splits exercise types in a per day basis
    def split_by_days(self):
        all_exercises = self.exercises
        training_days = self.training_days
        new_dict = {}
        num_days_len = len(training_days)
        exec_slice = {}
        # Init the slice number
        for key in all_exercises:
            exec_slice[key] = int(math.floor(len(all_exercises[key]) / num_days_len))
        for day in training_days:
            daily_exer = {}
            for key in all_exercises:
                daily_exer[key] = all_exercises[key][:exec_slice[key]]
                for _ in range(0, exec_slice[key]):
                    all_exercises[key].pop(0)
            new_dict[day] = daily_exer
        for key in all_exercises:
            if all_exercises[key]:
                new_dict[next(iter(training_days.keys()))][key].append(all_exercises[key][0])
        return new_dict

    # Builds a Json object from a passed list of exercises
    def build_json(self):
        exercises = self.exercises
        json = {}
        for day in exercises:
            json[day] = {}
            for ex_type in exercises[day]:
                count = 0
                json[day][ex_type] = {}
                for exer in exercises[day][ex_type]:
                    json[day][ex_type][count] = {
                        'name': exer,
                        'complete': False
                    }
                    count = count + 1
        return json

    # Check if the day is in the dict
    def day_not_in_training_days(self, day):
        return day[0] not in self.training_days

    # Check the complete parameter
    def is_incomplete(self, exercise):
        return not exercise['complete']

    # Check if user has generated workouts
    def user_has_no_workouts(self):
        return 'workouts' not in self.user

    # Check if the user has no exercises last week
    def user_first_week(self, last_monday):
        return not self.user.get('workouts')

    # Check if user has initiated settings
    def has_settings(self):
        return self.user.get('settings')

    # Check if the user has an adaptive schedule
    def is_adaptive(self):
        return self.settings.get('adaptive_schedule')

    # Check if the user has an hard schedule
    def is_hard(self):
        return self.settings.get('HARD')
