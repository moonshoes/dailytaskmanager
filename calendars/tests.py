from django.test import TestCase
from .functions import (
    getPreviousMonth,
    getNextMonth,
    getPreviousDay,
    getNextDay,
    getPreviousWeek,
    getNextWeek,
    getCurrentWeek)
from .exceptions import InvalidMonthNumber
import datetime, calendar

class TestGetPreviousMonth(TestCase):
    def test_month_between_one_and_twelve(self):
        result = getPreviousMonth(2020, 7)
        expectedResult = {
            'year': 2020,
            'month': 6
        }
        self.assertEqual(result, expectedResult)
    
    def test_month_one(self):
        result = getPreviousMonth(2020, 1)
        expectedResult = {
            'year': 2019,
            'month': 12
        }
        self.assertEqual(result, expectedResult)
    
    def test_month_twelve(self):
        result = getPreviousMonth(2020, 12)
        expectedResult = {
            'year': 2020,
            'month': 11
        }
        self.assertEqual(result, expectedResult)
    
    def test_month_zero(self):
        self.assertRaises(InvalidMonthNumber, getPreviousMonth, 2020, 0)
    
    def test_month_thirteen(self):
        self.assertRaises(InvalidMonthNumber, getPreviousMonth, 2020, 13)

class TestGetNextMonth(TestCase):
    def test_month_between_one_and_twelve(self):
        result = getNextMonth(2020, 7)
        expectedResult = {
            'year': 2020,
            'month': 8
        }
        self.assertEqual(result, expectedResult)
    
    def test_month_one(self):
        result = getNextMonth(2020, 1)
        expectedResult = {
            'year': 2020,
            'month': 2
        }
        self.assertEqual(result, expectedResult)
    
    def test_month_twelve(self):
        result = getNextMonth(2020, 12)
        expectedResult = {
            'year': 2021,
            'month': 1
        }
        self.assertEqual(result, expectedResult)
    
    def test_month_zero(self):
        self.assertRaises(InvalidMonthNumber, getNextMonth, 2020, 0)
    
    def test_month_thirteen(self):
        self.assertRaises(InvalidMonthNumber, getNextMonth, 2020, 13)


class TestGetPreviousDay(TestCase):
    def test_middle_of_month_day(self):
        today = datetime.date(2020, 7, 10)
        result = getPreviousDay(today)
        expectedResult = {
            'year': 2020,
            'month': 7,
            'day': 9,
        }
        self.assertEqual(result, expectedResult)

    def test_beginning_of_month(self):
        today = datetime.date(2020, 7, 1)
        result = getPreviousDay(today)
        expectedResult = {
            'year': 2020,
            'month': 6,
            'day': 30,
        }
        self.assertEqual(result, expectedResult)
    
    def test_beginning_of_year(self):
        today = datetime.date(2020, 1, 1)
        result = getPreviousDay(today)
        expectedResult = {
            'year': 2019,
            'month': 12,
            'day': 31,
        }
        self.assertEqual(result, expectedResult)
    
    def test_incorrect_argument(self):
        self.assertRaises(TypeError, getPreviousDay, "date")

class TestGetNextDay(TestCase):
    def test_middle_of_month_day(self):
        today = datetime.date(2020, 7, 10)
        result = getNextDay(today)
        expectedResult = {
            'year': 2020,
            'month': 7,
            'day': 11,
        }
        self.assertEqual(result, expectedResult)

    def test_end_of_month(self):
        today = datetime.date(2020, 7, 31)
        result = getNextDay(today)
        expectedResult = {
            'year': 2020,
            'month': 8,
            'day': 1,
        }
        self.assertEqual(result, expectedResult)
    
    def test_end_of_year(self):
        today = datetime.date(2020, 12, 31)
        result = getNextDay(today)
        expectedResult = {
            'year': 2021,
            'month': 1,
            'day': 1,
        }
        self.assertEqual(result, expectedResult)
    
    def test_incorrect_argument(self):
        self.assertRaises(TypeError, getNextDay, "date")

class TestGetPreviousWeek(TestCase):
    def test_middle_of_month_day(self):
        today = datetime.date(2020, 7, 10)
        result = getPreviousWeek(today)
        expectedResult = {
            'year': 2020,
            'month': 7,
            'day': 3,
        }
        self.assertEqual(result, expectedResult)

    def test_beginning_of_month(self):
        today = datetime.date(2020, 7, 1)
        result = getPreviousWeek(today)
        expectedResult = {
            'year': 2020,
            'month': 6,
            'day': 24,
        }
        self.assertEqual(result, expectedResult)
    
    def test_beginning_of_year(self):
        today = datetime.date(2020, 1, 1)
        result = getPreviousWeek(today)
        expectedResult = {
            'year': 2019,
            'month': 12,
            'day': 25,
        }
        self.assertEqual(result, expectedResult)
    
    def test_incorrect_argument(self):
        self.assertRaises(TypeError, getPreviousWeek, "date")

