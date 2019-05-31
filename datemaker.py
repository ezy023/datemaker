#!/usr/bin/env python

import argparse
import calendar
import datetime
import re


DATE_FORMAT_STRING = "%Y-%m-%d"
TIME_FORMAT_STRING = "%H:%M:%S"
DATETIME_FORMAT_STRING = DATE_FORMAT_STRING + " " + TIME_FORMAT_STRING

EXP_DATE_STRING = "yyyy-mm-dd"
EXP_TIME_STRING = "HH-MM-SS"
EXP_DATETIME_STRING = EXP_DATE_STRING + " " + EXP_TIME_STRING


def datetime_to_epoch(dt):
    return calendar.timegm(dt.timetuple())


def datetime_from_string(dt_string):
    if len(dt_string) == len(EXP_DATE_STRING):
        return datetime.datetime.strptime(dt_string, DATE_FORMAT_STRING)
    elif len(dt_string) == len(EXP_DATETIME_STRING):
        return datetime.datetime.strptime(dt_string, DATETIME_FORMAT_STRING)
    else:
        raise TypeError("Invalid datetime string applied")


def datetimes_from_start_and_deltas(start_date, deltas):
    """
    param :start_date: Datetime object representing the date to which deltas will be applied
    param :deltas: List of integers representing time deltas in days to apply to start_date

    return: List of datetime objects representing each delta being applied to the start_date
            Example:
            [start_date + d1, start_date + d2, ...]
    """

    return map(lambda d: datetime_with_applied_delta_tuple(start_date, d), deltas)


def datetime_with_applied_delta_tuple(start_date, delta_int):
    return start_date + datetime.timedelta(days=delta_int)


def main_main(args):
    if args.start_date_string:
        start_date = datetime_from_string(args.start_date_string)
    else:
        start_date = datetime.datetime.now()

    time_deltas = args.deltas
    result_datetimes = datetimes_from_start_and_deltas(start_date, time_deltas)
    epochs = map(datetime_to_epoch, result_datetimes)

    for idx, ts in enumerate(epochs):
        print "%d: %d" % (time_deltas[idx], ts)


def build_argument_parser():
    parser = argparse.ArgumentParser(description="Make some epoch date ranges")
    parser.add_argument('--start', '-s', action='store', dest='start_date_string',
                            help='A string representing the date from which the deltas should be applied.\n' + \
                            'Date can be in the format "' + EXP_DATE_STRING + '" or "' + EXP_DATETIME_STRING + '"\n\n' + \
                            'Defaults to current datetime if not specified')
    parser.add_argument('--delta', '-d', action='append', metavar='DELTA', type=int, dest='deltas',
                            help='An integer representing a positive or negative amount of 24-hour periods to adjust *start* by')

    return parser


if __name__ == '__main__':
    parser = build_argument_parser()

    args = parser.parse_args()

    main_main(args)
