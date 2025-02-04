from tkinter import *
from tkinter import ttk, messagebox
from tkinter import PhotoImage
from PIL import Image, ImageTk
import sqlite3
from datetime import datetime, timedelta, date
from create_db import create_db
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
from ttkbootstrap.widgets import DateEntry
from tkinter import StringVar


class New_Customer:
    def __init__(self, root):
        self.root=root
        self.root.geometry("1280x720+50+50")
        self.root.title("Add New Customer")
        self.root.focus_force()


        create_db()

        # Create a Title
        new_customer_title = ttkb.Label(self.root, text="Add New Customer", font=("Helvetica", 20, "bold"), bootstyle="primary inverse", anchor=CENTER)
        new_customer_title.place(relx=0.5, y=0, anchor="n", relwidth=1, height=50)

        #Entry Variables
        self.var_full_name = StringVar()
        self.var_mobile_number = StringVar()
        self.var_address = StringVar()
        self.var_mediator_name = StringVar()
        self.var_loan_amount = StringVar()
        self.var_loan_interest_rate=StringVar() 
        self.var_interest_amount = StringVar()
        self.var_total_given_amount = StringVar()
        self.var_daily_collection_amount = StringVar()
        

        #Entry Fields
        style=ttkb.Style()
        style.configure('TLabel', font=("Helvetica", 15, "bold"), background="#2c3e50", foreground="white")
        lbl_label_title = ttkb.Label(self.root, text="Enter All The Details of the Customer Below", style='TLabel', justify=CENTER, anchor=CENTER)
        lbl_label_title.place(x=0, y=70, relwidth=1, height=35)
       
        style.configure('primary.TLabel', font=("Helvetica", 15, "bold"), foreground="white")
        style.configure('custom.TEntry', selectbackground='lightyellow', selectborderwidth=5, font=("Helvetica", 15, "bold"))
        lbl_full_name = ttkb.Label(self.root, text="1. Full Name of Customer:-", style='primary.TLabel')
        lbl_full_name.place(x=95, y=120)
        entry_full_name = ttkb.Entry(self.root, text="", textvariable=self.var_full_name, style='custom.TEntry')
        entry_full_name.place(x=525, y=120, width=600)

        lbl_mobile_number = ttkb.Label(self.root, text="2. Mobile Number of Customer:-", style='primary.TLabel')
        lbl_mobile_number.place(x=95, y=160)
        entry_mobile_number = ttkb.Entry(self.root, text="", textvariable=self.var_mobile_number, style='custom.TEntry')
        entry_mobile_number.place(x=525, y=160, width=600)

        lbl_address = ttkb.Label(self.root, text="3. Address of Customer:-", style='primary.TLabel')
        lbl_address.place(x=95, y=200)
        entry_address = ttkb.Entry(self.root, text="", textvariable=self.var_address, style='custom.TEntry')
        entry_address.place(x=525, y=200, width=600)

        lbl_mediator_name = ttkb.Label(self.root, text="4. Name of Mediator:-", style='primary.TLabel')
        lbl_mediator_name.place(x=95, y=240)
        entry_mediator_name = ttkb.Entry(self.root, text="", textvariable=self.var_mediator_name, style='custom.TEntry')
        entry_mediator_name.place(x=525, y=240, width=600)

        lbl_loan_amount = ttkb.Label(self.root, text="5. Loan Amount:-", style='primary.TLabel')
        lbl_loan_amount.place(x=95, y=280)
        entry_loan_amount = ttkb.Entry(self.root, text="", textvariable=self.var_loan_amount, style='custom.TEntry')
        entry_loan_amount.place(x=525, y=280, width=600)
        entry_loan_amount.bind("<KeyRelease>", self.calculate_interest)

        lbl_loan_interest_rate = ttkb.Label(self.root, text="6. Loan Interest Rate:-", style='primary.TLabel')
        lbl_loan_interest_rate.place(x=95, y=320)
        entry_loan_interest_rate = ttkb.Entry(self.root, text="", textvariable=self.var_loan_interest_rate, style='custom.TEntry')
        entry_loan_interest_rate.place(x=525, y=320, width=600)
        entry_loan_interest_rate.bind("<KeyRelease>", self.calculate_interest)

        lbl_interest_amount = ttkb.Label(self.root, text="6. Interest Amount:-", style='primary.TLabel')
        lbl_interest_amount.place(x=95, y=360)
        entry_interest_amount = ttkb.Entry(self.root, text="", textvariable=self.var_interest_amount, style='custom.TEntry')
        entry_interest_amount.place(x=525, y=360, width=600)

        lbl_total_given_amount = ttkb.Label(self.root, text="7. Total Given Amount:-", style='primary.TLabel')
        lbl_total_given_amount.place(x=95, y=400)
        entry_total_given_amount = ttkb.Entry(self.root, text="", textvariable=self.var_total_given_amount, style='custom.TEntry')
        entry_total_given_amount.place(x=525, y=400, width=600)

        lbl_daily_collection_amount = ttkb.Label(self.root, text="8. Daily Collection Amount:-", style='primary.TLabel')
        lbl_daily_collection_amount.place(x=95, y=440)
        entry_daily_collection = ttkb.Entry(self.root, text="", textvariable=self.var_daily_collection_amount, style='custom.TEntry')
        entry_daily_collection.place(x=525, y=440, width=600)

        lbl_start_date = ttkb.Label(self.root, text="9. Start Date:-", style='primary.TLabel')
        lbl_start_date.place(x=95, y=480)
        
        
        # Inside your __init__ method
        # self.var_start_date = StringVar()

        # Create the DateEntry widget
        self.entry_start_date = DateEntry(self.root, bootstyle='primary')

        # Place the DateEntry widget
        self.entry_start_date.place(x=525, y=480, width=600)  


        #Buttons
        style.configure("TButton", font=("Helvetica", 14, "bold"))
        new_customer_submit_button = ttkb.Button(self.root, text="Submit", style="info.TButton", cursor="hand2", command=self.validate_entries)
        new_customer_submit_button.place(x=525, y=540, width=175)

        clear_all_button = ttkb.Button(self.root, text="Clear All", style="warning.TButton", cursor="hand2", command=self.clear_data)
        clear_all_button.place(x=735, y=540, width=175)

        back_home_button = ttkb.Button(self.root, text="Back / Home", style="danger.TButton", cursor="hand2", command=self.root.destroy)
        back_home_button.place(x=950, y=540, width=175)


        # Footer
        footer = ttkb.Label(self.root, text="Saraswati Bachat Gat\nDesign by: Shrenik", font=("Helvetica", 12, "bold"), justify="center", bootstyle="primary inverse", anchor=CENTER)
        footer.place(anchor="s", relwidth=1, height=60, relx=0.5, rely=1)