class TestGetNextWeek(TestCase):
    def test_middle_of_month_day(self):
        today = datetime.date(2020, 7, 10)
        result = getNextWeek(today)
        expectedResult = {
            'year': 2020,
            'month': 7,
            'day': 17,
        }
        self.assertEqual(result, expectedResult)

    def test_end_of_month(self):
        today = datetime.date(2020, 7, 31)
        result = getNextWeek(today)
        expectedResult = {
            'year': 2020,
            'month': 8,
            'day': 7,
        }
        self.assertEqual(result, expectedResult)
    
    def test_end_of_year(self):
        today = datetime.date(2020, 12, 31)
        result = getNextWeek(today)
        expectedResult = {
            'year': 2021,
            'month': 1,
            'day': 7,
        }
        self.assertEqual(result, expectedResult)
    
    def test_incorrect_argument(self):
        self.assertRaises(TypeError, getNextWeek, "date")

class TestGetCurrentWeek(TestCase):
    def setUp(self):
        self.maxDiff = None
        self.userCalendar = calendar.Calendar(0)
        self.weekList = []
        for i in range(6, 13):
            self.weekList.append(datetime.date(2020, 7, i))
    
    def test_middle_of_month_middle_of_week(self):
        today = datetime.date(2020, 7, 10)
        result = getCurrentWeek(today, self.userCalendar)
        expectedResult = {
            'weekDaysList': self.weekList,
            'firstWeekDay': datetime.date(2020, 7, 6),
            'lastWeekDay': datetime.date(2020, 7, 12),
        }
        self.assertEqual(result, expectedResult)
    
    def test_middle_of_month_beginning_of_week(self):
        today = datetime.date(2020, 7, 6)
        result = getCurrentWeek(today, self.userCalendar)
        expectedResult = {
            'weekDaysList': self.weekList,
            'firstWeekDay': datetime.date(2020, 7, 6),
            'lastWeekDay': datetime.date(2020, 7, 12),
        }
        self.assertEqual(result, expectedResult)

    def test_middle_of_month_end_of_week(self):
        today = datetime.date(2020, 7, 12)
        result = getCurrentWeek(today, self.userCalendar)
        expectedResult = {
            'weekDaysList': self.weekList,
            'firstWeekDay': datetime.date(2020, 7, 6),
            'lastWeekDay': datetime.date(2020, 7, 12),
        }
        self.assertEqual(result, expectedResult)

    def test_beginning_of_month(self):
        today = datetime.date(2020, 7, 1)
        result = getCurrentWeek(today, self.userCalendar)

        expectedWeekList = [
            datetime.date(2020, 6, 29),
            datetime.date(2020, 6, 30)
        ]
        for i in range(1, 6):
            expectedWeekList.append(datetime.date(2020, 7, i))

        expectedResult = {
            'weekDaysList': expectedWeekList,
            'firstWeekDay': datetime.date(2020, 6, 29),
            'lastWeekDay': datetime.date(2020, 7, 5),
        }
        self.assertEqual(result, expectedResult)

    def test_end_of_month(self):
        today = datetime.date(2020, 7, 31)
        result = getCurrentWeek(today, self.userCalendar)

        expectedWeekList = []
        for i in range(27, 32):
            expectedWeekList.append(datetime.date(2020, 7, i))
        expectedWeekList.append(datetime.date(2020, 8, 1))
        expectedWeekList.append(datetime.date(2020, 8, 2))

        expectedResult = {
            'weekDaysList': expectedWeekList,
            'firstWeekDay': datetime.date(2020, 7, 27),
            'lastWeekDay': datetime.date(2020, 8, 2),
        }
        self.assertEqual(result, expectedResult)
        
    def test_beginning_of_year(self):
        today = datetime.date(2020, 1, 1)
        result = getCurrentWeek(today, self.userCalendar)

        expectedWeekList = [
            datetime.date(2019, 12, 30),
            datetime.date(2019, 12, 31)
        ]
        for i in range(1, 6):
            expectedWeekList.append(datetime.date(2020, 1, i))

        expectedResult = {
            'weekDaysList': expectedWeekList,
            'firstWeekDay': datetime.date(2019, 12, 30),
            'lastWeekDay': datetime.date(2020, 1, 5),
        }
        self.assertEqual(result, expectedResult)
    
    def test_end_of_year(self):
        today = datetime.date(2020, 12, 31)
        result = getCurrentWeek(today, self.userCalendar)

        expectedWeekList = [
            datetime.date(2020, 12, 28),
            datetime.date(2020, 12, 29),
            datetime.date(2020, 12, 30),
            datetime.date(2020, 12, 31),
            datetime.date(2021, 1, 1),
            datetime.date(2021, 1, 2),
            datetime.date(2021, 1, 3),
        ]

        expectedResult = {
            'weekDaysList': expectedWeekList,
            'firstWeekDay': datetime.date(2020, 12, 28),
            'lastWeekDay': datetime.date(2021, 1, 3),
        }
        self.assertEqual(result, expectedResult)
    
    def test_invalid_day_argument(self):
        self.assertRaises(TypeError, getCurrentWeek, "date", self.userCalendar)
    
    def test_invalid_calendar_argument(self):
        today = datetime.date(2020, 7, 10)
        self.assertRaises(TypeError, getCurrentWeek, today, "calendar")