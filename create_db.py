import sqlite3
def create_db():
    con=sqlite3.connect(database="loan_database.db")
    cur=con.cursor()
    cur.execute("create table if not exists customer_loan_list (acc_no integer primary key autoincrement, full_name text, mobile_number text, address text, mediator_name text, loan_amount text, interest_rate text, interest_amount text, total_given_amount text, term integer, daily_collection_amount text, start_date text, end_date text, status text default ongoing)")
    con.commit()

create_db()