# Script used to take a filename and export the file data into firebase.
import sys
from firebase import firebase
import exercise_populator_config as conf

firebase = firebase.FirebaseApplication('https://healthifier-f583f.firebaseio.com', None)

muscles = conf.CONST_MUSCLES

print('Enter the file name: ')
filename = sys.stdin.readline()
filename = filename[0:len(filename)-1]

print('Enter the exercise type: ')
exercise_type = sys.stdin.readline()
exercise_type = exercise_type[0:len(exercise_type)-1]
path = '/exercises/' + exercise_type

f = open(filename, 'r')

for exercises in f:
    exercises = exercises.split(',')
    name = exercises[0].replace('/', ' ')
    print(name)
    muscle = exercises[1].strip()
    if exercise_type in muscles:
        if muscle in muscles[exercise_type]:
            getMuscleGroup = firebase.get(path, muscle)
            position = path + '/' + muscle
            child = {'name': name}
            firebase.put(position, name, child)
    else:
        getMuscleGroup = firebase.get(path, muscle)
        position = path + '/' + muscle
        child = {'name': name}
        firebase.put(position, name, child)
