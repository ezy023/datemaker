#!/usr/bin/python

import argparse
import calendar
import datetime
import re

from collections import namedtuple

class Magnitude(object):
    DAY = 'day'
    WEEK = 'week'


DATE_FORMAT_STRING = "%Y-%m-%d"
TIME_FORMAT_STRING = "%H:%M:%S"
DATETIME_FORMAT_STRING = DATE_FORMAT_STRING + " " + TIME_FORMAT_STRING

EXP_DATE_STRING = "yyyy-mm-dd"
EXP_TIME_STRING = "HH-MM-SS"
EXP_DATETIME_STRING = EXP_DATE_STRING + " " + EXP_TIME_STRING

TIMEDELTA_STR_PATTERN = "([+-]?[0-9]+)([a-z]+)"

TimeDelta = namedtuple('timdelta', ['amount', 'magnitude'])
ParsedTuple = namedtuple('paredtuple', ['amount', 'identifier'])

def datetime_to_epoch(dt):
    return calendar.timegm(dt.timetuple())

def datetime_from_string(dt_string):
    if len(dt_string) == len(EXP_DATE_STRING):
        return datetime.datetime.strptime(dt_string, DATE_FORMAT_STRING)
    elif len(dt_string) == len(EXP_DATETIME_STRING):
        return datetime.datetime.strptime(dt_string, DATETIME_FORMAT_STRING)
    else:
        raise TypeError("Invalid datetime string applied")


def parse_timedelta_string(delta_string):
    """
    Parse the delta_string to a tuple representing the amount and magnitude of the delta
    """
    delta_match = re.match(TIMEDELTA_STR_PATTERN, delta_string)
    if not delta_match:
        raise TypeError('Invalid timedelta. Proper format is "%s%s" % (int_amount, char_magnitude)')

    re_groups = delta_match.groups()

    parsed_tuple = ParsedTuple(*re_groups)

    if parsed_tuple.identifier == 'd':
        return TimeDelta(int(parsed_tuple.amount), Magnitude.DAY)
    elif parsed_tuple.identifier == 'w':
        return TimeDelta(int(parsed_tuple.amount), Magnitude.WEEK)



def datetimes_from_start_and_deltas(start_date, deltas):
    """
    param :start_date: Datetime object representing the date to which deltas will be applied
    param :deltas: List of strings representing time deltas in days to apply to start_date

    return: List of datetime objects representing each delta being applied to the start_date
            Example:
            [start_date + d1, start_date + d2, ...]
    """

    parsed_delta_tuples = map(parse_timedelta_string, deltas)

    return map(lambda d: datetime_with_applied_delta_tuple(start_date, d), parsed_delta_tuples)


def datetime_with_applied_delta_tuple(start_date, delta_tuple):
    if delta_tuple.magnitude == Magnitude.DAY:
        return start_date + datetime.timedelta(days=delta_tuple.amount)
    elif delta_tuple.magnitude == Magnitude.WEEK:
        return start_date + datetime.timedelta(weeks=delta_tuple.amount)


def main_main(args):
    if args.start_date_string:
        start_date = datetime_from_string(args.start_date_string)
    else:
        start_date = datetime.datetime.now()

    time_deltas = args.deltas
    result_datetimes = datetimes_from_start_and_deltas(start_date, time_deltas)
    epochs = map(datetime_to_epoch, result_datetimes)

    for ts in epochs:
        print "%d" % ts


def cust_str(arg_str):
    return str(arg_str)


def build_argument_parser():
    parser = argparse.ArgumentParser(description="Make some epoch date ranges")
    parser.add_argument('--start', '-s', action='store', dest='start_date_string',
                            help='A string representing the date from which the deltas should be applied.\n' + \
                            'Date should be in the format "yyyy-mm-dd HH:MM:SS"\n\n' + \
                            'Defaults to current datetime if not specified')
    parser.add_argument('--delta', '-d', action='append', type=cust_str, dest='deltas',
                            help='An integer representing a positive or negative amount of days to adjust *start* by')

    return parser


if __name__ == '__main__':
    parser = build_argument_parser()

    args = parser.parse_args()
    print args
    # main_main(args)
    # args = parser.parse_args('--delta +1 -d -3'.split())
    # print args
    # timedeltas = args.deltas