#===============Functions=================================


    # Calculate Interest Amount
    def calculate_interest(self, event=None):
        try:
            loan_amount=float(self.var_loan_amount.get())
            interest_rate = float(self.var_loan_interest_rate.get())
            interest_amount=((loan_amount * interest_rate)/100)*3
            self.var_interest_amount.set(f"{interest_amount:.2f}")
            self.var_total_given_amount.set(loan_amount - interest_amount)
            self.var_daily_collection_amount.set(loan_amount/100)
        except ValueError:
            # Handle the case where the input is not a number 
            self.var_interest_amount.set("0.00")


    # Valiadate All the Entries
    def validate_entries(self): 
        entries = { 
            "Full Name": self.var_full_name.get(), 
            "Mobile Number": self.var_mobile_number.get(), 
            "Address": self.var_address.get(), 
            "Mediator Name": self.var_mediator_name.get(), 
            "Loan Amount": self.var_loan_amount.get(), 
            "Interest Rate": self.var_loan_interest_rate.get(), 
            "Total Given Amount": self.var_total_given_amount.get(), 
            "Daily Collection Amount": self.var_daily_collection_amount.get(), 
            } 
        for field_name, value in entries.items(): 
            if not value.strip(): 
                messagebox.showerror("Input Error", f"Please enter {field_name}.") 
                return
        self.add_new_customer()


    # Create New Customer
    def add_new_customer(self):
        full_name=self.var_full_name.get()
        mobile_number=self.var_mobile_number.get()
        address=self.var_address.get()
        mediator_name=self.var_mediator_name.get()
        loan_amount=float(self.var_loan_amount.get())
        interest_rate=float(self.var_loan_interest_rate.get())
        interest_amount=float(self.var_interest_amount.get())
        total_given_amount=float(self.var_total_given_amount.get())
        daily_collection_amount=float(self.var_daily_collection_amount.get())
        start_date = self.entry_start_date.entry.get()
        




        # Calculate the end date (100 days after the start date)
        start_date_obj = datetime.strptime((start_date), "%d-%m-%Y")
        end_date_obj = start_date_obj + timedelta(days=99)
        end_date = end_date_obj.strftime("%d-%m-%Y")

        con=sqlite3.connect("loan_database.db")
        cur=con.cursor()
        cur.execute("insert into customer_loan_list (full_name , mobile_number, address, mediator_name, loan_amount, interest_rate, interest_amount, total_given_amount, term, daily_collection_amount, start_date, end_date, status) values(?,?,?,?,?,?,?,?,?,?,?,?,?)", (full_name, mobile_number, address, mediator_name, loan_amount, interest_rate, interest_amount, total_given_amount, 100, daily_collection_amount, start_date, end_date, "ongoing")) #100 Days Term
        con.commit()
        acc_no=cur.lastrowid
        con.close()
        self.clear_data()
        messagebox.showinfo("Success", f"New Customer Created on Date: {start_date}")
        self.create_dynamic_table(acc_no, start_date)


    # Function to create a dynamic table for each customer
    def create_dynamic_table(self, acc_no, start_date):
        table_name = f"customer_{acc_no}"
        con = sqlite3.connect("loan_database.db")
        cur = con.cursor()
        
        cur.execute(f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                day_no INTEGER,
                date TEXT,
                daily_collection_amount REAL,
                cumulative_total REAL,
                entered_date TEXT,
                PRIMARY KEY(day_no)
            )
        """)
        
        # Populate the table with 100 rows
        start_date_obj = datetime.strptime(start_date, "%d-%m-%Y")
        cumulative_total = 0
        
        for day_no in range(1, 101):
            date = start_date_obj + timedelta(days=day_no - 1)
            date_str = date.strftime("%d-%m-%Y")
            daily_collection_amount = 0  # Initial amount is 0
            cumulative_total += daily_collection_amount  # Cumulative total initially 0
            entered_date=None

            cur.execute(f"INSERT INTO {table_name} (day_no, date, daily_collection_amount, cumulative_total, entered_date) VALUES (?, ?, ?, ?,?)",
                        (day_no, date_str, daily_collection_amount, cumulative_total, entered_date))
        
        con.commit()
        con.close()
        

   
    # Clear Data
    def clear_data(self):
        self.var_full_name.set("")
        self.var_mobile_number.set("")
        self.var_address.set("")
        self.var_mediator_name.set("")
        self.var_loan_amount.set("")
        self.var_loan_interest_rate.set("") 
        self.var_interest_amount.set("")
        self.var_total_given_amount.set("")
        self.var_daily_collection_amount.set("")


    


if __name__ == "__main__":
    root=ttkb.Window(themename="darkly")
    object=New_Customer(root)
    root.mainloop()