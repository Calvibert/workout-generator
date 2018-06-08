#
#   Created by Samuel Dufresne on 2018-03-03
#

from datetime import datetime, timedelta
import dateutil.parser as parser


# Returns the Monday of the current week
def get_monday():
    weekday = datetime.today().weekday()
    monday = datetime.today() - timedelta(days=weekday)
    monday_str = str(monday.year) + "-" + str(monday.month) + "-" + str(monday.day)
    return monday_str


# Return true if Sunday
def is_sunday():
    if datetime.today().weekday() == 6:
        return True
    return False


# Returns the available training days
def get_available_days(training_days):
    available_days = {}
    monday = get_monday()
    for day, value in training_days.items():
        if value:
            day = day_to_date(monday, day)
            available_days[day] = value
    return available_days


# Returns the remaining training days within the week
def get_remaining_days(training_days):
    available_days = {}
    monday = get_monday()
    today = get_today()
    for day, value in training_days.items():
        day = day_to_date(monday, day)
        if value & (parser.parse(day) >= parser.parse(today)):
            available_days[day] = value
    return available_days


# Returns the date conform to the system dates
def day_to_date(monday, day):
    monday = datetime.strptime(monday, "%Y-%m-%d")
    selector = {
        'monday': 0,
        'tuesday': 1,
        'wednesday': 2,
        'thursday': 3,
        'friday': 4,
        'saturday': 5,
        'sunday': 6
    }[day]
    day = monday + timedelta(days=selector)
    return str(day.year) + "-" + str(day.month) + "-" + str(day.day)


# Return the monday of the previous week
def get_last_monday():
    weekday = datetime.today().weekday()
    monday = datetime.today() - timedelta(days=weekday)
    last_monday = monday - timedelta(days=7)
    last_monday_str = str(last_monday.year) + "-" + str(last_monday.month) + "-" + str(last_monday.day)
    return last_monday_str


# Return properly formatted today
def get_today():
    today = datetime.today()
    today = str(today.year) + "-" + str(today.month) + "-" + str(today.day)
    return today
