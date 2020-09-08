from django.test import TestCase
from calendars.models import Habit, HabitStreak
from django.contrib.auth.models import User
import datetime

class TestHabitStreak(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username="test", password="test")

        cls.habit_freq_everyday = Habit.objects.create(
            name="testHabit1", 
            creator=cls.user, 
            creationDate=datetime.date(2020,8,1),
            monday=True, tuesday=True, wednesday=True,
            thursday=True, friday=True, saturday=True,
            sunday=True)
        cls.habit_freq_every_other_day = Habit.objects.create(
            name="testHabit2", 
            creator=cls.user, 
            creationDate=datetime.date(2020,8,1),
            monday=True, tuesday=False, wednesday=True,
            thursday=False, friday=True, saturday=False,
            sunday=True)
        cls.habit_freq_one_day = Habit.objects.create(
            name="testHabit2", 
            creator=cls.user, 
            creationDate=datetime.date(2020,8,1),
            monday=False, tuesday=False, wednesday=True,
            thursday=False, friday=False, saturday=False,
            sunday=False)
        cls.habit_freq_random = Habit.objects.create(
            name="testHabit2", 
            creator=cls.user, 
            creationDate=datetime.date(2020,8,1),
            monday=False, tuesday=True, wednesday=False,
            thursday=False, friday=False, saturday=True,
            sunday=True)
        
        cls.habitStreak_freq_everyday = HabitStreak.objects.create(
            habit=cls.habit_freq_everyday,
            startDate=datetime.date(2020,8,20),
            endDate=datetime.date(2020,9,5),
            frequency=cls.habit_freq_everyday.frequency()
        )
        cls.habitStreak_freq_every_other_day = HabitStreak.objects.create(
            habit=cls.habit_freq_every_other_day,
            startDate=datetime.date(2020,8,19),
            endDate=datetime.date(2020,9,4),
            frequency=cls.habit_freq_every_other_day.frequency()
        )
        cls.habitStreak_freq_one_day = HabitStreak.objects.create(
            habit=cls.habit_freq_one_day,
            startDate=datetime.date(2020,8,26),
            endDate=datetime.date(2020,9,2),
            frequency=cls.habit_freq_one_day.frequency()
        )
        cls.habitStreak_freq_random = HabitStreak.objects.create(
            habit=cls.habit_freq_random,
            startDate=datetime.date(2020,9,1),
            endDate=datetime.date(2020,9,5),
            frequency=cls.habit_freq_random.frequency()
        )

    def setUp(self):
        self.user.refresh_from_db()
        self.habit_freq_everyday.refresh_from_db()
        self.habit_freq_every_other_day.refresh_from_db()
        self.habit_freq_one_day.refresh_from_db()
        self.habit_freq_random.refresh_from_db()
        self.habitStreak_freq_everyday.refresh_from_db()
        self.habitStreak_freq_every_other_day.refresh_from_db()
        self.habitStreak_freq_one_day.refresh_from_db()
        self.habitStreak_freq_random.refresh_from_db()
    
    # Tests for frequencyToArray
    def test_frequencyToArray_every_day(self):
        result = self.habitStreak_freq_everyday.frequencyToArray()
        expectedResult = [1,1,1,1,1,1,1]
        self.assertEqual(result, expectedResult)
    
    def test_frequencyToArray_every_other_day(self):
        result = self.habitStreak_freq_every_other_day.frequencyToArray()
        expectedResult = [1,0,1,0,1,0,1]
        self.assertEqual(result, expectedResult)

    def test_frequencyToArray_one_day(self):
        result = self.habitStreak_freq_one_day.frequencyToArray()
        expectedResult = [0,0,1,0,0,0,0]
        self.assertEqual(result, expectedResult)
    
    def test_frequencyToArray_random(self):
        result = self.habitStreak_freq_random.frequencyToArray()
        expectedResult = [0,1,0,0,0,1,1]
        self.assertEqual(result, expectedResult)
    

    #Tests for nextFrequencyDate
    def test_nextFrequencyDate_every_day(self):
        dateArgument = datetime.date(2020,9,4)
        expectedResult = datetime.date(2020,9,5)
        result = self.habitStreak_freq_everyday.nextFrequencyDate(dateArgument)
        self.assertEqual(result, expectedResult)
    
    def test_nextFrequencyDate_every_other_day(self):
        dateArgument = datetime.date(2020,9,4)
        expectedResult = datetime.date(2020,9,6)
        result = self.habitStreak_freq_every_other_day.nextFrequencyDate(dateArgument)
        self.assertEqual(result, expectedResult)

    def test_nextFrequencyDate_one_day(self):
        dateArgument = datetime.date(2020,9,2)
        expectedResult = datetime.date(2020,9,9)
        result = self.habitStreak_freq_one_day.nextFrequencyDate(dateArgument)
        self.assertEqual(result, expectedResult)
    
    def test_nextFrequencyDate_random(self):
        dateArgument = datetime.date(2020,8,30)
        expectedResult = datetime.date(2020,9,1)
        result = self.habitStreak_freq_random.nextFrequencyDate(dateArgument)
        self.assertEqual(result, expectedResult)
    
    def test_nextFrequencyDate_invalid_date_argument(self):
        self.assertRaises(TypeError, self.habitStreak_freq_random.nextFrequencyDate, "date")
    

    #Tests for previousFrequencyDate
    def test_previousFrequencyDate_every_day(self):
        dateArgument = datetime.date(2020,9,5)
        expectedResult = datetime.date(2020,9,4)
        result = self.habitStreak_freq_everyday.previousFrequencyDate(dateArgument)
        self.assertEqual(result, expectedResult)
    
    def test_previousFrequencyDate_every_other_day(self):
        dateArgument = datetime.date(2020,9,6)
        expectedResult = datetime.date(2020,9,4)
        result = self.habitStreak_freq_every_other_day.previousFrequencyDate(dateArgument)
        self.assertEqual(result, expectedResult)

    def test_previousFrequencyDate_one_day(self):
        dateArgument = datetime.date(2020,9,9)
        expectedResult = datetime.date(2020,9,2)
        result = self.habitStreak_freq_one_day.previousFrequencyDate(dateArgument)
        self.assertEqual(result, expectedResult)
    
    def test_previousFrequencyDate_random(self):
        dateArgument = datetime.date(2020,9,1)
        expectedResult = datetime.date(2020,8,30)
        result = self.habitStreak_freq_random.previousFrequencyDate(dateArgument)
        self.assertEqual(result, expectedResult)
    
    def test_previousFrequencyDate_invalid_date_argument(self):
        self.assertRaises(TypeError, self.habitStreak_freq_random.previousFrequencyDate, "date")
    

    #Tests for updateStartDate
    def test_updateStartDate_date_in_freq(self):
        newDate = datetime.date(2020,8,21)
        self.habitStreak_freq_every_other_day.updateStartDate(newDate)
        self.assertEqual(self.habitStreak_freq_every_other_day.startDate, newDate)
    
    def test_updateStartDate_date_not_in_freq(self):
        newDate = datetime.date(2020,8,20)
        oldStartDate = self.habitStreak_freq_every_other_day.startDate
        self.habitStreak_freq_every_other_day.updateStartDate(newDate)
        self.assertEqual(self.habitStreak_freq_every_other_day.startDate, oldStartDate)
    
    def test_updateStartDate_date_is_endDate(self):
        newDate = datetime.date(2020,9,4)
        self.habitStreak_freq_every_other_day.updateStartDate(newDate)
        self.assertEqual(self.habitStreak_freq_every_other_day.startDate, newDate)
    
    def test_updateStartDate_date_greater_than_endDate(self):
        newDate = datetime.date(2020,9,6)
        oldStartDate = self.habitStreak_freq_every_other_day.startDate
        self.habitStreak_freq_every_other_day.updateStartDate(newDate)
        self.assertEqual(self.habitStreak_freq_every_other_day.startDate, oldStartDate)

    def test_updateStartDate_invalid_date_argument(self):
        self.assertRaises(TypeError,
            self.habitStreak_freq_every_other_day.updateStartDate,
            "date")

    
    #Tests for updateEndDate
    def test_updateEndDate_date_in_freq(self):
        newDate = datetime.date(2020,9,2)
        self.habitStreak_freq_every_other_day.updateEndDate(newDate)
        self.assertEqual(self.habitStreak_freq_every_other_day.endDate, newDate)
    
    def test_updateEndDate_date_not_in_freq(self):
        newDate = datetime.date(2020,9,5)
        oldEndDate = self.habitStreak_freq_every_other_day.endDate
        self.habitStreak_freq_every_other_day.updateEndDate(newDate)
        self.assertEqual(self.habitStreak_freq_every_other_day.endDate, oldEndDate)
    
    def test_updateEndDate_date_is_startDate(self):
        newDate = datetime.date(2020,8,19)
        self.habitStreak_freq_every_other_day.updateEndDate(newDate)
        self.assertEqual(self.habitStreak_freq_every_other_day.endDate, newDate)
    
    def test_updateEndDate_date_less_than_startDate(self):
        newDate = datetime.date(2020,8,17)
        oldEndDate = self.habitStreak_freq_every_other_day.endDate
        self.habitStreak_freq_every_other_day.updateEndDate(newDate)
        self.assertEqual(self.habitStreak_freq_every_other_day.endDate, oldEndDate)

    def test_updateEndDate_invalid_date_argument(self):
        self.assertRaises(TypeError,
            self.habitStreak_freq_every_other_day.updateEndDate,
            "date")
    
    #Tests for isInFrequency
    def test_isInFrequency(self):
        dateArgument = datetime.date(2020,9,5)
        self.assertTrue(self.habitStreak_freq_everyday.isInFrequency(dateArgument))
    
    def test_isInFrequency_not_in_freq(self):
        dateArgument = datetime.date(2020,9,5)
        self.assertFalse(self.habitStreak_freq_every_other_day.isInFrequency(dateArgument))
    
    def test_isInFrequency_invalid_date_argument(self):
        self.assertRaises(TypeError, self.habitStreak_freq_everyday.isInFrequency, "date")
    

    #Tests for isDateInStreak
    def test_isDateInStreak_middle_of_streak(self):
        dateArgument = datetime.date(2020,8,30)
        self.assertTrue(self.habitStreak_freq_everyday.isDateInStreak(dateArgument))
    
    def test_isDateInStreak_startDate(self):
        dateArgument = datetime.date(2020,8,20)
        self.assertTrue(self.habitStreak_freq_everyday.isDateInStreak(dateArgument))

    def test_isDateInStreak_endDate(self):
        dateArgument = datetime.date(2020,9,5)
        self.assertTrue(self.habitStreak_freq_everyday.isDateInStreak(dateArgument))
    
    def test_isDateInStreak_before_streak(self):
        dateArgument = datetime.date(2020,8,19)
        self.assertFalse(self.habitStreak_freq_everyday.isDateInStreak(dateArgument))
    
    def test_isDateInStreak_after_streak(self):
        dateArgument = datetime.date(2020,9,6)
        self.assertFalse(self.habitStreak_freq_everyday.isDateInStreak(dateArgument))

    def test_isDateInStreak_date_in_streak_not_in_freq(self):
        dateArgument = datetime.date(2020,9,1)
        self.assertFalse(self.habitStreak_freq_every_other_day.isDateInStreak(dateArgument))
    
    def test_isDateInStreak_date_not_in_streak_not_in_freq(self):
        dateArgument = datetime.date(2020,9,5)
        self.assertFalse(self.habitStreak_freq_every_other_day.isDateInStreak(dateArgument))
    
    def test_isDateInStreak_invalid_date_argument(self):
        self.assertRaises(TypeError, self.habitStreak_freq_every_other_day.isDateInStreak, "date")