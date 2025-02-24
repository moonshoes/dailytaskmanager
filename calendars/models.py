from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from datetime import date
import datetime

class CalendarEntry(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=150, null=True, blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        abstract = True

class Task(CalendarEntry):
    completed = models.BooleanField(default=False)
    date = models.DateField(auto_now=False, auto_now_add=False)

    class Meta:
        db_table = "task"

    def __str__(self):
        return self.name

    def toggleCompleted(self):
        self.completed = not self.completed
        self.save()

class Event(CalendarEntry):
    location = models.CharField(max_length=100, null=True, blank=True)
    startDate = models.DateTimeField(auto_now=False, auto_now_add=False)
    endDate = models.DateTimeField(auto_now=False, auto_now_add=False)

    def __str__(self):
        return self.name

class Habit(CalendarEntry):
    creationDate = models.DateField(auto_now_add=True)
    monday = models.BooleanField(default=False)
    tuesday = models.BooleanField(default=False)
    wednesday = models.BooleanField(default=False)
    thursday = models.BooleanField(default=False)
    friday = models.BooleanField(default=False)
    saturday = models.BooleanField(default=False)
    sunday = models.BooleanField(default=False)

    iconColor = models.CharField(max_length=7)

    def __str__(self):
        return self.name
    
    def frequency(self):
        frequency = ""

        if (self.monday and self.tuesday and self.wednesday and self.thursday 
            and self.friday and self.saturday and self.sunday):
            frequency = "Every day"
        else:
            if self.monday:
                frequency = frequency + "Mon, "
            if self.tuesday:
                frequency = frequency + "Tues, "
            if self.wednesday:
                frequency = frequency + "Wed, "
            if self.thursday:
                frequency = frequency + "Thurs, "
            if self.friday:
                frequency = frequency + "Fri, "
            if self.saturday:
                frequency = frequency + "Sat, "
            if self.sunday:
                frequency = frequency + "Sun"
            
            lengthF = len(frequency)
            if lengthF != 0 and frequency[lengthF-1] == " ":
                frequency = frequency[:lengthF-2]
            
        return frequency

    def frequencyToArray(self):
        array = []
        for i in range(7):
            array.append(False)

        if self.frequency() == "Every day":
            array[0] = True
            array[1] = True
            array[2] = True
            array[3] = True
            array[4] = True
            array[5] = True
            array[6] = True
        else:
            for day in self.frequency().split(', '):
                if day == 'Mon':
                    array[0] = True
                elif day == 'Tues':
                    array[1] = True
                elif day == 'Wed':
                    array[2] = True
                elif day == 'Thurs':
                    array[3] = True
                elif day == 'Fri':
                    array[4] = True
                elif day == 'Sat':
                    array[5] = True
                elif day == 'Sun':
                    array[6] = True
        return array
    
    def isInFrequency(self, dateArg):
        if not isinstance(dateArg, date):
            raise TypeError("{} is not a date!".format(dateArg))
        frequencyArray = self.frequencyToArray()
        weekDay = dateArg.weekday()
        return frequencyArray[weekDay]
    
    # Streak logic
    def getStreaks(self):
        return HabitStreak.objects.filter(habit=self)
    
    def getYearStreaks(self, year):
        return HabitStreak.objects.filter(
            Q(habit=self),
            Q(startDate__year=year) |
            Q(endDate__year=year)
        )
    
    def completedToday(self, dateArg):
        if not isinstance(dateArg, date):
            raise TypeError("{} is not a date!".format(dateArg))
        streaks = self.getStreaks()
        for streak in streaks:
            if streak.isDateInStreak(dateArg):
                return True
        return False
    
    def toggleCompleteToday(self, dateArg):
        if not isinstance(dateArg, date):
            raise TypeError("{} is not a date!".format(dateArg))
        if self.completedToday(dateArg):
            for streak in self.getStreaks():
                if streak.endDate == dateArg:
                    if streak.startDate != streak.endDate:
                        streak.updateEndDate(streak.previousFrequencyDate(streak.endDate))
                    else:
                        streak.delete()
                    self.lowerRewardCounter(dateArg)
        else:
            found = False
            for streak in self.getStreaks():
                if (streak.frequency == self.frequency()
                    and streak.nextFrequencyDate(streak.endDate) == dateArg):
                    streak.updateEndDate(dateArg)
                    self.upRewardCounter(dateArg)
                    found = True
                    break
            if not found:
                self.makeNewStreak(dateArg)

    def completeEarlierDays(self, dateArr):
        for dateArg in dateArr.split(','):
            dateParam = dateArg.split('/')
            if len(dateParam) != 3:
                raise IndexError("{} is not a valid date!".format(dateArg))
            if (not dateParam[0].isdigit() and
                not dateParam[1].isdigit() and
                not dateParam[2].isdigit()):
                raise ValueError("{} is not a valid date!".format(dateArg))
            dateArg = datetime.date(int(dateParam[2]),
                int(dateParam[1]),
                int(dateParam[0]))
            if not self.completedToday(dateArg) and dateArg <= datetime.date.today():
                found = False
                # Booleans to see if either the end or the start has been updated
                # In most cases these won't be true at the same time, unless a streak is being merged together
                # This ensures we only query the db when we really need to!
                updatedStart = False
                updatedEnd = False
                for streak in self.getStreaks():
                    if (streak.frequency == self.frequency() and
                        (streak.nextFrequencyDate(streak.endDate) == dateArg or
                        streak.previousFrequencyDate(streak.startDate) == dateArg)):
                        found = True
                        if streak.nextFrequencyDate(streak.endDate) == dateArg:
                            streak.updateEndDate(dateArg)
                            updatedEnd = True
                        else:
                            streak.updateStartDate(dateArg)
                            updatedStart = True

                if not found:
                    self.makeNewStreak(dateArg)
                elif updatedStart and updatedEnd:
                    # Two streaks can be merged together
                    earlierStreak = HabitStreak.objects.get(habit=self, endDate=dateArg)
                    laterStreak = HabitStreak.objects.get(habit=self, startDate=dateArg)
                    if earlierStreak.frequency == laterStreak.frequency:
                        earlierStreak.updateEndDate(laterStreak.endDate)
                        laterStreak.delete()
    
    def makeNewStreak(self, dateArg):
        if not isinstance(dateArg, date):
            raise TypeError("{} is not a date!".format(dateArg))
        streakFrequency = self.frequency()
        HabitStreak.objects.create(habit=self, startDate=dateArg, endDate=dateArg, frequency=streakFrequency)
        self.startRewardOver(dateArg)

    # Reward logic
    def getRewards(self):
        return Reward.objects.filter(habit=self)
    
    def startRewardOver(self, dateArg):
        if not isinstance(dateArg, date):
            raise TypeError("{} is not a date!".format(dateArg))
        if self.getRewards():
            for reward in self.getRewards():
                if reward.openRewardStreakExists():
                    rewardStreak = reward.getRewardStreak()
                    rewardStreak.startOver(dateArg)
                    rewardStreak.upCounter()
                else:
                    rewardStreak = RewardStreak.objects.create(reward=reward, startDate=dateArg)
                    rewardStreak.upCounter()

    def upRewardCounter(self, dateArg):
        if not isinstance(dateArg, date):
            raise TypeError("{} is not a date!".format(dateArg))
        if self.getRewards():
            for reward in self.getRewards():
                if reward.openRewardStreakExists():
                    rewardStreak = reward.getRewardStreak()
                    rewardStreak.upCounter()
                else:
                    rewardStreak = RewardStreak.objects.create(reward=reward, startDate=dateArg)
                    rewardStreak.upCounter()

    def lowerRewardCounter(self, dateArg):
        if not isinstance(dateArg, date):
            raise TypeError("{} is not a date!".format(dateArg))
        if self.getRewards():
            for reward in self.getRewards():
                if reward.openRewardStreakExists():
                    rewardStreak = reward.getRewardStreak()
                    rewardStreak.lowerCounter()
                elif reward.unlockedTodayStreakExists(dateArg):
                    rewardStreak = reward.getUnlockedTodayRewards(dateArg)
                    rewardStreak.lowerCounter()
                
  

class HabitStreak(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    startDate = models.DateField()
    endDate = models.DateField()
    frequency = models.CharField(max_length=40)

    def __str__(self):
        return '{} streak: {} until {}'.format(self.habit, self.startDate, self.endDate)

    def updateStartDate(self, newDate):
        if not isinstance(newDate, date):
            raise TypeError("{} is not a date!".format(newDate))
        if self.isInFrequency(newDate) and self.endDate >= newDate:
            self.startDate = newDate
            self.save()

    def updateEndDate(self, newDate):
        if not isinstance(newDate, date):
            raise TypeError("{} is not a date!".format(newDate))
        if self.isInFrequency(newDate) and newDate >= self.startDate:
            self.endDate = newDate
            self.save()
    
    def isDateInStreak(self, dateArg):
        if not isinstance(dateArg, date):
            raise TypeError("{} is not a date!".format(dateArg))
        return (self.isInFrequency(dateArg) and
            dateArg >= self.startDate and
            dateArg <= self.endDate)
    
    def isInFrequency(self, dateArg):
        if not isinstance(dateArg, date):
            raise TypeError("{} is not a date!".format(dateArg))
        frequencyArray = self.frequencyToArray()
        weekDay = dateArg.weekday()
        return frequencyArray[weekDay]

    def frequencyToArray(self):
        array = []
        for i in range(7):
            array.append(False)

        if self.frequency == "Every day":
            array[0] = True
            array[1] = True
            array[2] = True
            array[3] = True
            array[4] = True
            array[5] = True
            array[6] = True
        else:
            for day in self.frequency.split(', '):
                if day == 'Mon':
                    array[0] = True
                elif day == 'Tues':
                    array[1] = True
                elif day == 'Wed':
                    array[2] = True
                elif day == 'Thurs':
                    array[3] = True
                elif day == 'Fri':
                    array[4] = True
                elif day == 'Sat':
                    array[5] = True
                elif day == 'Sun':
                    array[6] = True
        return array

    def nextFrequencyDate(self, dateArg):
        if not isinstance(dateArg, date):
            raise TypeError("{} is not a date!".format(dateArg))
        weekDay = dateArg.weekday()
        found = False
        counter = 0
        array = self.frequencyToArray()

        while not found:
            if weekDay == 6:
                weekDay = 0
            else:
                weekDay = weekDay + 1
            if array[weekDay]:
                found = True
            counter = counter + 1

        delta = datetime.timedelta(days=counter)
        return dateArg + delta

    def previousFrequencyDate(self, dateArg):
        if not isinstance(dateArg, date):
            raise TypeError("{} is not a date!".format(dateArg))
        weekDay = dateArg.weekday()
        found = False
        counter = 0
        array = self.frequencyToArray()

        while not found:
            if weekDay == 0:
                weekDay = 6
            else:
                weekDay = weekDay - 1
            if array[weekDay]:
                found = True
            counter = counter + 1
        
        delta = datetime.timedelta(days=counter)
        return dateArg - delta

class Reward(models.Model):
    creationDate = models.DateField(auto_now_add=True)
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    days = models.IntegerField()

    def __str__(self):
        return 'Reward for {}'.format(self.habit)

    def openRewardStreakExists(self):
        return RewardStreak.objects.filter(reward=self, unlocked=False).exists()
    
    def unlockedTodayStreakExists(self, dateArg):
        return RewardStreak.objects.filter(reward=self, unlocked=True, unlockDate=dateArg).exists()
    
    def getRewardStreak(self):
        return RewardStreak.objects.get(reward=self, unlocked=False)
    
    def getUnlockedRewards(self):
        return RewardStreak.objects.filter(reward=self, unlocked=True)
    
    def getUnlockedTodayRewards(self, dateArg):
        return RewardStreak.objects.get(reward=self, unlocked=True, unlockDate=dateArg)


class RewardStreak(models.Model):
    reward = models.ForeignKey(Reward, on_delete=models.CASCADE)
    startDate = models.DateField()
    unlocked = models.BooleanField(default=False)
    counter = models.IntegerField(default=0)
    unlockDate = models.DateField(null=True, blank=True)

    def __str__(self):
        return '{} started on {}'.format(self.reward, self.startDate)

    def startOver(self, dateArg):
        if not isinstance(dateArg, date):
            raise TypeError("{} is not a date!".format(dateArg))
        if (dateArg >= self.startDate and 
            self.reward.habit.isInFrequency(dateArg)):
            self.startDate = dateArg
            self.counter = 0
            self.save()
    
    def upCounter(self):
        if not self.unlocked:
            self.counter = self.counter + 1
            if self.counter >= self.reward.days:
                self.unlocked = True
                self.unlockDate = datetime.date.today()
            self.save()
    
    def lowerCounter(self):
        if self.counter != 0:
            self.counter = self.counter - 1
            if self.counter < self.reward.days:
                self.unlocked = False
                self.unlockDate = None
            self.save()