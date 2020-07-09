from django.test import TestCase
from .functions import getPreviousMonth, getNextMonth
from .exceptions import InvalidMonthNumber

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


