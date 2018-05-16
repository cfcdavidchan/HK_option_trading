from helper.download_csvfile import *
from helper.businessday_check import *
from helper.reading_HKEX_option_data import option_data_mining
import tkinter as tk
from tkinter.messagebox import showinfo, showerror
import os, shutil, json

### creating all the necessary directories ###
if 'csv_tmp' not in os.listdir():
    os.mkdir('csv_tmp')

if 'csv_stock' not in os.listdir():
    os.mkdir('csv_stock')

### finding the updated trading day
last_businessday = last_tradingday()
last_businessday_str = datetime.datetime(last_businessday.year(), last_businessday.month(), last_businessday.dayOfMonth()).strftime("%d %m %Y")

### runnuing tkinter ###
class App:
    def __init__(self,windows):
        # creating the frame
        #self.windows = windows
        self.update_button() #update automatically when the program starts

        # Clean button frame
        self.frame_clean = tk.Frame(windows, width=500, height=100)
        self.frame_clean.grid(row=0, column=0, sticky='w')
        self.init_clean(self.frame_clean)

        # Update button frame
        self.frame_update = tk.Frame(windows, width=500, height=100)
        self.frame_update.grid(row=0, column=0, sticky='e')
        self.init_update(self.frame_update)

        # Separate frame
        self.frame_separate = tk.Frame(windows, height=15)
        self.frame_separate.grid(row=1, column=0, sticky='nw')

        # Entry frame
        self.frame_entry = tk.Frame(windows, width=50, height=100)
        self.frame_entry.grid(row=2, column=0, sticky='w')
        self.init_entry(self.frame_entry)

        # stock selection frame
        self.frame_stock_selection = tk.Frame(windows, width=50, height=100)
        self.frame_stock_selection.grid(row=3, column=0, sticky='w')
        self.init_stock_selection_button(self.frame_stock_selection)

        # stock entry frame
        self.init_frame_stock_entry = tk.Frame(windows)



    def init_clean(self,frame):
        ## Update button
        self.clean_button = tk.Button(frame, text= "Clean", fg="black", font=12, activeforeground='green', command= self.clean_button) #update_button
        self.clean_button.grid(row=0, column=0, sticky='e')


    def init_update(self,frame):

        ## Update button
        self.update_button = tk.Button(frame, text= "Update", fg="black", font=12, activeforeground='green', command= self.update_button) #update_button
        self.update_button.grid(row=0, column=50, sticky='e')


