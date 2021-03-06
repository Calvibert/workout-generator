#
# Factory of model
#

from firebase import firebase as firebase
from random import randint
import config as conf
import schedule_weekly as weekly
import schedule_daily as daily
import Library.date as date


class ScheduleModelFactory():

    def __init__(self, user_id):
        self.f_b = firebase.FirebaseApplication(conf.CONST_FIREBASE_URL, None)
        self.user_repo = self.f_b.get('/users/', None, connection=None)
        self.user = None
        self.user_id = user_id
        self.schema = None
        if self.user_exists():
            self.user = self.user_repo[user_id]
            self.set_schema()

    # Return the proper Model
    def dispatch(self):
        # On last day of the week, regenerate a new schedule
        if date.is_sunday():
            return weekly.ScheduleModelWeekly()
        if self.schema == 1:
            return weekly.ScheduleModelWeekly()
        if self.schema == 2:
            return daily.ScheduleModelDaily()
        return 'User does not exist'

        # A/B test: Issue #23
    def init_adaptive_schedule(self):
        path = '/users/' + self.user_id + '/settings/'
        self.schema = randint(1, 2)
        self.f_b.put(path, 'adaptive_schema', self.schema, connection=None)

    def user_exists(self):
        return self.user_repo.get(self.user_id)

    def set_schema(self):
        if self.has_settings():
            if self.has_schema():
                self.schema = self.user.get('settings').get('adaptive_schema')
                return
        self.init_adaptive_schedule()

    def has_settings(self):
        return self.user.get('settings')

    def has_schema(self):
        return self.user.get('settings').get('adaptive_schema')
