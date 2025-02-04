from tkinter import *
from tkinter import ttk, messagebox
from tkinter import PhotoImage
from tkinter import filedialog
from PIL import Image, ImageTk
import sqlite3
from datetime import datetime, timedelta
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, PageBreak
from reportlab.lib.styles import getSampleStyleSheet

class Existing_Customer:
    def __init__(self, root):
        self.root=root
        self.root.geometry("1280x720+50+50")
        self.root.title("Existing Customer")
        self.root.focus_force()

        
        # Create a Title
        new_customer_title = ttkb.Label(self.root, text="Existing Customer", font=("Helvetica", 20, "bold"), bootstyle="primary inverse", anchor=CENTER)
        new_customer_title.place(relx=0.5, y=0, anchor="n", relwidth=1, height=50)

        #Left Frame
        style=ttkb.Style()
        style.configure('TFrame', relief='solid')
        existing_customer_frame1 = ttkb.Frame(self.root, style="TFrame", height=600, width=620)
        existing_customer_frame1.place(x=10, y=55)
        #Right Frame
        existing_customer_frame2 = ttkb.Frame(self.root, style="TFrame", height=600, width=620)
        existing_customer_frame2.place(x=650, y=55)

        #Frame 1 Data
        self.var_search = StringVar()
        lbl_search_name = ttkb.Label(existing_customer_frame1, text="Customer Name:", font=("Helvetica", 12, "bold"), style="TLabel").place(x=30, y=10)
        style.configure('custom.TEntry', selectbackground='lightyellow', selectborderwidth=5, font=("Helvetica", 12, "bold"))
        txt_search_name = ttkb.Entry(existing_customer_frame1, textvariable=self.var_search, style='custom.TEntry').place(x=200, y=10, width=250, height=35)
        style.configure("TButton", font=("Helvetica", 12, "bold"), bordercolor="darkblue", relief="solid")
        search_button = ttkb.Button(existing_customer_frame1, text="Search", style="info.TButton", cursor="hand2", command=self.search_customer).place(x=475, y=10, width=100, height=35)
        
        customer_data_inner_frame = Frame(existing_customer_frame1, bg="lightgreen", bd=2, relief="solid") 
        customer_data_inner_frame.place(x=30, y=50, height=540, width=550)

        #Scrollbar
        style.configure('custom.Horizontal.TScrollbar', background='black', troughcolor='white', arrowcolor='white')
        style.configure('custom.Vertical.TScrollbar', background='black', troughcolor='white', arrowcolor='white')
        customer_data_inner_frame_scrolly = ttkb.Scrollbar(customer_data_inner_frame, orient=VERTICAL, bootstyle="round", style='custom.Vertical.TScrollbar')
        customer_data_inner_frame_scrollx = ttkb.Scrollbar(customer_data_inner_frame, orient=HORIZONTAL, bootstyle="round", style='custom.Horizontal.TScrollbar')

        #Customer Table
        style.configure("Treeview", font=("Helvetica", 10), rowheight=35)
        style.configure("Treeview.Heading", font=("Helvetica", 10), padding=(5, 5), background="#0e59bf")
        self.customer_name_table = ttk.Treeview(customer_data_inner_frame, columns=("account_number", "customer_name", "mobile_number", "loan_amount", "total_given_amount", "daily_collection_amount", "start_date", "end_date"), yscrollcommand=customer_data_inner_frame_scrolly.set, xscrollcommand=customer_data_inner_frame_scrollx.set) 
        #Configure Scrollbar
        customer_data_inner_frame_scrolly.config(command=self.customer_name_table.yview)
        customer_data_inner_frame_scrollx.config(command=self.customer_name_table.xview)
        #Pack Treeview & Scrollbar
        customer_data_inner_frame_scrolly.pack(side=RIGHT, fill=Y)
        customer_data_inner_frame_scrollx.pack(side=BOTTOM, fill=X)
        
        # Configure Treeview Columns
        self.customer_name_table.heading("account_number", text="A/C Number") 
        self.customer_name_table.heading("customer_name", text="Customer Name") 
        self.customer_name_table.heading("mobile_number", text="Mobile Number") 
        self.customer_name_table.heading("loan_amount", text="Loan Amount") 
        self.customer_name_table.heading("total_given_amount", text="Total Given Amount") 
        self.customer_name_table.heading("daily_collection_amount", text="Daily Collection Amount") 
        self.customer_name_table.heading("start_date", text="Start Date") 
        self.customer_name_table.heading("end_date", text="End Date") 
        self.customer_name_table["show"]='headings'
        self.customer_name_table.column("account_number", width=110, minwidth=110, anchor=W)
        self.customer_name_table.column("customer_name", width=200, minwidth=150, anchor=W)
        self.customer_name_table.column("mobile_number", width=130, minwidth=130, anchor=W)
        self.customer_name_table.column("loan_amount", width=100, minwidth=100, anchor=W)
        self.customer_name_table.column("total_given_amount", width=180, minwidth=180, anchor=W)
        self.customer_name_table.column("daily_collection_amount", width=200, minwidth=200, anchor=W)
        self.customer_name_table.column("start_date", width=100, minwidth=100, anchor=W)
        self.customer_name_table.column("end_date", width=100, minwidth=100, anchor=W)
        
        # Assign Tags for alternating row colors
        self.customer_name_table.tag_configure("odd_row", background="#5a7475")
        self.customer_name_table.tag_configure("even_row", background="#6885a3")
        self.customer_name_table.pack(fill=BOTH, expand=TRUE)
        self.customer_name_table.bind("<ButtonRelease-1>", self.load_emi_data)
        self.show_search_table()

        #Frame 2 Data
        style.configure('TLabel', foreground='white')
        lbl_emi_data_title = ttkb.Label(existing_customer_frame2, text="Customer Daily Collection", font=("Helvetica", 12, "bold"), style="TLabel", anchor=CENTER)
        lbl_emi_data_title.place(relwidth=1)
        customer_emi_inner_frame = Frame(existing_customer_frame2, bg="lightgreen", bd=2, relief="solid") 
        customer_emi_inner_frame.place(x=15, y=85, height=450, width=585)

        self.lbl_customer_name=ttkb.Label(existing_customer_frame2, text="Costomer Name:", font=("Helvetica", 12, "bold"), style="TLabel").place(x=10,y=40)
        self.lbl_customer_search_name=ttkb.Label(existing_customer_frame2, text="", font=("Helvetica", 12, "bold"), style="TLabel")
        self.lbl_customer_search_name.place(x=175,y=40)

        #Scrollbar
        style.configure('custom.Vertical.TScrollbar', background='black', troughcolor='white', arrowcolor='white')
        customer_emi_inner_frame_scrolly=ttkb.Scrollbar(customer_emi_inner_frame, orient=VERTICAL, bootstyle="round", style='custom.Vertical.TScrollbar')

        self.customer_emi_table = ttk.Treeview(customer_emi_inner_frame, columns=("day_no", "date", "daily_collection_amount", "cumulative_total"), show="headings", yscrollcommand=customer_emi_inner_frame_scrolly.set) 
        customer_emi_inner_frame_scrolly.pack(side=RIGHT, fill=Y)
        customer_emi_inner_frame_scrolly.config(command=self.customer_emi_table.yview)

        self.customer_emi_table.heading("day_no", text="No. Of Days") 
        self.customer_emi_table.heading("date", text="Collection Date") 
        self.customer_emi_table.heading("daily_collection_amount", text="Daily Collection") 
        self.customer_emi_table.heading("cumulative_total", text="Cumulative Total") 
        self.customer_emi_table["show"]='headings'
        self.customer_emi_table.column("day_no", width=50, anchor=CENTER) 
        self.customer_emi_table.column("date", width=50, anchor=CENTER) 
        self.customer_emi_table.column("daily_collection_amount", width=50, anchor=CENTER) 
        self.customer_emi_table.column("cumulative_total", width=50, anchor=CENTER)

        # Add striped rows for grid effect
        self.customer_emi_table.tag_configure("odd_row", background="#5a7475")
        self.customer_emi_table.tag_configure("even_row", background="#6885a3")

        self.customer_emi_table.pack(fill="both", expand=True)
        
        self.customer_emi_table.bind("<Double-1>", self.edit_table_value)

        style.configure("TButton", font=("Helvetica", 11))
        emi_submit_button = ttkb.Button(existing_customer_frame2, text="Submit", style='info.TButton', cursor="hand2", command=self.submit_daily_collection)
        emi_submit_button.place(x=20, y=540, width=130)
        
        loan_foreclose_button = ttkb.Button(existing_customer_frame2, text="Foreclose", style='warning.TButton', cursor="hand2", command=self.loan_foreclose)
        loan_foreclose_button.place(x=160, y=540, width=130)
        
        back_home_button = ttkb.Button(existing_customer_frame2, text="Back / Home", style='danger.TButton', cursor="hand2", command=self.root.destroy)
        back_home_button.place(x=300, y=540, width=130)

        generate_pdf_button = ttkb.Button(existing_customer_frame2, text="Generate PDF", style='success.TButton', cursor="hand2", command=self.generate_customer_statement)
        generate_pdf_button.place(x=440, y=540, width=135)


        
        # Footer
        footer = ttkb.Label(self.root, text="Saraswati Bachat Gat\nDesign by: Shrenik", font=("Helvetica", 12, "bold"), justify="center", bootstyle="primary inverse", anchor=CENTER)
        footer.place(anchor="s", relwidth=1, height=60, relx=0.5, rely=1)

    #Functions
    def show_search_table(self):
        con=sqlite3.connect("loan_database.db")
        cur=con.cursor()
        try:
            cur.execute("select acc_no, full_name, mobile_number, loan_amount, total_given_amount, daily_collection_amount, start_date, end_date from customer_loan_list WHERE status='ongoing'")
            rows=cur.fetchall()
            self.customer_name_table.delete(*self.customer_name_table.get_children())
            
            for index, row in enumerate(rows):
                tag = 'odd_row' if index % 2 == 0 else 'even_row'
                self.customer_name_table.insert('', END, values=row, tags=(tag,))
        
        except Exception as ex:
            messagebox.showerror("Error", f"Error Due to {str(ex)}")
        finally:
            con.close()


    def search_customer(self):
        search_term = self.var_search.get().lower() 
        for item in self.customer_name_table.get_children(): 
            values = self.customer_name_table.item(item, "values") 
            if search_term in values[1].lower(): 
                self.customer_name_table.selection_set(item) 
                self.customer_name_table.see(item) 
                break 
            else: messagebox.showinfo("Not found", "Customer not found")



    def load_emi_data(self, event):
        item = self.customer_name_table.selection()[0]
        acc_no, customer_name, mobile_number, loan_amount, total_given_amount, daily_collection_amount, start_date, end_date = self.customer_name_table.item(item, 'values')
        start_date = self.get_start_date(acc_no)

        self.lbl_customer_search_name.config(text=customer_name)
        table_name = f"customer_{acc_no}"
        self.populate_customer_emi_table(table_name)


    def get_start_date(self, acc_no):
        con = sqlite3.connect("loan_database.db")
        cur = con.cursor()
        try:
            cur.execute("SELECT start_date FROM customer_loan_list WHERE acc_no=?", (acc_no,))
            start_date = cur.fetchone()[0]
        except Exception as ex:
            messagebox.showerror("Error", f"Error fetching start date: {str(ex)}")
            start_date = datetime.today().strftime("%d-%m-%Y")
        finally:
            con.close()
        return start_date

    def populate_customer_emi_table(self, table_name):
        con = sqlite3.connect("loan_database.db")
        cur = con.cursor()
        try:
            
            cur.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
            table_exists = cur.fetchone()
            
            if not table_exists:
                messagebox.showerror("Error", f"Table {table_name} does not exist in the database.")
                return

            # Fetch the EMI data for the customer from their respective table
            cur.execute(f"SELECT day_no, date, daily_collection_amount, cumulative_total FROM {table_name}")
            rows = cur.fetchall()

            # Clear existing rows in the EMI table
            self.customer_emi_table.delete(*self.customer_emi_table.get_children())
            
            # Insert new rows from the fetched data
            for index, row in enumerate(rows):
                tag = 'odd_row' if index % 2 == 0 else 'even_row'
                self.customer_emi_table.insert('', END, values=row, tags=(tag,))
                
        
        except Exception as ex:
            messagebox.showerror("Error", f"Error fetching data: {str(ex)}")
        finally:
            con.close()



        self.update_total_row()

   
    def edit_table_value(self, event):
        # Get selected item and column
        try:
            selected_item = self.customer_emi_table.selection()[0]
            col = self.customer_emi_table.identify_column(event.x)
            row = self.customer_emi_table.identify_row(event.y)
            if not selected_item or not col or not row:
                return
        except IndexError:
            return  # No item selected

        # Allow editing only the `daily_collection_amount` column (column 3)
        if col == '#3':
            # Calculate cell bounds
            bbox = self.customer_emi_table.bbox(selected_item, column=col)
            if not bbox:
                return

            entry_widget = Entry(self.customer_emi_table)
            entry_widget.place(x=bbox[0], y=bbox[1], width=bbox[2], height=bbox[3])

            def save_edit(event=None):
                new_value = entry_widget.get()
                try:
                    # Validate input
                    new_value = float(new_value)
                    self.customer_emi_table.set(selected_item, column="daily_collection_amount", value=new_value)
                    # Update cumulative sum
                    self.update_cumulative_sum()
                except ValueError:
                    messagebox.showerror("Input Error", "Please enter a valid number.")
                finally:
                    entry_widget.destroy()  # Remove Entry widget after editing

            entry_widget.bind("<Return>", save_edit)
            entry_widget.focus()


    def update_cumulative_sum(self):
        rows = self.customer_emi_table.get_children()
        cumulative_sum = 0
        for row in rows:
            daily_collection = float(self.customer_emi_table.item(row)['values'][2])
            cumulative_sum += daily_collection
            # Update cumulative total in the table
            self.customer_emi_table.set(row, column="cumulative_total", value=cumulative_sum)
        
        self.update_total_row()



    def submit_daily_collection(self):
        selected_customer = self.customer_name_table.selection()
        if not selected_customer:
            messagebox.showerror("Error", "Please select a customer first.")
            return

        acc_no, customer_name, mobile_number, loan_amount, total_given_amount, daily_collection_amount, start_date, end_date = self.customer_name_table.item(selected_customer[0], 'values')
        table_name = f"customer_{acc_no}"

        con = sqlite3.connect("loan_database.db")
        cur = con.cursor()
        try:
            for row in self.customer_emi_table.get_children():
                day_no = self.customer_emi_table.item(row)['values'][0]
                if day_no == "Total":  # Skip the "Total" row
                    continue
                
                new_daily_collection_amount = float(self.customer_emi_table.item(row)['values'][2])
                cumulative_total = float(self.customer_emi_table.item(row)['values'][3])

                # Fetch the existing daily_collection_amount from the database
                cur.execute(f"SELECT daily_collection_amount FROM {table_name} WHERE day_no = ?", (day_no,))
                result = cur.fetchone()

                if result:
                    existing_daily_collection_amount = result[0]
                else:
                    messagebox.showerror("Error", f"Day {day_no} not found in database.")
                    continue

                # Update only if the daily_collection_amount has changed
                if new_daily_collection_amount != existing_daily_collection_amount:
                    entered_date = datetime.today().strftime("%d-%m-%Y")  # Update the entered_date
                    cur.execute(f"""
                        UPDATE {table_name}
                        SET daily_collection_amount = ?, cumulative_total = ?, entered_date = ?
                        WHERE day_no = ?
                    """, (new_daily_collection_amount, cumulative_total, entered_date, day_no))
                else:
                    # Update only the cumulative_total without changing the entered_date
                    cur.execute(f"""
                        UPDATE {table_name}
                        SET cumulative_total = ?
                        WHERE day_no = ?
                    """, (cumulative_total, day_no))

            con.commit()
            messagebox.showinfo("Success", "Daily collections updated successfully!")
            self.update_total_row()  # Refresh the total row
        except Exception as ex:
            messagebox.showerror("Error", f"Error updating database: {str(ex)}")
        finally:
            con.close()


    def update_total_row(self):
        # Get all rows excluding the "Total" row
        rows = self.customer_emi_table.get_children()
        rows = [row for row in rows if self.customer_emi_table.item(row)['values'][0] != "Total"]

        # Recalculate total of daily_collection_amount
        total_daily_collection = sum(
            float(self.customer_emi_table.item(row)['values'][2]) for row in rows
        )

        # Remove any existing "Total" row
        existing_total_rows = [
            row for row in self.customer_emi_table.get_children()
            if self.customer_emi_table.item(row)['values'][0] == "Total"
        ]
        for row in existing_total_rows:
            self.customer_emi_table.delete(row)

        # Add the "Total" row back with the updated total
        self.customer_emi_table.insert('', 'end', values=("Total", "", total_daily_collection, ""), tags=('total_row'))

        # Check if total_daily_collection matches the loan amount
        selected_customer = self.customer_name_table.selection()
        if selected_customer:
            acc_no, customer_name, mobile_number, loan_amount, total_given_amount, daily_collection_amount, start_date, end_date = self.customer_name_table.item(selected_customer[0], 'values')

            # Update status in the database if total_daily_collection equals or exceeds loan_amount
            if total_daily_collection >= float(loan_amount):
                con = sqlite3.connect("loan_database.db")
                cur = con.cursor()
                try:
                    cur.execute("""
                        UPDATE customer_loan_list
                        SET status = 'closed'
                        WHERE acc_no = ?
                    """, (acc_no,))
                    con.commit()
                    messagebox.showinfo("Loan Status Updated", f"The loan for {customer_name} has been marked as closed.")
                except Exception as ex:
                    messagebox.showerror("Error", f"Error updating loan status: {str(ex)}")
                finally:
                    con.close()


    def loan_foreclose(self):
        selected_customer = self.customer_name_table.selection()
        if not selected_customer:
            messagebox.showerror("Error", "Please select a customer first.")
            return

        # Retrieve selected customer details
        acc_no, customer_name, mobile_number, loan_amount, total_given_amount, daily_collection_amount, start_date, end_date = self.customer_name_table.item(selected_customer[0], 'values')

        # Confirm the foreclosure action
        confirm = messagebox.askyesno("Confirm Foreclosure", f"Are you sure you want to foreclose the loan for {customer_name} (Account No: {acc_no})?")
        if not confirm:
            return

        # Update loan status to 'foreclosed' directly in the database
        con = sqlite3.connect("loan_database.db")
        cur = con.cursor()
        try:
            cur.execute("""
                UPDATE customer_loan_list
                SET status = 'closed'
                WHERE acc_no = ?
            """, (acc_no,))
            con.commit()

            # Notify the user and refresh the table
            messagebox.showinfo("Success", f"The loan for {customer_name} (Account No: {acc_no}) has been foreclosed successfully.")
            self.show_search_table()  # Refresh the table to show updated loan status
        except Exception as ex:
            messagebox.showerror("Error", f"Error foreclosing loan: {str(ex)}")
        finally:
            con.close()


    def generate_customer_statement(self):
        # Check if a customer is selected
        selected_customer = self.customer_name_table.selection()
        if not selected_customer:
            messagebox.showerror("Error", "Please select a customer first.")
            return

        # Get customer details
        acc_no, customer_name, mobile_number, loan_amount, total_given_amount, daily_collection_amount, start_date, end_date = self.customer_name_table.item(selected_customer[0], 'values')

        # Fetch table data from the database
        table_name = f"customer_{acc_no}"
        con = sqlite3.connect("loan_database.db")
        cur = con.cursor()
        try:
            cur.execute(f"SELECT day_no, date, daily_collection_amount, cumulative_total FROM {table_name}")
            rows = cur.fetchall()
        except Exception as ex:
            messagebox.showerror("Error", f"Error fetching table data: {str(ex)}")
            return
        finally:
            con.close()

        # Apply PDF-only condition: cumulative_total = 0 if daily_collection_amount == 0
        pdf_rows = []
        for row in rows:
            day_no, date, daily_collection_amount, cumulative_total = row
            if daily_collection_amount == 0:
                cumulative_total = 0  # For PDF purposes only
            pdf_rows.append([day_no, date, daily_collection_amount, cumulative_total])

        # Add headers to the data
        data = [["Day No", "Collection Date", "Daily Collection", "Cumulative Total"]]  # Headers
        data.extend(pdf_rows)  # Add processed rows
        
        # Prompt user to select a save location
        pdf_file = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            initialfile=f"{customer_name}_Statement.pdf",
            title="Save PDF As"
        )
        if not pdf_file:  # User cancelled the save dialog
            return

        # Create PDF document
        pdf_doc = SimpleDocTemplate(pdf_file, pagesize=letter)
        elements = []

        # Add customer details to the PDF
        styles = getSampleStyleSheet()
        elements.append(Paragraph("<b>Customer Loan Statement</b>", styles['Title']))
        elements.append(Paragraph(f"Customer Name: {customer_name}", styles['Normal']))
        elements.append(Paragraph(f"Account Number: {acc_no}", styles['Normal']))
        elements.append(Paragraph(f"Loan Amount: {loan_amount}", styles['Normal']))
        elements.append(Paragraph(f"Mobile Number: {mobile_number}", styles['Normal']))
        elements.append(Paragraph(f"Start Date: {start_date}", styles['Normal']))
        elements.append(Paragraph(f"End Date: {end_date}", styles['Normal']))
        elements.append(Paragraph("<br/>", styles['Normal']))  # Spacer

        # Create table
        table = Table(data, repeatRows=1)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))

        # Add table to elements
        elements.append(table)

        # Build the PDF
        try:
            pdf_doc.build(elements)
            messagebox.showinfo("Success", f"PDF saved successfully at: {pdf_file}")
        except Exception as ex:
            messagebox.showerror("Error", f"Error generating PDF: {str(ex)}")

   
if __name__ == "__main__":
    root=ttkb.Window(themename="darkly")
    object=Existing_Customer(root)
    root.mainloop()