#         ## separate Frame
#         self.separate_frame = tk.Label(self.frame, borderwidth=5, width=50, height=5)
#         self.separate_frame.grid(row=0, column=0, columnspan=10, rowspan=5)



    def init_entry(self,frame):
                            ### User entry ###
        frame.grid_columnconfigure(7)
        #creating the label for End date input
        self.end_date_label = tk.Label(frame, text='End Date:', font='large_font')
        self.end_date_label.grid(row=5, column=1, sticky='w')
        # End date entry
        self.end_date_textvariable = tk.StringVar(frame, value=last_businessday_str)
        self.end_date_entry = tk.Entry(frame, width=10, textvariable=self.end_date_textvariable, font='large_font')
        self.end_date_entry.grid(row=5, column=2)
        # End date value
        self.end_date_value = tk.Label(frame, text=self.date_str_to_month_name(last_businessday_str))
        self.end_date_value.grid(row=5, column=3, sticky='w')


        # creating the Checkbutton for start date
        self.start_period_Radio = tk.IntVar()
        self.start_period_Radio.set(3)
        # self.start_date_boolean.set(True)
        self.start_date_tick = tk.Radiobutton(frame, variable=self.start_period_Radio, text='Start Date:', font='large_font', value=1, command= self.checkbutton_period_start_date_entry)
        self.start_date_tick.grid(row=6, column=1, sticky='w')

        # Start date entry
        self.start_date_textvariable = tk.StringVar(frame, value='')
        self.start_date_entry = tk.Entry(frame, width=10, textvariable=self.start_date_textvariable, state='disabled', font='large_font')
        self.start_date_entry.grid(row=6, column=2)
        # Start date value
        self.start_date_value = tk.Label(frame, text='            ')
        self.start_date_value.grid(row=6, column=3, sticky='w')

        # creating the Checkbutton for start date
        self.period_tick = tk.Radiobutton(frame, variable=self.start_period_Radio, text='Period:', font='large_font', value=2, command= self.checkbutton_period_start_date_entry)
        self.period_tick.grid(row=7, column=1, sticky='w')

        #creating the frame for Start date input
        # period entry
        self.period_textvariable = tk.IntVar(frame, value='')
        self.period_entry = tk.Entry(frame, width=10, textvariable=self.period_textvariable, state='disabled', font='large_font')
        self.period_entry.grid(row=7, column=2)

        self.updated_date_tick = tk.Radiobutton(frame, variable=self.start_period_Radio, text='Updated date Only', font='large_font', value=3, command= self.checkbutton_period_start_date_entry)
        self.updated_date_tick.grid(row=8, column=1, sticky='w')

        self.start_end_day_label_update()

        ## Download button
        self.download_button = tk.Button(frame, text= "Download", fg="black", font=12, activeforeground='green', command= self.dowload_button) #update_button
        self.download_button.grid(row=8, column=1000, sticky='ne')
        frame.grid_columnconfigure(7, minsize=100)
                                ### User entry End ###


    def init_stock_selection_button(self,frame):
                             ### Stock choosing button Area ###
        self.download_type = tk.StringVar()
        self.options = ["Full", "Stock"]
        self.download_type.set(self.options[0])
        self.drop_list = tk.OptionMenu(frame, self.download_type, *self.options, command= self.drop_list_OptionMenu)
        self.drop_list.configure(width=10)
        self.drop_list.grid(row=1, column=0, sticky='w')

        self.max_column = 4
        self.stock_list = list()


        self.add_stock_button = tk.Button(frame, text= "+", font=12, state = 'disabled', command = self.add_entry_button)
        self.add_stock_button.grid(row=1, column=2)

        # self.print = tk.Button(frame, text= "Print", font=12, command = self.print_stock_list)
        # self.print.grid(row=1, column=4)

        frame.grid_columnconfigure(3, minsize=100)



    ### function area ###

    def checkbutton_period_start_date_entry(self):
        if self.start_period_Radio.get() == 1:
            self.start_date_entry.configure(state ='normal')
            self.period_entry.configure(state = 'disabled')

        if self.start_period_Radio.get() == 2:
            self.start_date_entry.configure(state ='disabled')
            self.period_entry.configure(state = 'normal')

        if self.start_period_Radio.get() == 3:
            self.start_date_entry.configure(state ='disabled')
            self.period_entry.configure(state = 'disabled')

    def date_str_to_month_name(self,date_str):
        try:
            return str(datetime.datetime.strptime(date_str, '%d %m %Y').strftime('%d %b, %Y'))
        except:
            return str('            ')

    def start_end_day_label_update(self):
        self.end_date_value.configure(text = self.date_str_to_month_name(self.end_date_textvariable.get()))
        self.start_date_value.configure(text = self.date_str_to_month_name(self.start_date_textvariable.get()))
        self.start_date_value.after(1000, self.start_end_day_label_update) # repeated the function after 1000millisecond

    def drop_list_OptionMenu(self,*arg): #change the add box
        if self.download_type.get() == self.options[0]: ## full vision
            self.add_stock_button.configure(state='disable')
        elif self.download_type.get() == self.options[1]: ##  Stock vision
            self.add_stock_button.configure(state='normal')

    def add_entry_button(self):
        stock = tk.Entry(self.init_frame_stock_entry)
        self.init_frame_stock_entry.grid(row=4, column=0, sticky='w') # the fram appeard only if the stock_entry function being used
        first_row = 2

        if len(self.stock_list) < self.max_column: # 0 - max_column
            row = first_row
            column = len(self.stock_list)

        elif (len(self.stock_list) % self.max_column == 0):
            row = int(((len(self.stock_list)/ self.max_column)) + first_row)
            column = 0

        else:
            row = int(len(self.stock_list)/ self.max_column) + first_row
            column = len(self.stock_list) % self.max_column

        stock.configure(width = 18)
        stock.grid(row=row, column=column)

        self.stock_list.append(stock)

    def print_stock_list(self):
        stock = list()
        for number, stock_code in enumerate(self.stock_list):
                stock.append(stock_code.get())

        print (stock)

    def clean_button(self):
        if 'csv_tmp' in os.listdir():
            for file in os.listdir('./csv_tmp/'):
                file_path = os.path.join('csv_tmp', file)
                try:
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except:
                    print ('Error')

        if 'csv_stock' in os.listdir():
            for file in os.listdir('./csv_stock/'):
                file_path = os.path.join('csv_stock', file)
                try:
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except:
                    print ('Error')
    def update_button(self):
        if '.update_tmp' not in os.listdir():
            os.mkdir('.update_tmp')

        updated_file = option_data_csv(path='./.update_tmp/')
        updated_csv = option_data_mining(path='.update_tmp/%s' %updated_file)

        json_name = 'option_code.json'

        if json_name in os.listdir():
            os.remove(json_name)

        with open(json_name, 'w') as outfile:
            json.dump(updated_csv.code_dictionary(), outfile)

        if '.update_tmp' in os.listdir():
            shutil.rmtree('.update_tmp')

    def dowload_button(self):
        end_date = self.end_date_textvariable.get()

        ###  creating the period list ###
        if self.start_period_Radio.get() == 1:
            try:
                period_list = business_day_start_end_list(start_date= self.start_date_textvariable.get(), end_date= end_date, formate= 'str')
            except:
                pass
        elif self.start_period_Radio.get() == 2:
            try:
                period_list = business_day_period_list(period= int(self.period_textvariable.get()), end_date= end_date, formate = 'str')
            except:
                pass
        elif self.start_period_Radio.get() == 3:
            try:
                period_list = business_day_period_list(period= 0, end_date= end_date, formate = 'str')
            except:
                pass

        ###

        ### Download in different mode ###
        if self.download_type.get() == self.options[0]: ## full vision
            for date in period_list:
                try:
                    option_data_csv(date= date, path='./csv_tmp/')
                except:
                    print (date, 'option data is not available to download')


        elif self.download_type.get() == self.options[1]: ##  Stock vision
            stock_list = []
            for stock in self.stock_list: ## convert it in 5 digit stock code
                stock_code = stock.get()
                while True:
                    if len(stock_code) == 0:
                        break
                    if len(stock_code) >= 5:
                        stock_list.append(stock_code)
                        break
                    stock_code = '0' + stock_code


            with open('option_code.json') as f: #check whether the stock is in the option list
                stock_code_dict = json.load(f)

            for stock in stock_list:
                if str(stock) not in stock_code_dict.keys():
                    stock_list.remove(stock)
                    showerror('Error', '%s is not in the stock option list' %stock)


            for date in period_list:
                optioncsv_filename = option_data_csv(date= date, path='./csv_tmp/')
                optioncsv = option_data_mining(path='./csv_tmp/%s' %optioncsv_filename)

                for stock in stock_list:

                    ### create sub directory for the stock ###
                    if stock not in os.listdir('./csv_stock'):
                        os.mkdir('./csv_stock/%s' %stock)
                        os.mkdir('./csv_stock/%s/call_table' %stock)
                        os.mkdir('./csv_stock/%s/put_table' %stock)

                    call_table, put_table = optioncsv.call_put_table(stock)

                    call_table.to_csv('./csv_stock/%s/call_table/call_table_%s' %(stock, optioncsv_filename))
                    put_table.to_csv('./csv_stock/%s/put_table/put_table_%s' % (stock, optioncsv_filename))


        showinfo("Report", "Dowload Finish")




windows = tk.Tk()
windows.title("Option data downloader")
#windows.geometry('600x500')
#windows.configure()
windows.resizable(0, 0)
display = App(windows)
windows.mainloop()
