from django.test import TestCase
from calendars.models import Habit, Reward, RewardStreak
from django.contrib.auth.models import User
import datetime

class TestRewardStreak(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username="test", password="test")
        cls.habit = Habit.objects.create(
            name="testHabit1", 
            creator=cls.user, 
            creationDate=datetime.date(2020,8,1),
            monday=True, tuesday=True, wednesday=True,
            thursday=True, friday=True, saturday=True,
            sunday=True
        )
        cls.habit_freq_every_other_day = Habit.objects.create(
            name="testHabit1", 
            creator=cls.user, 
            creationDate=datetime.date(2020,8,1),
            monday=True, tuesday=False, wednesday=True,
            thursday=False, friday=True, saturday=False,
            sunday=True
        )

        cls.reward = Reward.objects.create(
            creationDate=datetime.date(2020,8,1),
            habit=cls.habit,
            days=5
        )
        cls.reward_freq_every_other_day = Reward.objects.create(
            creationDate=datetime.date(2020,8,1),
            habit=cls.habit_freq_every_other_day,
            days=5
        )

        cls.rewardStreak_counter0 = RewardStreak.objects.create(
            reward=cls.reward,
            startDate=datetime.date(2020,8,25)
        )
        cls.rewardStreak_counter1 = RewardStreak.objects.create(
            reward=cls.reward,
            startDate=datetime.date(2020,8,25),
            counter=1
        )
        cls.rewardStreak_counter4 = RewardStreak.objects.create(
            reward=cls.reward,
            startDate=datetime.date(2020,8,25),
            counter=4
        )
        cls.rewardStreak_unlocked = RewardStreak.objects.create(
            reward=cls.reward,
            startDate=datetime.date(2020,8,25),
            unlocked=True,
            counter=5,
            unlockDate=datetime.date(2020,8,30)
        )
        cls.rewardStreak_freq_every_other_day = RewardStreak.objects.create(
            reward=cls.reward_freq_every_other_day,
            startDate=datetime.date(2020,8,26),
            counter=1
        )
    
    def setUp(self):
        self.user.refresh_from_db()
        self.habit.refresh_from_db()
        self.habit_freq_every_other_day.refresh_from_db()
        self.reward.refresh_from_db()
        self.reward_freq_every_other_day.refresh_from_db()
        self.rewardStreak_counter0.refresh_from_db()
        self.rewardStreak_counter1.refresh_from_db()
        self.rewardStreak_counter4.refresh_from_db()
        self.rewardStreak_unlocked.refresh_from_db()
        self.rewardStreak_freq_every_other_day.refresh_from_db()
    
    #Tests for startOver
    def test_startOver(self):
        dateArgument = datetime.date(2020,9,5)
        self.rewardStreak_counter1.startOver(dateArgument)
        self.assertEquals(self.rewardStreak_counter1.startDate, dateArgument)
        self.assertEquals(self.rewardStreak_counter1.counter, 0)
    
    def test_startOver_date_before_startDate(self):
        dateArgument = datetime.date(2020,8,20)
        oldStreak = self.rewardStreak_counter1
        self.rewardStreak_counter1.startOver(dateArgument)
        self.assertEquals(self.rewardStreak_counter1, oldStreak)
    
    def test_startOver_date_not_in_freq(self):
        dateArgument = datetime.date(2020,9,1)
        oldStreak = self.rewardStreak_freq_every_other_day
        self.rewardStreak_freq_every_other_day.startOver(dateArgument)
        self.assertEquals(self.rewardStreak_freq_every_other_day, oldStreak)
    
    def test_startOver_invalid_date_argument(self):
        self.assertRaises(TypeError, self.rewardStreak_counter1.startOver, "date")

    #Test upCounter
    def test_upCounter(self):
        self.rewardStreak_counter1.upCounter()
        self.assertEquals(self.rewardStreak_counter1.counter, 2)
    
    def test_upCounter_unlock_reward(self):
        self.rewardStreak_counter4.upCounter()
        self.assertEquals(self.rewardStreak_counter4.counter, 5)
        self.assertTrue(self.rewardStreak_counter4.unlocked)
        self.assertEquals(self.rewardStreak_counter4.unlockDate, datetime.date.today())

    def test_upCounter_already_unlocked(self):
        oldData = self.rewardStreak_unlocked
        self.rewardStreak_unlocked.upCounter()
        self.assertEquals(self.rewardStreak_unlocked, oldData)
    
    #Test lowerCounter
    def test_lowerCounter(self):
        self.rewardStreak_counter1.lowerCounter()
        self.assertEquals(self.rewardStreak_counter1.counter, 0)
    
    def test_lowerCounter_counter0(self):
        oldData = self.rewardStreak_counter0
        self.rewardStreak_counter0.lowerCounter()
        self.assertEquals(self.rewardStreak_counter0, oldData)
    
    def test_lowerCounter_unlocked(self):
        self.rewardStreak_unlocked.lowerCounter()
        self.assertEquals(self.rewardStreak_unlocked.counter, 4)
        self.assertFalse(self.rewardStreak_unlocked.unlocked)
        self.assertEquals(self.rewardStreak_unlocked.unlockDate, None)