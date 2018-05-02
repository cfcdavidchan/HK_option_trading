# Import all the necessary library
import QuantLib as ql
import datetime

calendar = ql.HongKong() #presetting as Hong Kong market


# Change the date (day, month, year) into QuantLib
def ql_date_formate(day, month, year):
    return ql.Date(day, month, year) #input in (int formate

# Check whether the date is a business in Hong Kong 
def business_day_checker(date):
#    calendar = ql.HongKong()
    return calendar.isBusinessDay(date)

# find the nearest trading day
## note that the HKEX will not provide current day data
last_businessday = ql.Date_todaysDate() -1
while not business_day_checker(last_businessday):
    last_businessday = calendar.advance(last_businessday, ql.Period(-1, ql.Days))


# Convert Quantlib date formate into string formate
def date_to_string(date):
    datetime_formate = datetime.datetime(date.year(), date.month(), date.dayOfMonth())
    return datetime_formate.strftime("%y%m%d")

def business_day_start_end_list(start_date, end_date = None, formate = 'ql'):
    # start_date and end_date formate dd mm yyyy
    if end_date == None:
        end_date = last_businessday
    else:
        end_date = ql_date_formate(int(end_date.split(' ')[0]), int(end_date.split(' ')[1]), int(end_date.split(' ')[2]))
        
    # the date after last trading day is not allow  
    if end_date > last_businessday:
        print ('Sorry, the end date cannot be further than', last_businessday)
        return
    
    if not business_day_checker(end_date): # if the end day is not a business day then loop backward         
        print ('Sorry, end date:  ', end_date, 'is not a business day')
        while not business_day_checker(end_date):
               end_date = calendar.advance(end_date, ql.Period(-1, ql.Days))
        print ('End date will change to ', end_date)
    
    # convert start date as ql formate
    start_date = ql_date_formate(int(start_date.split(' ')[0]), int(start_date.split(' ')[1]), int(start_date.split(' ')[2]))
    
    if not business_day_checker(start_date): # if the start date is not a business day then loop backward         
        print ('Sorry, start date:  ', start_date, 'is not a business day')
        while not business_day_checker(start_date):
               start_date = calendar.advance(start_date, ql.Period(-1, ql.Days))
        print ('Start date will change to ', start_date)
    
    
    
    
    start_end_list = list()
    
    # formate  # if no input, will save as ql
    
    if formate == 'str':
        start_end_list.append(date_to_string(end_date))
    else:
        start_end_list.append(end_date)
    
    while True:
        min_period = ql.Period(-1, ql.Days)
        end_date = calendar.advance(end_date, min_period)
        
        if end_date < start_date:
            break
        
        if formate == 'str':
            start_end_list.append(date_to_string(end_date))
        else:
            start_end_list.append(end_date)
    
    print ('start date: ', start_date, 'end date: ', end_date, 'number of preiod: ', len(start_end_list))
    
    return start_end_list
    
# Creating a list of business day.
    # First input is the target period (days)
    # Second input is the start_day of the period, presetted as today
        # Note that the start_day means the last day of the whole target period because the function is counting backward
    # Third input is the date formate inside the list, it can be in Quantlib date formate ('ql') or string ('str') formate.
    
def business_day_period_list(period, end_date = last_businessday, formate = 'ql'):
    period_list = list()
    
    if end_date > last_businessday:
        print ('Sorry, the end day cannot be further than', last_businessday)
        return
    
    if formate == 'str':
        period_list.append(date_to_string(end_date))
    else:
        period_list.append(end_date)
        
    for i in range(1, period):
        min_period = ql.Period(-i, ql.Days)
        date = calendar.advance(end_date, min_period)
        
        if formate == 'str':
            date = date_to_string(date)
        period_list.append(date)
    
    return period_list