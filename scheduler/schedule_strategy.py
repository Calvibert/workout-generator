"""
Strategy pattern for proper handling of the different algorithms.
"""

import abc
import schedule_daily as md
import schedule_weekly as mw

class ScheduleStrategy(object, __metaclass__ = abc.ABCMeta):
    
    @abc.abstractmethod
    def generate(self):
        pass
