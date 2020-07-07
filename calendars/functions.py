from .exceptions import InvalidMonthNumber

def getPreviousMonth(year, month):
    if month > 1 and month <= 12:
        month = month - 1
    elif month == 1:
        month = 12
        year = year - 1
    else:
        raise InvalidMonthNumber("{:d} isn't a valid month!".format(month))
    
    return {'year': year, 'month': month}

def getNextMonth(year, month):
    if month >= 1 and month < 12:
        month = month + 1
    elif month == 12:
        month = 1
        year = year + 1
    else:
        raise InvalidMonthNumber("{:d} isn't a valid month!".format(month))
    
    return {'year': year, 'month': month}
