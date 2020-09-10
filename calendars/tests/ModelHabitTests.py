from django.test import TestCase
from calendars.models import Habit, HabitStreak, Reward, RewardStreak
from django.contrib.auth.models import User
import datetime

class TestHabit(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username="test", password="test")

        cls.habit_freq_everyday = Habit.objects.create(
            name="testHabit1", 
            creator=cls.user, 
            creationDate=datetime.date(2020,8,1),
            monday=True, tuesday=True, wednesday=True,
            thursday=True, friday=True, saturday=True,
            sunday=True
        )
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
    
    def setUp(self):
        self.user.refresh_from_db()
        self.habit_freq_everyday.refresh_from_db()
        self.habit_freq_every_other_day.refresh_from_db()
        self.habit_freq_one_day.refresh_from_db()
        self.habit_freq_random.refresh_from_db()
    
    #Test frequency
    def test_frequency_every_day(self):
        result = self.habit_freq_everyday.frequency()
        expectedResult = "Every day"
        self.assertEqual(result, expectedResult)
    
    def test_frequency_every_other_day(self):
        result = self.habit_freq_every_other_day.frequency()
        expectedResult = "Mon, Wed, Fri, Sun"
        self.assertEqual(result, expectedResult)

    def test_frequency_one_day(self):
        result = self.habit_freq_one_day.frequency()
        expectedResult = "Wed"
        self.assertEqual(result, expectedResult)
    
    def test_frequency_random(self):
        result = self.habit_freq_random.frequency()
        expectedResult = "Tues, Sat, Sun"
        self.assertEqual(result, expectedResult)
    
    #Test frequencyToArray
    def test_frequencyToArray_every_day(self):
        result = self.habit_freq_everyday.frequencyToArray()
        expectedResult = [1,1,1,1,1,1,1]
        self.assertEqual(result, expectedResult)
    
    def test_frequencyToArray_every_other_day(self):
        result = self.habit_freq_every_other_day.frequencyToArray()
        expectedResult = [1,0,1,0,1,0,1]
        self.assertEqual(result, expectedResult)

    def test_frequencyToArray_one_day(self):
        result = self.habit_freq_one_day.frequencyToArray()
        expectedResult = [0,0,1,0,0,0,0]
        self.assertEqual(result, expectedResult)
    
    def test_frequencyToArray_random(self):
        result = self.habit_freq_random.frequencyToArray()
        expectedResult = [0,1,0,0,0,1,1]
        self.assertEqual(result, expectedResult)

    #Tests for isInFrequency
    def test_isInFrequency(self):
        dateArgument = datetime.date(2020,9,5)
        self.assertTrue(self.habit_freq_everyday.isInFrequency(dateArgument))
    
    def test_isInFrequency_not_in_freq(self):
        dateArgument = datetime.date(2020,9,5)
        self.assertFalse(self.habit_freq_every_other_day.isInFrequency(dateArgument))
    
    def test_isInFrequency_invalid_date_argument(self):
        self.assertRaises(TypeError, self.habit_freq_everyday.isInFrequency, "date")

    #Tests for completedToday
    def test_completedToday_completed_middle_of_streak(self):
        habitStreak = HabitStreak.objects.create(
            habit=self.habit_freq_everyday,
            startDate=datetime.date(2020,9,1),
            endDate=datetime.date(2020,9,10),
            frequency=self.habit_freq_everyday.frequency()
        )
        dateArgument = datetime.date(2020,9,6)
        self.assertTrue(self.habit_freq_everyday.completedToday(dateArgument))
    
    def test_completedToday_completed_end_of_streak(self):
        habitStreak = HabitStreak.objects.create(
            habit=self.habit_freq_everyday,
            startDate=datetime.date(2020,9,1),
            endDate=datetime.date(2020,9,10),
            frequency=self.habit_freq_everyday.frequency()
        )
        dateArgument = datetime.date(2020,9,10)
        self.assertTrue(self.habit_freq_everyday.completedToday(dateArgument))
    
    def test_completedToday_completed_beginning_of_streak(self):
        habitStreak = HabitStreak.objects.create(
            habit=self.habit_freq_everyday,
            startDate=datetime.date(2020,9,1),
            endDate=datetime.date(2020,9,10),
            frequency=self.habit_freq_everyday.frequency()
        )
        dateArgument = datetime.date(2020,9,1)
        self.assertTrue(self.habit_freq_everyday.completedToday(dateArgument))
    
    def test_completedToday_completed_different_streak_freq(self):
        habitStreak = HabitStreak.objects.create(
            habit=self.habit_freq_everyday,
            startDate=datetime.date(2020,9,2),
            endDate=datetime.date(2020,9,9),
            frequency=self.habit_freq_every_other_day.frequency()
        )
        dateArgument = datetime.date(2020,9,4)
        self.assertTrue(self.habit_freq_everyday.completedToday(dateArgument))
    
    def test_completedToday_not_completed_after_streak(self):
        habitStreak = HabitStreak.objects.create(
            habit=self.habit_freq_everyday,
            startDate=datetime.date(2020,9,1),
            endDate=datetime.date(2020,9,10),
            frequency=self.habit_freq_everyday.frequency()
        )
        dateArgument = datetime.date(2020,9,11)
        self.assertFalse(self.habit_freq_everyday.completedToday(dateArgument))
    
    def test_completedToday_not_completed_before_streak(self):
        habitStreak = HabitStreak.objects.create(
            habit=self.habit_freq_everyday,
            startDate=datetime.date(2020,9,1),
            endDate=datetime.date(2020,9,10),
            frequency=self.habit_freq_everyday.frequency()
        )
        dateArgument = datetime.date(2020,8,31)
        self.assertFalse(self.habit_freq_everyday.completedToday(dateArgument))
    
    def test_completedToday_not_completed_in_different_streak_freq(self):
        habitStreak = HabitStreak.objects.create(
            habit=self.habit_freq_everyday,
            startDate=datetime.date(2020,9,2),
            endDate=datetime.date(2020,9,9),
            frequency=self.habit_freq_every_other_day.frequency()
        )
        dateArgument = datetime.date(2020,9,5)
        self.assertFalse(self.habit_freq_everyday.completedToday(dateArgument))
    
    def test_completedToday_no_streak_exists(self):
        dateArgument = datetime.date(2020,9,5)
        self.assertFalse(self.habit_freq_everyday.completedToday(dateArgument))
    
    def test_completedToday_only_streaks_for_other_habits(self):
        habitStreak = HabitStreak.objects.create(
            habit=self.habit_freq_every_other_day,
            startDate=datetime.date(2020,9,2),
            endDate=datetime.date(2020,9,9),
            frequency=self.habit_freq_every_other_day.frequency()
        )
        dateArgument = datetime.date(2020,9,4)
        self.assertFalse(self.habit_freq_everyday.completedToday(dateArgument))
    
    def test_completedToday_one_day_streak(self):
        habitStreak = HabitStreak.objects.create(
            habit=self.habit_freq_everyday,
            startDate=datetime.date(2020,9,2),
            endDate=datetime.date(2020,9,2),
            frequency=self.habit_freq_everyday.frequency()
        )
        dateArgument = datetime.date(2020,9,2)
        self.assertTrue(self.habit_freq_everyday.completedToday(dateArgument))
    
    def test_completedToday_date_in_between_streaks(self):
        habitStreak1 = HabitStreak.objects.create(
            habit=self.habit_freq_everyday,
            startDate=datetime.date(2020,9,2),
            endDate=datetime.date(2020,9,2),
            frequency=self.habit_freq_everyday.frequency()
        )
        habitStreak2 = HabitStreak.objects.create(
            habit=self.habit_freq_everyday,
            startDate=datetime.date(2020,9,5),
            endDate=datetime.date(2020,9,10),
            frequency=self.habit_freq_everyday.frequency()
        )
        dateArgument = datetime.date(2020,9,4)
        self.assertFalse(self.habit_freq_everyday.completedToday(dateArgument))
    
    def test_completedToday_completed_multiple_streaks(self):
        habitStreak1 = HabitStreak.objects.create(
            habit=self.habit_freq_everyday,
            startDate=datetime.date(2020,9,2),
            endDate=datetime.date(2020,9,2),
            frequency=self.habit_freq_everyday.frequency()
        )
        habitStreak2 = HabitStreak.objects.create(
            habit=self.habit_freq_everyday,
            startDate=datetime.date(2020,9,5),
            endDate=datetime.date(2020,9,10),
            frequency=self.habit_freq_everyday.frequency()
        )
        dateArgument = datetime.date(2020,9,6)
        self.assertTrue(self.habit_freq_everyday.completedToday(dateArgument))

    def test_completedToday_invalid_date_argument(self):
        self.assertRaises(TypeError, self.habit_freq_everyday.completedToday, "date")
    
    #Tests for startRewardOver
    def test_startRewardOver_one_reward_with_open_rewardstreak(self):
        reward = Reward.objects.create(
            creationDate=datetime.date(2020,8,3),
            habit=self.habit_freq_everyday,
            days=5
        )
        rewardStreak = RewardStreak.objects.create(
            reward=reward,
            startDate=datetime.date(2020,9,3),
            counter=2
        )
        dateArgument = datetime.date(2020,9,6)
        self.habit_freq_everyday.startRewardOver(dateArgument)
        self.assertEqual(reward.getRewardStreak().counter, 1)
        self.assertEqual(reward.getRewardStreak().startDate, dateArgument)
    
    def test_startRewardOver_one_reward_with_unlocked_rewardstreak(self):
        reward = Reward.objects.create(
            creationDate=datetime.date(2020,8,3),
            habit=self.habit_freq_everyday,
            days=5
        )
        rewardStreak = RewardStreak.objects.create(
            reward=reward,
            startDate=datetime.date(2020,9,1),
            counter=5,
            unlocked=True,
            unlockDate=datetime.date(2020,9,6)
        )
        dateArgument = datetime.date(2020,9,6)
        self.assertFalse(reward.openRewardStreakExists())
        self.habit_freq_everyday.startRewardOver(dateArgument)
        self.assertTrue(reward.openRewardStreakExists())
        newRewardStreak = reward.getRewardStreak()
        self.assertEqual(newRewardStreak.counter, 1)
        self.assertEqual(newRewardStreak.startDate, dateArgument)

    def test_startRewardOver_one_reward_no_rewardstreak(self):
        reward = Reward.objects.create(
            creationDate=datetime.date(2020,8,3),
            habit=self.habit_freq_everyday,
            days=5
        )
        dateArgument = datetime.date(2020,9,6)
        self.assertFalse(reward.openRewardStreakExists())
        self.habit_freq_everyday.startRewardOver(dateArgument)
        self.assertTrue(reward.openRewardStreakExists())
        newRewardStreak = reward.getRewardStreak()
        self.assertEqual(newRewardStreak.counter, 1)
        self.assertEqual(newRewardStreak.startDate, dateArgument)
    
    def test_startRewardOver_invalid_date_argument(self):
        self.assertRaises(TypeError, self.habit_freq_everyday.startRewardOver, "date")
    
    #Tests for upRewardCounter
    def test_upRewardCounter_one_reward_with_open_rewardstreak(self):
        reward = Reward.objects.create(
            creationDate=datetime.date(2020,8,3),
            habit=self.habit_freq_everyday,
            days=5
        )
        rewardStreak = RewardStreak.objects.create(
            reward=reward,
            startDate=datetime.date(2020,9,3),
            counter=2
        )
        dateArgument = datetime.date(2020,9,6)
        self.habit_freq_everyday.upRewardCounter(dateArgument)
        self.assertEqual(reward.getRewardStreak().counter, 3)
    
    def test_upRewardCounter_one_reward_with_unlocked_rewardstreak(self):
        reward = Reward.objects.create(
            creationDate=datetime.date(2020,8,3),
            habit=self.habit_freq_everyday,
            days=5
        )
        rewardStreak = RewardStreak.objects.create(
            reward=reward,
            startDate=datetime.date(2020,9,1),
            counter=5,
            unlocked=True,
            unlockDate=datetime.date(2020,9,6)
        )
        dateArgument = datetime.date(2020,9,6)
        self.assertFalse(reward.openRewardStreakExists())
        self.habit_freq_everyday.upRewardCounter(dateArgument)
        self.assertTrue(reward.openRewardStreakExists())
        newRewardStreak = reward.getRewardStreak()
        self.assertEqual(newRewardStreak.counter, 1)
        self.assertEqual(newRewardStreak.startDate, dateArgument)

    def test_upRewardCounter_one_reward_no_rewardstreak(self):
        reward = Reward.objects.create(
            creationDate=datetime.date(2020,8,3),
            habit=self.habit_freq_everyday,
            days=5
        )
        dateArgument = datetime.date(2020,9,6)
        self.assertFalse(reward.openRewardStreakExists())
        self.habit_freq_everyday.upRewardCounter(dateArgument)
        self.assertTrue(reward.openRewardStreakExists())
        newRewardStreak = reward.getRewardStreak()
        self.assertEqual(newRewardStreak.counter, 1)
        self.assertEqual(newRewardStreak.startDate, dateArgument)
    
    def test_upRewardCounter_invalid_date_argument(self):
        self.assertRaises(TypeError, self.habit_freq_everyday.upRewardCounter, "date")
    
    #Tests for lowerRewardCounter
    def test_lowerRewardCounter_one_reward_with_open_rewardstreak(self):
        reward = Reward.objects.create(
            creationDate=datetime.date(2020,8,3),
            habit=self.habit_freq_everyday,
            days=5
        )
        rewardStreak = RewardStreak.objects.create(
            reward=reward,
            startDate=datetime.date(2020,9,3),
            counter=3
        )
        dateArgument = datetime.date(2020,9,6)
        self.habit_freq_everyday.lowerRewardCounter(dateArgument)
        self.assertEqual(reward.getRewardStreak().counter, 2)
    
    def test_lowerRewardCounter_one_reward_with_not_unlocked_today_rewardstreak(self):
        reward = Reward.objects.create(
            creationDate=datetime.date(2020,8,3),
            habit=self.habit_freq_everyday,
            days=5
        )
        rewardStreak = RewardStreak.objects.create(
            reward=reward,
            startDate=datetime.date(2020,8,31),
            counter=5,
            unlocked=True,
            unlockDate=datetime.date(2020,9,5)
        )
        dateArgument = datetime.date(2020,9,6)
        self.assertFalse(reward.openRewardStreakExists())
        self.habit_freq_everyday.lowerRewardCounter(dateArgument)
        self.assertFalse(reward.openRewardStreakExists())
    
    def test_lowerRewardCounter_one_reward_with_unlocked_today_rewardstreak(self):
        reward = Reward.objects.create(
            creationDate=datetime.date(2020,8,3),
            habit=self.habit_freq_everyday,
            days=5
        )
        rewardStreak = RewardStreak.objects.create(
            reward=reward,
            startDate=datetime.date(2020,9,11),
            counter=5,
            unlocked=True,
            unlockDate=datetime.date(2020,9,6)
        )
        dateArgument = datetime.date(2020,9,6)
        self.assertFalse(reward.openRewardStreakExists())
        self.habit_freq_everyday.lowerRewardCounter(dateArgument)
        self.assertTrue(reward.openRewardStreakExists())
        newRewardStreak = reward.getRewardStreak()
        self.assertEqual(newRewardStreak.counter, 4)

    def test_lowerRewardCounter_one_reward_no_rewardstreak(self):
        reward = Reward.objects.create(
            creationDate=datetime.date(2020,8,3),
            habit=self.habit_freq_everyday,
            days=5
        )
        dateArgument = datetime.date(2020,9,6)
        self.assertFalse(reward.openRewardStreakExists())
        self.habit_freq_everyday.lowerRewardCounter(dateArgument)
        self.assertFalse(reward.openRewardStreakExists())
    
    def test_lowerRewardCounter_invalid_date_argument(self):
        self.assertRaises(TypeError, self.habit_freq_everyday.lowerRewardCounter, "date")
    
    #Tests for makeNewStreak
    def test_makeNewStreak_no_streaks(self):
        self.assertFalse(self.habit_freq_everyday.getStreaks())
        dateArgument = datetime.date(2020,9,5)
        self.habit_freq_everyday.makeNewStreak(dateArgument)
        streak = self.habit_freq_everyday.getStreaks()[0]
        self.assertEqual(streak.habit, self.habit_freq_everyday)
        self.assertEqual(streak.startDate, dateArgument)
        self.assertEqual(streak.endDate, dateArgument)
        self.assertEqual(streak.frequency, self.habit_freq_everyday.frequency())
    
    def test_makeNewStreak_invalid_date_argument(self):
        self.assertRaises(TypeError, self.habit_freq_everyday.makeNewStreak, "date")
    
    #Tests for toggleCompleteToday
    def test_toggleCompleteToday_not_completed_streak_exists(self):
        habitStreak = HabitStreak.objects.create(
            habit=self.habit_freq_everyday,
            startDate=datetime.date(2020,8,20),
            endDate=datetime.date(2020,9,5),
            frequency=self.habit_freq_everyday.frequency()
        )
        streaksBefore = len(self.habit_freq_everyday.getStreaks())
        dateArgument = datetime.date(2020, 9, 6)
        self.habit_freq_everyday.toggleCompleteToday(dateArgument)
        streak = self.habit_freq_everyday.getStreaks()[0]
        streaksAfter = len(self.habit_freq_everyday.getStreaks())
        self.assertEqual(streak.endDate, dateArgument)
        self.assertEqual(streaksBefore, streaksAfter)

    def test_toggleCompleteToday_not_completed_no_streak(self):
        streaksBefore = len(self.habit_freq_everyday.getStreaks())
        self.assertEqual(streaksBefore, 0)
        dateArgument = datetime.date(2020, 9, 6)
        self.habit_freq_everyday.toggleCompleteToday(dateArgument)
        streak = self.habit_freq_everyday.getStreaks()[0]
        streaksAfter = len(self.habit_freq_everyday.getStreaks())
        self.assertEqual(streak.endDate, dateArgument)
        self.assertEqual(streaksAfter, 1)
    
    def test_toggleCompleteToday_not_completed_diff_freq(self):
        habitStreak = HabitStreak.objects.create(
            habit=self.habit_freq_everyday,
            startDate=datetime.date(2020,8,19),
            endDate=datetime.date(2020,9,4),
            frequency=self.habit_freq_every_other_day.frequency()
        )
        streaksBefore = len(self.habit_freq_everyday.getStreaks())
        self.assertEqual(streaksBefore, 1)
        dateArgument = datetime.date(2020, 9, 5)
        self.habit_freq_everyday.toggleCompleteToday(dateArgument)
        streak = self.habit_freq_everyday.getStreaks()[1]
        streaksAfter = len(self.habit_freq_everyday.getStreaks())
        self.assertEqual(streak.frequency, self.habit_freq_everyday.frequency())
        self.assertEqual(streak.endDate, dateArgument)
        self.assertEqual(streaksAfter, 2)

    def test_toggleCompleteToday_completed_long_streak(self):
        habitStreak = HabitStreak.objects.create(
            habit=self.habit_freq_every_other_day,
            startDate=datetime.date(2020,9,2),
            endDate=datetime.date(2020,9,6),
            frequency=self.habit_freq_every_other_day.frequency()
        )
        dateArgument = datetime.date(2020, 9, 6)
        self.habit_freq_every_other_day.toggleCompleteToday(dateArgument)
        streak = self.habit_freq_every_other_day.getStreaks()[0]
        self.assertEqual(streak.endDate, datetime.date(2020, 9, 4))
    
    def test_toggleCompleteToday_completed_one_day_streak(self):
        habitStreak = HabitStreak.objects.create(
            habit=self.habit_freq_every_other_day,
            startDate=datetime.date(2020,9,6),
            endDate=datetime.date(2020,9,6),
            frequency=self.habit_freq_every_other_day.frequency()
        )
        dateArgument = datetime.date(2020, 9, 6)
        self.habit_freq_every_other_day.toggleCompleteToday(dateArgument)
        self.assertFalse(self.habit_freq_every_other_day.getStreaks())

    def test_toggleCompleteToday_invalid_date_argument(self):
        self.assertRaises(TypeError, self.habit_freq_everyday.toggleCompleteToday, "date")

    #Tests for completeEarlierDays
    def test_completeEarlierDays_insert_standalone_date(self):
        self.assertFalse(self.habit_freq_everyday.getStreaks())
        dateArgument = "1/9/2020"
        self.habit_freq_everyday.completeEarlierDays(dateArgument)
        newStreak = self.habit_freq_everyday.getStreaks()[0]
        self.assertEqual(len(self.habit_freq_everyday.getStreaks()), 1)
        self.assertEqual(newStreak.startDate, newStreak.endDate)

    def test_completeEarlierDays_insert_date_at_end_streak(self):
        habitStreak = HabitStreak.objects.create(
            habit=self.habit_freq_everyday,
            startDate=datetime.date(2020,9,2),
            endDate=datetime.date(2020,9,3),
            frequency=self.habit_freq_everyday.frequency()
        )
        oldStreaks = len(self.habit_freq_everyday.getStreaks())
        dateArgument = "4/9/2020"
        self.habit_freq_everyday.completeEarlierDays(dateArgument)
        newStreaks = len(self.habit_freq_everyday.getStreaks())
        streak = self.habit_freq_everyday.getStreaks()[0]
        self.assertEqual(newStreaks, oldStreaks)
        self.assertEqual(streak.endDate, datetime.date(2020,9,4))
    
    def test_completeEarlierDays_insert_date_at_beginning_streak(self):
        habitStreak = HabitStreak.objects.create(
            habit=self.habit_freq_everyday,
            startDate=datetime.date(2020,9,2),
            endDate=datetime.date(2020,9,3),
            frequency=self.habit_freq_everyday.frequency()
        )
        oldStreaks = len(self.habit_freq_everyday.getStreaks())
        dateArgument = "1/9/2020"
        self.habit_freq_everyday.completeEarlierDays(dateArgument)
        newStreaks = len(self.habit_freq_everyday.getStreaks())
        streak = self.habit_freq_everyday.getStreaks()[0]
        self.assertEqual(newStreaks, oldStreaks)
        self.assertEqual(streak.startDate, datetime.date(2020,9,1))
    
    def test_completeEarlierDays_insert_today(self):
        today = datetime.date.today()
        delta = datetime.timedelta(days=1)
        habitStreak = HabitStreak.objects.create(
            habit=self.habit_freq_everyday,
            startDate=datetime.date(2020,9,2),
            endDate=today-delta,
            frequency=self.habit_freq_everyday.frequency()
        )
        oldStreaks = len(self.habit_freq_everyday.getStreaks())
        dateArgument = "{}/{}/{}".format(today.day, today.month, today.year)
        self.habit_freq_everyday.completeEarlierDays(dateArgument)
        newStreaks = len(self.habit_freq_everyday.getStreaks())
        streak = self.habit_freq_everyday.getStreaks()[0]
        self.assertEqual(newStreaks, oldStreaks)
        self.assertEqual(streak.endDate, today)

    def test_completeEarlierDays_insert_future_date(self):
        today = datetime.date.today()
        delta = datetime.timedelta(days=10)
        futureDate = today + delta
        dateArgument = "{}/{}/{}".format(
            futureDate.day, 
            futureDate.month, 
            futureDate.year
        )
        self.assertFalse(self.habit_freq_everyday.getStreaks())
        self.habit_freq_everyday.completeEarlierDays(dateArgument)
        self.assertFalse(self.habit_freq_everyday.getStreaks())
    
    def test_completeEarlierDays_insert_diff_freq(self):
        habitStreak = HabitStreak.objects.create(
            habit=self.habit_freq_everyday,
            startDate=datetime.date(2020,9,2),
            endDate=datetime.date(2020,9,6),
            frequency=self.habit_freq_every_other_day.frequency()
        )
        oldStreaks = len(self.habit_freq_everyday.getStreaks())
        dateArgument = "7/9/2020"
        self.habit_freq_everyday.completeEarlierDays(dateArgument)
        newStreaks = len(self.habit_freq_everyday.getStreaks())
        streak = self.habit_freq_everyday.getStreaks()[1]
        self.assertNotEqual(newStreaks, oldStreaks)
        self.assertEqual(streak.startDate, streak.endDate)
        self.assertEqual(streak.endDate, datetime.date(2020,9,7))
    
    def test_completeEarlierDays_insert_already_completed_date(self):
        habitStreak = HabitStreak.objects.create(
            habit=self.habit_freq_everyday,
            startDate=datetime.date(2020,9,2),
            endDate=datetime.date(2020,9,10),
            frequency=self.habit_freq_everyday.frequency()
        )
        oldStreaks = len(self.habit_freq_everyday.getStreaks())
        dateArgument = "5/9/2020"
        self.habit_freq_everyday.completeEarlierDays(dateArgument)
        newStreaks = len(self.habit_freq_everyday.getStreaks())
        streak = self.habit_freq_everyday.getStreaks()[0]
        self.assertEqual(newStreaks, oldStreaks)
        self.assertNotEqual(streak.startDate, datetime.date(2020,9,5))
        self.assertNotEqual(streak.endDate, datetime.date(2020,9,5))

    def test_completeEarlierDays_insert_date_between_two_streaks(self):
        habitStreak1 = HabitStreak.objects.create(
            habit=self.habit_freq_everyday,
            startDate=datetime.date(2020,9,2),
            endDate=datetime.date(2020,9,3),
            frequency=self.habit_freq_everyday.frequency()
        )
        habitStreak2 = HabitStreak.objects.create(
            habit=self.habit_freq_everyday,
            startDate=datetime.date(2020,9,5),
            endDate=datetime.date(2020,9,10),
            frequency=self.habit_freq_everyday.frequency()
        )
        oldStreaks = len(self.habit_freq_everyday.getStreaks())
        dateArgument = "4/9/2020"
        self.habit_freq_everyday.completeEarlierDays(dateArgument)
        newStreaks = len(self.habit_freq_everyday.getStreaks())
        streak = self.habit_freq_everyday.getStreaks()[0]
        self.assertNotEqual(newStreaks, oldStreaks)
        self.assertEqual(newStreaks, 1)
        self.assertEqual(streak.startDate, datetime.date(2020,9,2))
        self.assertEqual(streak.endDate, datetime.date(2020,9,10))
    
    def test_completeEarlierDays_two_dates_make_one_streak_from_two(self):
        habitStreak1 = HabitStreak.objects.create(
            habit=self.habit_freq_everyday,
            startDate=datetime.date(2020,9,2),
            endDate=datetime.date(2020,9,3),
            frequency=self.habit_freq_everyday.frequency()
        )
        habitStreak2 = HabitStreak.objects.create(
            habit=self.habit_freq_everyday,
            startDate=datetime.date(2020,9,6),
            endDate=datetime.date(2020,9,10),
            frequency=self.habit_freq_everyday.frequency()
        )
        oldStreaks = len(self.habit_freq_everyday.getStreaks())
        dateArgument = "5/9/2020,4/9/2020"
        self.habit_freq_everyday.completeEarlierDays(dateArgument)
        newStreaks = len(self.habit_freq_everyday.getStreaks())
        streak = self.habit_freq_everyday.getStreaks()[0]
        self.assertNotEqual(newStreaks, oldStreaks)
        self.assertEqual(newStreaks, 1)
        self.assertEqual(streak.startDate, datetime.date(2020,9,2))
        self.assertEqual(streak.endDate, datetime.date(2020,9,10))
    
    def test_completeEarlierDays_insert_multiple_dates(self):
        habitStreak1 = HabitStreak.objects.create(
            habit=self.habit_freq_everyday,
            startDate=datetime.date(2020,9,2),
            endDate=datetime.date(2020,9,3),
            frequency=self.habit_freq_everyday.frequency()
        )
        habitStreak2 = HabitStreak.objects.create(
            habit=self.habit_freq_everyday,
            startDate=datetime.date(2020,9,6),
            endDate=datetime.date(2020,9,10),
            frequency=self.habit_freq_everyday.frequency()
        )
        oldStreaks = len(self.habit_freq_everyday.getStreaks())
        dateArgument = "1/9/2020,20/8/2020,5/9/2020,4/9/2020"
        self.habit_freq_everyday.completeEarlierDays(dateArgument)
        newStreaks = len(self.habit_freq_everyday.getStreaks())
        streak1 = self.habit_freq_everyday.getStreaks()[0]
        streak2 = self.habit_freq_everyday.getStreaks()[1]
        self.assertEqual(newStreaks, oldStreaks)
        self.assertEqual(streak1.startDate, datetime.date(2020,9,1))
        self.assertEqual(streak1.endDate, datetime.date(2020,9,10))
        self.assertEqual(streak2.startDate, datetime.date(2020,8,20))
        self.assertEqual(streak2.endDate, datetime.date(2020,8,20))

    def test_completeEarlierDays_invalid_dateArr_argument(self):
        self.assertRaises(IndexError, self.habit_freq_everyday.completeEarlierDays, "testest")
    
    def test_completeEarlierDays_invalid_dateArg_argument(self):
        self.assertRaises(ValueError, self.habit_freq_everyday.completeEarlierDays, "a/b/c")
    
    # This is actually raised earlier when attempting to make a datetime.date object and
    # throws a ValueError: day is out of range for month
    # it's caught in the form itself when it attempts to add the dates
    # def test_completeEarlierDays_invalid_dateArg_argument2(self):
    #     self.assertRaises(TypeError, self.habit_freq_everyday.completeEarlierDays, "34/9/1")

    #Tests for getYearStreaks
    def test_getYearStreaks_no_streaks(self):
        result = self.habit_freq_everyday.getYearStreaks(2020)
        self.assertFalse(result)
    
    def test_getYearStreaks(self):
        habitStreak = HabitStreak.objects.create(
            habit=self.habit_freq_everyday,
            startDate=datetime.date(2020,9,2),
            endDate=datetime.date(2020,9,5),
            frequency=self.habit_freq_everyday.frequency()
        )
        result = list(self.habit_freq_everyday.getYearStreaks(2020))
        expectedResult = [habitStreak]
        self.assertEqual(result, expectedResult)
    
    def test_getYearStreaks_streak_starts_prev_year(self):
        habitStreak = HabitStreak.objects.create(
            habit=self.habit_freq_everyday,
            startDate=datetime.date(2019,9,2),
            endDate=datetime.date(2020,9,5),
            frequency=self.habit_freq_everyday.frequency()
        )
        result = list(self.habit_freq_everyday.getYearStreaks(2020))
        expectedResult = [habitStreak]
        self.assertEqual(result, expectedResult)
    
    def test_getYearStreaks_streak_ends_next_year(self):
        habitStreak = HabitStreak.objects.create(
            habit=self.habit_freq_everyday,
            startDate=datetime.date(2020,9,2),
            endDate=datetime.date(2021,9,5),
            frequency=self.habit_freq_everyday.frequency()
        )
        result = list(self.habit_freq_everyday.getYearStreaks(2020))
        expectedResult = [habitStreak]
        self.assertEqual(result, expectedResult)

    def test_getYearStreaks_streak_starts_prev_year_full_streak_in_other_year(self):
        habitStreak1 = HabitStreak.objects.create(
            habit=self.habit_freq_everyday,
            startDate=datetime.date(2019,9,2),
            endDate=datetime.date(2019,9,5),
            frequency=self.habit_freq_everyday.frequency()
        )
        habitStreak2 = HabitStreak.objects.create(
            habit=self.habit_freq_everyday,
            startDate=datetime.date(2019,12,2),
            endDate=datetime.date(2020,1,10),
            frequency=self.habit_freq_everyday.frequency()
        )
        result = list(self.habit_freq_everyday.getYearStreaks(2020))
        expectedResult = [habitStreak2]
        self.assertEqual(result, expectedResult)
