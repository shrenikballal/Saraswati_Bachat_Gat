from tkinter import *
from tkinter import ttk, messagebox, font
from tkinter import PhotoImage
from PIL import Image, ImageTk
import sqlite3
from datetime import datetime, timedelta
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *

class statement:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1280x720+50+50")
        self.root.title("Statement")
        self.root.focus_force()


        # Pagination attributes
        self.current_page = 1  # Start with page 1
        self.rows_per_page = 100  # Number of rows per page

        # Create a Title
        statement_title = ttkb.Label(self.root, text="All Statement", font=("Helvetica", 20, "bold"),bootstyle="primary inverse", anchor=CENTER)
        statement_title.place(relx=0.5, y=0, anchor="n", relwidth=1, height=50)

        # Filter Frame
        filter_frame = ttk.Frame(self.root, style="primary.TFrame")
        filter_frame.place(x=10, y=55, width=1260, height=40)

        # Combobox for Status Filter
        filter_label=ttkb.Label(filter_frame, text="Filter by Status:", font=("Helvetica", 14), bootstyle="primary inverse").pack(side=LEFT, padx=10)
        self.status_var = StringVar()
        self.status_combo = ttk.Combobox(filter_frame, textvariable=self.status_var, state="readonly",
                                         values=["All", "Ongoing", "Closed"], font=("Helvetica", 14), width=20, style="info.TCombobox")
        self.status_combo.pack(side=LEFT, padx=10, pady=4)
        self.status_combo.current(0)  # Default to "All"

        # Filter Button
        style = ttkb.Style()
        style.configure("success.TButton", font=("Helvetica", 12), ANCHOR="center")  # Font family, size, and weight

        filter_button= ttkb.Button(filter_frame, text="Apply Filter", style="success.TButton", bootstyle="success", cursor="hand2",
               command=self.filter_table).pack(side=LEFT, padx=10, pady=4)
        

        # Pagination controls
        style = ttkb.Style()
        style.configure("info.TButton", font=("Helvetica", 12), ANCHOR="center")  # Font family, size, and weight
        self.next_button = ttkb.Button(filter_frame, text="Next", style="info.TButton", bootstyle="info", cursor="hand2",
                                   command=self.next_page)
        self.next_button.pack(side=RIGHT, padx=10, pady=4)

        self.page_label = ttkb.Label(filter_frame, text=f"Page: {self.current_page}", font=("Helvetica", 14), bootstyle="primary inverse")
        self.page_label.pack(side=RIGHT, padx=10)

        self.prev_button = ttkb.Button(filter_frame, text="Previous", style="info.TButton", bootstyle="info", cursor="hand2",
                                   command=self.prev_page)
        self.prev_button.pack(side=RIGHT, padx=10, pady=4)



        # Table Frame
        frame = ttkb.Frame(self.root, relief=RIDGE, bootstyle="secondary")
        frame.place(x=10, y=100, width=1260, height=550)

        # Scrollbars
        style.configure('custom.Horizontal.TScrollbar', background='black', troughcolor='white', arrowcolor='white')
        style.configure('custom.Vertical.TScrollbar', background='black', troughcolor='white', arrowcolor='white')
        scrolly = ttkb.Scrollbar(frame, orient=VERTICAL, bootstyle="round", style='custom.Vertical.TScrollbar')
        scrollx = ttkb.Scrollbar(frame, orient=HORIZONTAL, bootstyle="round", style='custom.Horizontal.TScrollbar')

        # Table
        style.configure("Treeview", font=("Helvetica", 12), rowheight=35)
        style.configure("Treeview.Heading", font=("Helvetica", 12), padding=(5, 5), background="#0e59bf")
        self.table = ttk.Treeview(frame, columns=("acc_no", "full_name", "mobile_number", "loan_amount",
                                                  "interest_rate", "interest_amount", "total_given_amount",
                                                  "total_collected_amount", "start_date", "end_date", "status"),
                                  yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.table.xview)
        scrolly.config(command=self.table.yview)

        # Table Headings
        self.table.heading("acc_no", text="Account Number")
        self.table.heading("full_name", text="Customer Name")
        self.table.heading("mobile_number", text="Mobile Number")
        self.table.heading("loan_amount", text="Loan Amount")
        self.table.heading("interest_rate", text="Interest Rate")
        self.table.heading("interest_amount", text="Interest Amount")
        self.table.heading("total_given_amount", text="Total Given Amount")
        self.table.heading("total_collected_amount", text="Total Collected Amount")
        self.table.heading("start_date", text="Start Date")
        self.table.heading("end_date", text="End Date")
        self.table.heading("status", text="Status")
        self.table["show"] = "headings"

        # Column Widths
        self.table.column("acc_no", width=170)
        self.table.column("full_name", width=200)
        self.table.column("mobile_number", width=200)
        self.table.column("loan_amount", width=200)
        self.table.column("interest_rate", width=200)
        self.table.column("interest_amount", width=200)
        self.table.column("total_given_amount", width=210)
        self.table.column("total_collected_amount", width=220)
        self.table.column("start_date", width=200)
        self.table.column("end_date", width=200)
        self.table.column("status", width=200)
         # Assign Tags for alternating row colors
        self.table.tag_configure("odd_row", background="#5a7475")
        self.table.tag_configure("even_row", background="#6885a3")
        self.table.pack(fill=BOTH, expand=1)

        self.show_statement()

        # Footer
        footer = ttkb.Label(self.root, text="Saraswati Bachat Gat\nDesign by: Shrenik", font=("Helvetica", 12, "bold"), justify="center", bootstyle="primary inverse", anchor=CENTER)
        footer.place(anchor="s", relwidth=1, height=60, relx=0.5, rely=1)

    def show_statement(self, status_filter="All"):
        con = sqlite3.connect("loan_database.db")
        cur = con.cursor()
        try:
            # Calculate totals
            total_query = """
                SELECT SUM(loan_amount), SUM(interest_amount), SUM(total_given_amount) 
                FROM customer_loan_list
            """
            if status_filter != "All":
                total_query += f" WHERE LOWER(status) = '{status_filter.lower()}'"
            
            cur.execute(total_query)
            total_result = cur.fetchone()
            total_loan_amount = total_result[0] or 0
            total_interest_amount = total_result[1] or 0
            total_given_amount = total_result[2] or 0

            # Calculate total collected amount correctly
            cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'customer_%' AND name NOT IN ('customer_loan_list')")
            customer_tables = cur.fetchall()

            total_collected_amount = 0
            for table in customer_tables:
                cur.execute(f"SELECT SUM(daily_collection_amount) FROM {table[0]}")
                collected = cur.fetchone()[0] or 0
                total_collected_amount += collected

            # Fetch paginated rows
            offset = (self.current_page - 1) * self.rows_per_page
            query = """
                SELECT acc_no, full_name, mobile_number, loan_amount, interest_rate, 
                    interest_amount, total_given_amount, start_date, end_date, status 
                FROM customer_loan_list
            """
            if status_filter != "All":
                query += f" WHERE LOWER(status) = '{status_filter.lower()}'"
            query += f" LIMIT {self.rows_per_page} OFFSET {offset}"

            cur.execute(query)
            customers = cur.fetchall()

            # Clear existing rows
            self.table.delete(*self.table.get_children())

            # Populate table with paginated rows
            for index, customer in enumerate(customers):
                acc_no, full_name, mobile_number, loan_amount, interest_rate, interest_amount, given_amount, start_date, end_date, status = customer
                table_name = f"customer_{acc_no}"

                # Fetch total collected amount for each customer
                cur.execute(f"SELECT SUM(daily_collection_amount) FROM {table_name}")
                collected_amount = cur.fetchone()[0] or 0

                # Assign tags for alternating row colors
                row_tag = "odd_row" if index % 2 == 0 else "even_row"

                self.table.insert("", END, values=(acc_no, full_name, mobile_number, loan_amount, interest_rate,
                                                    interest_amount, given_amount, collected_amount,
                                                    start_date, end_date, status), tags=(row_tag,))

            # Add totals row at the end
            self.table.insert("", END, values=("TOTAL", "", "", total_loan_amount, "", total_interest_amount,
                                            total_given_amount, total_collected_amount, "", "", ""),
                            tags=('total_row'))
            self.table.tag_configure('total_row', background="blue", font=("Helvetica", 12, "bold"))
            

        except Exception as ex:
            messagebox.showerror("Error", f"Error fetching data: {str(ex)}")
        finally:
            con.close()


    def filter_table(self):
        self.current_page = 1  # Reset to page 1 on filter change
        self.show_statement(status_filter=self.status_var.get())

    def next_page(self):
        self.current_page += 1
        self.page_label.config(text=f"Page: {self.current_page}")
        self.show_statement(status_filter=self.status_var.get())

    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.page_label.config(text=f"Page: {self.current_page}")
            self.show_statement(status_filter=self.status_var.get())


if __name__ == "__main__":
    root = ttkb.Window(themename="darkly")
    app = statement(root)
    root.mainloop()
