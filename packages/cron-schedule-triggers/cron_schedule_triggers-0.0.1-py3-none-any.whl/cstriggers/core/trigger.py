from collections import OrderedDict
from datetime import datetime

from cstriggers.core import parser, constants
from cstriggers.core.helper import dynamic_strp, constructed_kwargs, next_unit


class QuartzCron(object):
    def __init__(self, schedule_string=None, start_date=None, end_date=None):
        self.schedule_string = schedule_string.upper()
        self.schedule_dates = []

        schedule_parts = self.schedule_string.split()

        # QuartzCron `year` values are optional.
        if len(schedule_parts) == 6:
            schedule_parts.append("")

        self.time_units = OrderedDict(
            constructed_kwargs(
                ["second", "minute", "hour", "day", "month", "day_of_week", "year"],
                schedule_parts
            )
        )

        self.start_date, self.end_date = start_date, end_date

        self.date_pointer = self._init_pointer(self.start_date)
        self.end_date_pointer = self._init_pointer(self.end_date, fallback=constants.CRON_RANGE_END)

    @staticmethod
    def _init_pointer(date, fallback=None):
        """ Initializes a pointer datetime from start_date input. """
        if type(date) == datetime:
            return date
        elif date is None:
            if fallback is None:
                raise TypeError("date, or fallback date should be of type `datetime` or `str`.")
            return dynamic_strp(fallback, constants.DATETIME_FORMATS)

        return dynamic_strp(date, constants.DATETIME_FORMATS)

    def last_trigger(self):
        raise NotImplementedError

    def last_triggers(self, number_of_triggers=1):
        raise NotImplementedError

    @staticmethod
    def _get_parser(time_unit):
        """ Retrieves a parser for a time_unit. """
        return {
            "second": parser.CronSecondParser,
            "minute": parser.CronMinuteParser,
            "hour": parser.CronHourParser,
            "day": parser.CronDayParser,
            "day_of_week": parser.CronDayOfWeekParser,
            "month": parser.CronMonthParser,
            "year": parser.CronYearParser,
        }[time_unit]

    @staticmethod
    def _scale_ordered_unit_names(unit_names):
        """
            Swap the day_of_week and month order so that 'overflow' happens in the right order.
            :returns: unit names in ascending order of scale
        """
        unit_names[4],  unit_names[5] = unit_names[5],  unit_names[4]
        return unit_names

    def process_time_unit_queue(self, overflow, unit_names, ignore_pointer=False, counter=None,
                                recalculate_parent=False):
        """
            Space delimited Cron values are parsed in a queue.
            The logic of parsing of those delimited values have dependencies sometimes.
            To fulfill dependencies between delimtied values,
            a value may be added back to a 'followup queue' multiple times.
        """
        units, unit_names = unit_names, []
        followup_queue = []
        counter = counter or 0

        if recalculate_parent:
            units.append(next_unit(units[-1]))

        for unit_name in units:
            time_unit_value = self.time_units[unit_name]
            if overflow or ignore_pointer:
                self.date_pointer, overflow, recalculate_units = self._get_parser(unit_name)().parse(
                    self.date_pointer,
                    time_unit_value,
                    ignore_pointer=ignore_pointer,
                )
                followup_queue += recalculate_units or []

        if followup_queue:
            if counter == 0 and not ignore_pointer:
                self.process_time_unit_queue(
                    True,
                    followup_queue,
                    ignore_pointer=True,
                    counter=counter + 1
                )
            elif 12 > counter > 0:
                self.process_time_unit_queue(
                    True,
                    followup_queue,
                    counter=counter + 1,
                    recalculate_parent=True
                )

        return followup_queue

    def next_trigger(self, isoformat=False):
        """ Iterates through Cron Parsers to find the next valid trigger. """
        overflow = True
        unit_names = self._scale_ordered_unit_names(list(self.time_units.keys()))
        start_year = self.date_pointer.year

        self.process_time_unit_queue(overflow, unit_names)

        if (self.date_pointer.year < start_year) or (self.end_date_pointer < self.date_pointer):
            raise StopIteration("This cron schedule has reached its end-date.")

        return self.date_pointer.isoformat() if isoformat else self.date_pointer

    def next_triggers(self, number_of_triggers=1, isoformat=False):
        """
            Iterates through a Cron Parsers a series of times according to `number_of_triggers`
            to produce a list of trigger datetimes.
        """

        for _ in range(number_of_triggers):
            try:
                self.schedule_dates.append(self.next_trigger(isoformat=isoformat))
            except StopIteration:
                break

        _schedule_dates = self.schedule_dates
        self.schedule_dates = []

        return _schedule_dates
