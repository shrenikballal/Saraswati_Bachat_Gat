from tkinter import *
from tkinter import ttk, messagebox
from tkinter import PhotoImage
from PIL import Image, ImageTk
import sqlite3
from datetime import datetime, timedelta
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *

class date_list:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1280x720+50+50")
        self.root.title("Date List")
        self.root.focus_force()

        # Create a Title
        statement_title = ttkb.Label(self.root, text="Date List for Ongoing Customers", font=("Helvetica", 25, "bold"), bootstyle="primary inverse", anchor=CENTER)
        statement_title.place(relx=0.5, y=0, anchor="n", relwidth=1, height=80)

        # Table Frame
        frame = ttkb.Frame(self.root, bootstyle="secondary")
        frame.place(x=10, y=100, width=1260, height=550)

        # Scrollbars
        style=ttkb.Style()
        style.configure('custom.Horizontal.TScrollbar', background='black', troughcolor='white', arrowcolor='white')
        style.configure('custom.Vertical.TScrollbar', background='black', troughcolor='white', arrowcolor='white')
        scrolly = ttkb.Scrollbar(frame, orient=VERTICAL, bootstyle="round", style='custom.Vertical.TScrollbar')
        scrollx = ttkb.Scrollbar(frame, orient=HORIZONTAL, bootstyle="round", style='custom.Horizontal.TScrollbar')

        # Table
        style.configure("Treeview", font=("Helvetica", 12), rowheight=35)
        style.configure("Treeview.Heading", font=("Helvetica", 12), padding=(5, 5), background="#0e59bf")
        self.table = ttk.Treeview(
            frame,
            columns=("acc_no", "customer_name", "last_updated_date", "total_daily_collection_amount"),
            yscrollcommand=scrolly.set,
            xscrollcommand=scrollx.set,
        )
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.table.xview)
        scrolly.config(command=self.table.yview)

        # Table Headings
        self.table.heading("acc_no", text="Account Number")
        self.table.heading("customer_name", text="Customer Name")
        self.table.heading("last_updated_date", text="Last Updated Date")
        self.table.heading("total_daily_collection_amount", text="Total Daily Collection Amount")
        self.table["show"] = "headings"

        # Column Widths
        self.table.column("acc_no", width=150)
        self.table.column("customer_name", width=200)
        self.table.column("last_updated_date", width=150)
        self.table.column("total_daily_collection_amount", width=200)

        # Assign Tags for alternating row colors
        self.table.tag_configure("odd_row", background="#5a7475")
        self.table.tag_configure("even_row", background="#6885a3")

        self.table.pack(fill=BOTH, expand=1)

        # Fetch data for the table
        self.fetch_data()

        # Footer
        footer = ttkb.Label(self.root, text="Saraswati Bachat Gat\nDesign by: Shrenik", font=("Helvetica", 12, "bold"), justify="center", bootstyle="primary inverse", anchor=CENTER)
        footer.place(anchor="s", relwidth=1, height=60, relx=0.5, rely=1)

    def fetch_data(self):
        con = sqlite3.connect("loan_database.db")
        cur = con.cursor()
        try:
            cur.execute("SELECT acc_no, full_name FROM customer_loan_list WHERE status='ongoing'")
            customers = cur.fetchall()
            self.table.delete(*self.table.get_children())  # Clear existing rows

            for index, customer in enumerate(customers):
                acc_no, customer_name = customer
                table_name = f"customer_{acc_no}"

                # Fetch the last date with a non-zero daily_collection_amount
                cur.execute(f"""
                    SELECT date FROM {table_name} 
                    WHERE daily_collection_amount > 0 
                    ORDER BY date DESC 
                    LIMIT 1
                """)
                last_updated_date = cur.fetchone()
                last_updated_date = last_updated_date[0] if last_updated_date else "No Entries"

                # Fetch total daily collection
                cur.execute(f"SELECT SUM(daily_collection_amount) FROM {table_name}")
                total_daily_collection_amount = cur.fetchone()[0] or 0

                # Insert row with alternating row colors (odd/even)
                if index % 2 == 0:
                    self.table.insert("", END, values=(acc_no, customer_name, last_updated_date, total_daily_collection_amount),
                                      tags=("even_row",))
                else:
                    self.table.insert("", END, values=(acc_no, customer_name, last_updated_date, total_daily_collection_amount),
                                      tags=("odd_row",))
        except Exception as ex:
            messagebox.showerror("Error", f"Error fetching data: {str(ex)}")
        finally:
            con.close()



if __name__ == "__main__":
    root = ttkb.Window(themename="darkly")
    app = date_list(root)
    root.mainloop()
