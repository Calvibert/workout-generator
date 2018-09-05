# In anaerobics
CONST_MUSCLES = {
    'upper': [
        'abdominals',
        'biceps',
        'chest',
        'forearms',
        'lats',
        'lower back',
        'middle back',
        'neck',
        'shoulders',
        'traps',
        'triceps'
    ],
    'lower': [
        'abductors',
        'adductors',
        'calves',
        'glutes',
        'hamstrings',
        'quadriceps'
    ],
    'aerobic': ['aerobics'],
    'flexibility': [
        'abdominals',
        'abs',
        'adductor',
        'back',
        'biceps',
        'calves',
        'glutes',
        'hamstring',
        'hamstrings',
        'hips',
        'lower back',
        'middle back',
        'neck',
        'quadriceps',
        'shoulders',
        'thighs',
        'triceps'
    ]
}

CONST_MAP_GOAL_QUANTITY = {
    'be_healthy': {
        'upper': [4, 4],
        'lower': [4, 4],
        'aerobic': [7],
        'flexibility': [1, 1, 1, 1, 1, 1, 1]
    },
    'get_jacked': {
        'upper': [3, 3, 3],
        'lower': [3, 3],
        'aerobic': [4],
        'flexibility': [1, 1, 1, 1, 1]
    },
    'lose_weight': {
        'upper': [2, 2],
        'lower': [2, 2],
        'aerobic': [8],
        'flexibility': [1, 1, 1, 1, 1, 1, 1, 1]
    }
}

CONST_FIREBASE_URL = 'https://workout-generator-f5894.firebaseio.com'

CONST_DIFFICULTY_LEVEL_EASY = 1

CONST_DIFFICULTY_LEVEL_HARD = 2

CONST_EMPTY_EXERCISE_DICT = {'upper': [], 'lower': [], 'aerobic': [], 'flexibility': []}