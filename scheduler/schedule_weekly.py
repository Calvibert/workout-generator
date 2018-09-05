import random
import config as conf
import Library.date as date_lib
import schedule as model


class ScheduleModelWeekly(model.ScheduleModel):

    def __init__(self):
        super(ScheduleModelWeekly, self).__init__()

    """-------------------------------------------
                    PUBLIC INTERFACE
    -------------------------------------------"""

    # From the user id given, retrieve and set the user's data before processing
    def set_user(self, user_id):
        self.user_id = user_id
        self.user = self.user_repo[self.user_id]
        self.training_days = date_lib.get_available_days(self.user['trainingDays'])
        self.goal = self.user['goal']
        self.muscles = {}
        if 'muscles' in self.user:
            self.muscles = self.user['muscles']
        self.activity_count = conf.CONST_MAP_GOAL_QUANTITY[self.goal]
        self.exercises = conf.CONST_EMPTY_EXERCISE_DICT
        self.set_previously_missed()

        # Reset attributes to their default
        self.adapt_flag = True
        self.difficulty = conf.CONST_DIFFICULTY_LEVEL_EASY
        if self.has_settings():
            self.settings = self.user.get('settings')
            if not self.is_adaptive():
                self.adapt_flag = False
                self.previously_missed = conf.CONST_EMPTY_EXERCISE_DICT
            if self.is_hard():
                self.difficulty = conf.CONST_DIFFICULTY_LEVEL_HARD

    # Generates the schedule using the helper functions of this class
    def generate_schedule(self):
        for key in self.exercises:
            t_muscles = self.get_muscles(key)
            t_exercises = self.get_exercises(key, t_muscles)
            self.exercises[key] = t_exercises

        self.exercises = self.split_by_days()
        self.exercises = self.build_json()
        date = date_lib.get_monday()
        path = '/users/' + self.user_id + '/workouts'
        result = self.f_b.put(path, date, self.exercises, connection=None)
        return result

    """----------------------------------------
                 PRIVATE METHODS
    ----------------------------------------"""

    # Returns a randomized subset of muscles
    def get_muscles(self, muscle_type):
        activity_count = self.activity_count[muscle_type]
        muscle_group = conf.CONST_MUSCLES[muscle_type][:]
        updated_muscle_group = muscle_group[:]
        user_muscles = []
        if muscle_type in self.muscles:
            user_muscles = self.muscles[muscle_type]
        path = '/users/' + self.user_id + '/muscles'

        for key in muscle_group:
            if key in user_muscles:
                updated_muscle_group.remove(key)

        if len(updated_muscle_group) < len(activity_count):
            updated_muscle_group = conf.CONST_MUSCLES[muscle_type][:]
            user_muscles = []
            self.f_b.put(path, type, user_muscles, connection=None)

        list = []
        for _ in range(0, len(activity_count)):
            list.append(updated_muscle_group[random.randrange(0, len(updated_muscle_group))])
            updated_muscle_group.remove(list[-1])

        user_muscles = user_muscles + list
        self.f_b.put(path, muscle_type, user_muscles, connection=None)
        return list

    # Returns a randomized list of exercises
    def get_exercises(self, muscle_type, muscle_list):
        array = []
        exercises = self.all_exercises[muscle_type]
        exercise_count = self.activity_count[muscle_type]
        exercises_array = []
        for index, muscle in enumerate(muscle_list):
            for exercise in exercises[muscle]:
                exercises_array.append(exercise)
            for _ in range(0, exercise_count[index]):
                array.append(exercises_array[random.randrange(0, len(exercises_array))])
        if self.previously_missed[muscle_type] and self.adapt_flag:
            for entry in self.previously_missed[muscle_type]:
                array.append(entry)
        return array

    # Runs every time a new schedule is generated. Look to the previous week for incomplete activities
    def set_previously_missed(self):
        self.previously_missed = self.exercises
        last_monday = date_lib.get_last_monday()
        if not self.user_has_no_workouts():
            return
        if self.user_first_week(last_monday):
            return
        last_week_exercises = self.user['workouts'][last_monday]
        previously_missed = self.exercises

        for day in last_week_exercises.items():
            for key, exercise in day[1].items():
                for e in exercise:
                    if self.is_incomplete(e):
                        previously_missed[key].append(e['name'])


