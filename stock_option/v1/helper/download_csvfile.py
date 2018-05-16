from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen
from helper.businessday_check import *
import os


def csv_directory_creater():
    # create a csv directory in the root folder
    if 'csv_file' not in os.listdir():
        print ('csv_file folder is created in ', os.getwd())
        os.mkdir('csv_file')


def option_data_csv(date = None, path= None):
    # if date is None, it will download the last trading day's data
    if date == None:
        date = date_to_string(last_tradingday())
    
    if path == None: # if the path is not specific, it will download to the csv_file directory in the root directory
        csv_directory_creater()
        path = os.getcwd() + '/csv_file/'
        
    hkex_url = 'https://www.hkex.com.hk/eng/stat/dmstat/dayrpt/dqe'
    #  date shoudl be yymmdd
    csv_zip = urlopen(hkex_url + date + '.zip')
    csv_zip = ZipFile(BytesIO(csv_zip.read()))
        
    csv_zip.extractall(path)
    
    original_filename = csv_zip.infolist()[0].filename
    new_filename = csv_zip.infolist()[0].filename.replace('dqe','')
    
    os.rename(path+original_filename, path+new_filename)
    return   new_filename
    

if __name__ == "__main__":
    os.chdir('../')
    day = ql.Date_todaysDate() -1
    
    # Finding the last business day (excluding current date)
    while True:
        if business_day_checker(day):
            last_businessday = day
            break
        else:
            day -= 1
    
    print ('The updated data is on', last_businessday)
    
    # Asking the start date
    while True:
        start_date_question = "Enter the last trading day of data you want (dd mm yyyy). (Default = %s)"% str(last_businessday)
        ddmmyyyy = input(start_date_question)
        if ddmmyyyy is '':
            start_day = last_businessday
            break
        try:
            dd, mm, yyyy = ddmmyyyy.split(" ")
            select_day = ql_date_formate(int(dd), int(mm), int(yyyy))
            if select_day < last_businessday:
                if not business_day_checker(select_day):
                    print (select_day, 'is not a business_day')
                    while not business_day_checker(select_day):
                        select_day -=1
                    print ('The program will change it to', select_day, 'as the starting day')
                start_day = select_day
                
                
                break
            else:
                print ("The date cannot be later than the updated date")
                
        except:
            print ('input error')
            continue

    # Asking the period
    while True:
        try:
            preiod = int(input("Period(days)"))
        except ValueError:
            print ('input error')
            continue
        else:
            break
    
    date_list = business_day_period_list(preiod, start_day= start_day, formate= 'str')
    
    for date in date_list:
        try:
            option_data_csv(date= date)
        except:
            print (date, 'option data is not available to download')