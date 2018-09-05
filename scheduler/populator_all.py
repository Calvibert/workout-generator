#
# Run this script locally to generate a weekly workout for all users
#

import config as conf
import model_factory as factory
from firebase import firebase as firebase

firebase = firebase.FirebaseApplication(conf.CONST_FIREBASE_URL, None)
user_ids = firebase.get('/users/', None, connection=None)

for id in user_ids:
    model = factory.ScheduleModelFactory(id).dispatch()
    if type(model) is str:
        print(model)
    else:
        print('Workout for ' + id + ':')
        model.set_user(id)
        result = model.generate_schedule()
        print(result)
