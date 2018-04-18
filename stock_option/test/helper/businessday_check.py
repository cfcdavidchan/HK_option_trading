# Import all the necessary library
import QuantLib as ql
import datetime

calendar = ql.HongKong() #presetting as Hong Kong market

# Change the date (day, month, year) into QuantLib
def ql_date_formate(day, month, year):
    return ql.Date(day, month, year)

# Check whether the date is a business in Hong Kong 
def business_day_checker(date):
#    calendar = ql.HongKong()
    return calendar.isBusinessDay(date)

# Convert Quantlib date formate into string formate
def date_to_string(date):
    datetime_formate = datetime.datetime(date.year(), date.month(), date.dayOfMonth())
    return datetime_formate.strftime("%y%m%d")

# Creating a list of business day.
    # First input is the target period (days)
    # Second input is the start_day of the period, presetted as today
        # Note that the start_day means the last day of the whole target period because the function is counting backward
    # Third input is the date formate inside the list, it can be in Quantlib date formate ('ql') or string ('str') formate.
    
def business_day_period_list(period, start_day = ql.Date_todaysDate(), formate = 'ql'):
    period_list = list()
    
    if formate == 'str':
        period_list.append(date_to_string(start_day))
    else:
        period_list.append(start_day)
        
    for i in range(1, period):
        min_period = ql.Period(-i, ql.Days)
        date = calendar.advance(start_day, min_period)
        
        if formate == 'str':
            date = date_to_string(date)
        period_list.append(date)
    
    return period_list