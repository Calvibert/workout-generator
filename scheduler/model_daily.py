#
# Created by Samuel Dufresne on 2018-03-23
#

import sys
sys.path.insert(0,'C:/Users/samue/Projects/healthifier/backend/')
import scripts.Schedule.config as conf
import scripts.Schedule.Library.date as date_lib
import scripts.Schedule.model as model


class ScheduleModelDaily(model.ScheduleModel):

    def __init__(self):
        super(ScheduleModelDaily, self).__init__()

    """-------------------------------------------
                  PUBLIC INTERFACE
    -------------------------------------------"""

    # From the user id given, retrieve and set the user's data before processing
    def set_user(self, user_id):
        self.user_id = user_id
        self.user = self.user_repo[self.user_id]
        self.training_days = date_lib.get_remaining_days(self.user['trainingDays'])
        self.goal = self.user['goal']
        self.muscles = {}
        if 'muscles' in self.user:
            self.muscles = self.user['muscles']
        self.activity_count = conf.CONST_MAP_GOAL_QUANTITY[self.goal]
        self.exercises = conf.CONST_EMPTY_EXERCISE_DICT

        # Reset attributes to their default
        self.adapt_flag = True
        self.difficulty = conf.CONST_DIFFICULTY_LEVEL_EASY
        if self.has_settings():
            self.settings = self.user.get('settings')
            if not self.is_adaptive():
                self.adapt_flag = False
            if self.is_hard():
                self.difficulty = conf.CONST_DIFFICULTY_LEVEL_HARD

    # Generate the schedule and add it to Firebase
    def generate_schedule(self):
        if not self.has_remaining_days():
            return 'No remaining training days.'
        self.build_remaining_schedule()

        self.exercises = self.split_by_days()
        self.exercises = self.build_json()
        date = date_lib.get_monday()
        path = '/users/' + self.user_id + '/workouts'
        result = self.f_b.put(path, date, self.exercises)
        return result

    """----------------------------------------
                PRIVATE METHODS
    ----------------------------------------"""

    # Take previously missed from the week and add it to the rest of the week
    def build_remaining_schedule(self):
        monday = date_lib.get_monday()
        if self.user_has_no_workouts():
            return

        this_week_exercises = self.user['workouts'][monday]

        for day in this_week_exercises.items():
            if self.day_not_in_training_days(day) & self.adapt_flag:
                for key, exercise in day[1].items():
                    for e in exercise:
                        if self.is_incomplete(e):
                            self.exercises[key].append(e['name'])
            else:
                for key, exercise in day[1].items():
                    for e in exercise:
                        self.exercises[key].append(e['name'])

    def has_remaining_days(self):
        return self.training_days
