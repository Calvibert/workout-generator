import sys
sys.path.insert(0,'C:/Users/samue/Projects/healthifier/backend/')
import unittest
from unittest import TestCase, mock
import scripts.Schedule.Library.date as date_lib
import scripts.Schedule.model_factory as factory
import scripts.Schedule.model_weekly as weekly
import scripts.Schedule.model_daily as daily
import warnings


def ignore_warnings(test_func):
    def do_test(self, *args, **kwargs):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", ResourceWarning)
            test_func(self, *args, **kwargs)
    return do_test


class TestModel(TestCase):

    @ignore_warnings
    def test_model_factory_no_user(self):
        model = factory.ScheduleModelFactory('wrong_user_id').dispatch()
        self.assertEqual(model, 'User does not exist')

    @ignore_warnings
    def test_model_daily_factory(self):
        test_factory = factory.ScheduleModelFactory('OnrOomBTBWVMMD2scVWbqCSlnTQ2')
        test_factory.schema = 2
        model = test_factory.dispatch()
        if date_lib.is_sunday():
            self.assertEqual(type(model), type(weekly.ScheduleModelWeekly()))
        else:
            self.assertEqual(type(model), type(daily.ScheduleModelDaily()))

    @ignore_warnings
    def test_model_weekly_factory(self):
        test_factory = factory.ScheduleModelFactory('OnrOomBTBWVMMD2scVWbqCSlnTQ2')
        test_factory.schema = 1
        model = test_factory.dispatch()
        self.assertEqual(type(model), type(weekly.ScheduleModelWeekly()))


if __name__ == '__main__':
    unittest.main()
    sys.exit()