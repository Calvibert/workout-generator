#
# Run this script locally to generate a weekly workout for an input user
#

import sys
sys.path.insert(0,'C:/Users/samue/Projects/healthifier/backend/')
import scripts.Schedule.model_factory as factory


print('Enter the user ID: ')
user_id = sys.stdin.readline()
user_id = user_id[0:len(user_id)-1]

model = factory.ScheduleModelFactory(user_id).dispatch()

if type(model) is str:
    print(model)
else:
    print('Workout for ' + user_id + ':')
    model.set_user(user_id)
    result = model.generate_schedule()
    print(result)
