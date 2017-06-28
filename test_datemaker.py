import unittest
import datetime

from datemaker import datetime_from_string
from datemaker import build_argument_parser
from datemaker import datetimes_from_start_and_deltas

class TestDateMaker(unittest.TestCase):

    def test_datetime_from_string_date_only(self):
        datetime_string = "2017-06-10"
        date = datetime_from_string(datetime_string)

        self.assertEquals(2017, date.year)
        self.assertEquals(6, date.month)
        self.assertEquals(10, date.day)


    def test_datetime_from_string_with_time(self):
        datetime_string = "2017-06-10 12:00:00"
        datetime = datetime_from_string(datetime_string)

        self.assertEquals(2017, datetime.year)
        self.assertEquals(6, datetime.month)
        self.assertEquals(10, datetime.day)
        self.assertEquals(12, datetime.hour)
        self.assertEquals(0, datetime.minute)
        self.assertEquals(0, datetime.second)


    def test_arg_parser_parse_single_delta(self):
        arg_string = "-d +3"
        arg_string_verbose = "--delta +3"

        parser = build_argument_parser()
        args = parser.parse_args(arg_string.split())
        args_verbose = parser.parse_args(arg_string_verbose.split())

        self.assertEquals([3], args.deltas)
        self.assertEquals([3], args_verbose.deltas)

    def test_arg_parser_negative_delta_args(self):
        args_string = '--delta -11 -d -3 -d -4'
        parser = build_argument_parser()
        args = parser.parse_args(args_string.split())

        self.assertEqual([-11, -3, -4], args.deltas)


    def test_arg_parser_parse_start_date(self):
        arg_string = "-s 2017-06-24"
        arg_string_verbose = "--start 2017-06-24"

        parser = build_argument_parser()
        args = parser.parse_args(arg_string.split())
        args_verbose = parser.parse_args(arg_string_verbose.split())

        self.assertEquals("2017-06-24", args.start_date_string)


    def test_datetimes_from_start_and_deltas(self):
        start_date = datetime.datetime(year=2017, month=6, day=24)
        deltas = [1]

        applied_deltas = datetimes_from_start_and_deltas(start_date, deltas)

        self.assertEqual(1, len(applied_deltas))
        self.assertEqual(2017, applied_deltas[0].year)
        self.assertEqual(6, applied_deltas[0].month)
        self.assertEqual(25, applied_deltas[0].day)


    def test_datetimes_from_start_and_deltas_multiple_deltas(self):
        start_date = datetime.datetime(year=2017, month=6, day=24)
        deltas = [1, -1]

        applied_deltas = datetimes_from_start_and_deltas(start_date, deltas)

        self.assertEqual(2, len(applied_deltas))

        self.assertEqual(2017, applied_deltas[0].year)
        self.assertEqual(6, applied_deltas[0].month)
        self.assertEqual(25, applied_deltas[0].day)

        self.assertEqual(2017, applied_deltas[1].year)
        self.assertEqual(6, applied_deltas[1].month)
        self.assertEqual(23, applied_deltas[1].day)



if __name__ == '__main__':
    unittest.main()
