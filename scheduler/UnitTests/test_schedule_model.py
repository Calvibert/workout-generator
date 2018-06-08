import sys
sys.path.insert(0,'C:/Users/samue/Projects/healthifier/backend/')
import unittest
from unittest import TestCase
import scripts.Schedule.model_weekly as weekly
import warnings
import sys
import scripts.Schedule.UnitTests.test_config as config


def ignore_warnings(test_func):
    def do_test(self, *args, **kwargs):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", ResourceWarning)
            test_func(self, *args, **kwargs)
    return do_test


class TestModel(TestCase):

    @ignore_warnings
    def test_split_by_days(self):
        model = weekly.ScheduleModelWeekly()
        model.set_user(config.CONST_USER_ID)
        model.training_days = config.CONST_SPLIT_BY_DAYS_TRAINING_DAYS
        model.exercises = config.CONST_SPLIT_BY_DAYS_EXERCISES
        result = model.split_by_days()
        self.assertEqual(result, config.CONST_SPLIT_BY_DAYS_RESULT)

    @ignore_warnings
    def test_build_json(self):
        model = weekly.ScheduleModelWeekly()
        model.set_user(config.CONST_USER_ID)
        model.exercises = config.CONST_BUILD_JSON_EXERCISES
        result = model.build_json()
        self.assertEqual(result, config.CONST_BUILD_JSON_RESULT)


if __name__ == '__main__':
    unittest.main()
    sys.exit()

