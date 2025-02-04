from tkinter import *
from tkinter import ttk
from tkinter import PhotoImage
from PIL import Image, ImageTk
from datetime import datetime, timedelta
import sqlite3
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
from new_customer import New_Customer
from existing_customer import Existing_Customer
from date_list import date_list
from statement import statement


class Dashboard:
    def __init__(self, root):
        self.root=root
        self.root.geometry("1280x720+0+0")
        self.root.title("Saraswati Bachat Gat")

        
        # Create a Title
        style=ttkb.Style()
        dashboard_title = ttkb.Label(self.root, text="Saraswati Bachat Gat", font=("Helvetica", 30, "bold"),bootstyle="primary inverse", anchor=CENTER)
        dashboard_title.place(x=0,y=0,relwidth=1, height=100)
        style.configure('primary.TLabel', foreground="white")
        menu_title=ttkb.Label(self.root, text="Menus", font=("Helvetica", 20, "bold"),style="primary.TLabel", anchor=CENTER)
        menu_title.place(x=590, y=120)
        
        #Create Menu Frame
        
        style.configure('Custom.TFrame', borderwidth=5,  bordercolor="lightgray", relief="solid", background="#1a0840")
        menu_frame = ttkb.Frame(self.root, style='Custom.TFrame')
        menu_frame.place(x=220,y=170, width=840, height=200)

        # Create buttons
        style.configure("TButton", font=("Helvetica", 12))
        existing_customer_button = ttkb.Button(menu_frame, text="Existing Customer", style='info.TButton', cursor="hand2", command=self.existing_customer)
        existing_customer_button.place(x=150, y=20, width=250, height=40)

        new_customer_button = ttkb.Button(menu_frame, text="New Customer", style='success.TButton', cursor="hand2", command=self.add_new_customer)
        new_customer_button.place(x=450, y=20, width=250, height=40)

        due_dates_button = ttkb.Button(menu_frame, text="Due Dates", style='warning.TButton', cursor="hand2", command=self.date_list)
        due_dates_button.place(x=150, y=75, width=250, height=40)

        show_all_statement_button = ttkb.Button(menu_frame, text="Show All Statement", style='success.TButton', cursor="hand2", command=self.statement)
        show_all_statement_button.place(x=450, y=75, width=250, height=40)

        close_app_button = ttkb.Button(menu_frame, text="Close App", style='danger.TButton', cursor="hand2", command=self.root.destroy)
        close_app_button.place(x=300, y=130, width=250, height=40)

        # Create labels for daily collection, and active customers

        self.today_collection_text = StringVar()
        self.today_collection_text.set("Today's Daily Collection:\n[₹0]")

        self.active_customers_text = StringVar()
        self.active_customers_text.set("Total Number of Active Customers:\n[₹0]")

        style.configure("Custom.TLabel", font=("Helvetica", 12, "bold"), background="#1a0840", borderwidth=10, bordercolor="lightgray", relief="ridge", foreground="#DAF7A6")
        today_collection_label = ttkb.Label(self.root, textvariable=self.today_collection_text, style="Custom.TLabel", justify=CENTER, anchor=CENTER)
        today_collection_label.place(x=220, y=400, width=330, height=150)
        
        active_customers_label = ttkb.Label(self.root, textvariable=self.active_customers_text, style="Custom.TLabel", justify=CENTER, anchor=CENTER)
        active_customers_label.place(x=570, y=400, width=490, height=150)


        # Footer
        footer = ttkb.Label(self.root, text="Saraswati Bachat Gat\nDesign by: Shrenik", font=("Helvetica", 12, "bold"), justify="center", bootstyle="primary inverse", anchor=CENTER)
        footer.place(anchor="s", relwidth=1, height=60, relx=0.5, rely=1)

    def add_new_customer(self):
        self.new_customer_window = Toplevel(self.root)
        self.new_object = New_Customer(self.new_customer_window)
        self.new_customer_window.grab_set()  # Ensures input focus remains on this window
        self.new_customer_window.wait_window()  # Waits for this window to close
        self.update_dashboard_labels()

    def existing_customer(self):
        self.existing_customer_window = Toplevel(self.root)
        self.existing_customer_object = Existing_Customer(self.existing_customer_window)
        self.existing_customer_window.grab_set()
        self.existing_customer_window.wait_window()
        self.update_dashboard_labels() 


    def date_list(self):
        self.date_list_window = Toplevel(self.root)
        self.date_list_object = date_list(self.date_list_window)
        self.date_list_window.grab_set()
        self.date_list_window.wait_window()
        self.update_dashboard_labels()

    def statement(self):
        self.statement_window = Toplevel(self.root)
        self.statement_object = statement(self.statement_window)
        self.statement_window.grab_set()  
        self.statement_window.wait_window()
        self.update_dashboard_labels()

    def update_dashboard_labels(self):
        try:
            con = sqlite3.connect("loan_database.db")
            cur = con.cursor()

            # Today's date
            today = datetime.today().strftime("%d-%m-%Y")

            # Fetch only dynamic customer tables
            cur.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name LIKE 'customer_%' AND name NOT IN ('customer_loan_list')
            """)
            customer_tables = cur.fetchall()

            total_collection = 0
            for table in customer_tables:
                table_name = table[0]
                try:
                    cur.execute(f"""
                        SELECT SUM(daily_collection_amount) FROM {table_name} WHERE entered_date = ?
                    """, (today,))
                    result = cur.fetchone()
                    if result and result[0]:
                        total_collection += result[0]
                except sqlite3.OperationalError:
                    continue

            # Active customers
            cur.execute("""
                SELECT COUNT(*) FROM customer_loan_list WHERE status = 'ongoing'
            """)
            active_customers_count = cur.fetchone()[0]

            # Update dashboard labels
            self.today_collection_text.set(f"Today's Daily Collection:\n[₹{total_collection:.2f}]")
            self.active_customers_text.set(f"Total Number of Active Customers:\n[{active_customers_count}]")

        except Exception as ex:
            print(f"Error updating dashboard labels: {str(ex)}")
        finally:
            con.close()



if __name__ == "__main__":
    root=ttkb.Window(themename="darkly")
    object=Dashboard(root)
    object.update_dashboard_labels()
    root.mainloop()