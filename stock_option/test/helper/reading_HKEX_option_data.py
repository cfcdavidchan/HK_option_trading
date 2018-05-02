import pandas as pd
import csv, re

class option_data_mining: 
    def __init__ (self, path):
        self.path = path
        
    def summary(self):
        option_summary = []
        with open(self.path, 'r') as csvfile:
            append = False # checking which part to start saving
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                if 'HKATS CODE' in row:
                    append = True
                if (append) and (not row):
                    break
                if append:
                    option_summary.append(row)

        self.option_summary = pd.DataFrame(option_summary, columns=option_summary.pop(0)) ## convert list to df
        ## Hard Code for editing the header name ##
        header = self.option_summary.columns.values
        header[2] = 'STOCK CODE'
        self.option_summary.columns = header
        ##
        
        return self.option_summary
    
    def code_dictionary(self):
        self.code = {}
        self.option_summary = self.option_summary
        for index, row in self.option_summary.iterrows():
            stock_code = row['STOCK CODE']
            stock_code = re.sub("\D",'',stock_code)
            self.code[stock_code] = {}
            self.code[stock_code]['UNDERLYING STOCK'] = row['UNDERLYING STOCK']
            self.code[stock_code]['HKATS CODE'] = row['HKATS CODE']
        return self.code
    
    def top_10_traded(self):
        top_10 = []
        with open(self.path, 'r') as csvfile:
            append = False # checking which part to start saving
            pointer = 0
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                if 'TOP 10 TRADED (BY VOLUME)' in row:
                    append = True
                    continue
                if append:
                    top_10.append(row)
                    pointer +=1
                if pointer == 11:
                    break
        # convert it to df
        headers = ['Call/Put', 'HKATS CODE','CONTRACT Month',\
                   'STRIKE PRICE','VOLUME','SETTLEMENT PRICE','IV%','HIGH','LOW','OPEN INTEREST','SETTLEMENT PRICE CHANGE','% CHANGE IN SETTLEMENT PRICE']
        top_10 = pd.DataFrame(top_10[1:], columns = headers)
        
        return top_10
    
    def top_5(self,up_down):
        top_5 = []
        keyword = 'TOP 5 ' + up_down
        with open(self.path, 'r') as csvfile:
            append = False # checking which part to start saving
            pointer = 0
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                if not (row): # skip empty line
                    continue
                if keyword in row[0]:
                    append = True
                    continue
                if append:
                    top_5.append(row)
                    pointer +=1
                if pointer == 5:
                    break
        # convert it to df
        headers = ['Call/Put', 'HKATS CODE','CONTRACT Month',\
                   'STRIKE PRICE','VOLUME','SETTLEMENT PRICE','IV%','HIGH','LOW','OPEN INTEREST','SETTLEMENT PRICE CHANGE','% CHANGE IN SETTLEMENT PRICE']
        top_5 = pd.DataFrame(top_5, columns = headers)
        
        return top_5
    
    
    
    def top_5_up(self):
        return self.top_5('UP')
    def top_5_down(self):
        return self.top_5('DOWN')
    
    
    
    def call_put_table(self,stock_code):
        stock = self.code[stock_code]['UNDERLYING STOCK']
        call_table = []
        put_table = []
        with open(self.path, 'r') as csvfile:
            call = False # checking which part to start saving call table
            put = False  # checking which part to start saving put table
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                if not (row):
                    continue
                ## finding call table ##
                if stock in row[0]:
                    call = True #'found'
                    continue
                if (call) and ('TOTAL CALL' in row):
                    call = False 
                    put = True ## starting to find put table
                    continue
                ## finding call table ##
                if (put) and ('TOTAL PUT' in row):
                    break ## end of searching

                if call: #append to call table
                    call_table.append(row)

                if put:  #append to put table
                    put_table.append(row)

        header = ['CONTRACT', 'STRIKE PRICE','CALL/PUT','OPENING PRICE','DAILY HIGH','DAILY LOW','SETTLEMENT PRICE',\
                  'CHANGE IN SETTLEMENT','IV%','VOLUME','OPEN INTEREST','CHANGE IN OI']

        call_table = pd.DataFrame(call_table, columns=header)
        put_table = pd.DataFrame(put_table, columns=header)
        
        return call_table, put_table
                
            