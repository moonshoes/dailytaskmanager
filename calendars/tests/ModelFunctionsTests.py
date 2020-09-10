from django.test import TestCase
from calendars.models import Habit, HabitStreak
from calendars.functions.modelFunctions import (
    getDisabledDaysHabit,
    getDailyHabits,
    getYearStreak
)
from django.contrib.auth.models import User
import datetime

class TestModelFunctions(TestCase):
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
            name="testHabit3", 
            creator=cls.user, 
            creationDate=datetime.date(2020,8,1),
            monday=False, tuesday=False, wednesday=True,
            thursday=False, friday=False, saturday=False,
            sunday=False)
        cls.habit_freq_random = Habit.objects.create(
            name="testHabit4", 
            creator=cls.user, 
            creationDate=datetime.date(2020,8,1),
            monday=False, tuesday=True, wednesday=False,
            thursday=False, friday=False, saturday=True,
            sunday=True)

    def setUp(self):
        self.user.refresh_from_db()
        self.habit_freq_everyday.refresh_from_db()
        self.habit_freq_every_other_day.refresh_from_db()
        self.habit_freq_one_day.refresh_from_db()
        self.habit_freq_random.refresh_from_db()
    
    #Tests for getDisabledDaysHabit
    def test_getDisabledDaysHabit_every_day(self):
        result = getDisabledDaysHabit(self.habit_freq_everyday)
        expectedResult = []
        self.assertEqual(result, expectedResult)
    
    def test_getDisabledDaysHabit_every_other_day(self):
        result = getDisabledDaysHabit(self.habit_freq_every_other_day)
        expectedResult = [2, 4, 6]
        self.assertEqual(result, expectedResult)
    
    def test_getDisabledDaysHabit_random(self):
        result = getDisabledDaysHabit(self.habit_freq_random)
        expectedResult = [1, 3, 4, 5]
        self.assertEqual(result, expectedResult)

    def test_getDisabledDaysHabit_invalid_habit_argument(self):
        self.assertRaises(TypeError, getDisabledDaysHabit, "habit")
    
    #Tests for getDailyHabits
    def test_getDailyHabits_after_all_creationDates(self):
        day = datetime.date(2020,9,7)
        result = getDailyHabits(day, self.user)
        expectedResult = [self.habit_freq_everyday,
            self.habit_freq_every_other_day]
        self.assertEqual(result, expectedResult)
    
    def test_getDailyHabits_before_creationDates(self):
        habitStreak = HabitStreak.objects.create(
            habit=self.habit_freq_everyday,
            startDate=datetime.date(2020,7,1),
            endDate=datetime.date(2020,7,10),
            frequency=self.habit_freq_everyday.frequency()
        )
        day = datetime.date(2020,7,6)
        result = getDailyHabits(day, self.user)
        expectedResult = [self.habit_freq_everyday]
        self.assertEqual(result, expectedResult)

    def test_getDailyHabits_invalid_date_argument(self):
        self.assertRaises(TypeError, getDailyHabits, "date", self.user)
    
    def test_getDailyHabits_invalid_user_argument(self):
        self.assertRaises(TypeError, getDailyHabits, datetime.date.today(), "user")
    
    #Tests for getYearStreak
    def test_getYearStreak_no_streaks(self):
        result = getYearStreak(self.habit_freq_everyday, 2020)
        self.assertEqual(result, [])
    
    def test_getYearStreak(self):
        habitStreak = HabitStreak.objects.create(
            habit=self.habit_freq_everyday,
            startDate=datetime.date(2020,9,2),
            endDate=datetime.date(2020,9,5),
            frequency=self.habit_freq_everyday.frequency()
        )
        result = getYearStreak(self.habit_freq_everyday, 2020)
        expectedResult = [
            datetime.date(2020,9,2),
            datetime.date(2020,9,3),
            datetime.date(2020,9,4),
            datetime.date(2020,9,5)
            ]
        self.assertEqual(result, expectedResult)
    
    def test_getYearStreak_streak_starts_prev_year(self):
        habitStreak = HabitStreak.objects.create(
            habit=self.habit_freq_everyday,
            startDate=datetime.date(2019,12,30),
            endDate=datetime.date(2020,1,2),
            frequency=self.habit_freq_everyday.frequency()
        )
        result = getYearStreak(self.habit_freq_everyday, 2020)
        expectedResult = [
            datetime.date(2020,1,1),
            datetime.date(2020,1,2),
        ]
        self.assertEqual(result, expectedResult)
    
    def test_getYearStreak_streak_ends_next_year(self):
        habitStreak = HabitStreak.objects.create(
            habit=self.habit_freq_everyday,
            startDate=datetime.date(2020,12,30),
            endDate=datetime.date(2021,1,2),
            frequency=self.habit_freq_everyday.frequency()
        )
        result = getYearStreak(self.habit_freq_everyday, 2020)
        expectedResult = [
            datetime.date(2020,12,30),
            datetime.date(2020,12,31),
        ]
        self.assertEqual(result, expectedResult)

    def test_getYearStreak_streak_starts_prev_year_full_streak_in_other_year(self):
        habitStreak1 = HabitStreak.objects.create(
            habit=self.habit_freq_everyday,
            startDate=datetime.date(2019,9,2),
            endDate=datetime.date(2019,9,5),
            frequency=self.habit_freq_everyday.frequency()
        )
        habitStreak2 = HabitStreak.objects.create(
            habit=self.habit_freq_everyday,
            startDate=datetime.date(2019,12,25),
            endDate=datetime.date(2020,1,2),
            frequency=self.habit_freq_everyday.frequency()
        )
        result = getYearStreak(self.habit_freq_everyday, 2020)
        expectedResult = [
            datetime.date(2020,1,1),
            datetime.date(2020,1,2),
        ]
        self.assertEqual(result, expectedResult)

    def test_getYearStreak_invalid_habit_argument(self):
        self.assertRaises(TypeError, getYearStreak, "habit", 2020)
    
    def test_getYearStreak_invalid_year_argument(self):
        self.assertRaises(ValueError, getYearStreak, self.habit_freq_everyday, "year")