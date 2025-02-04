# Saraswati Bachat Gat

Saraswati Bachat Gat is a Loan Management Application built using Python, Tkinter, and ttkbootstrap. It is a multi-window application designed to manage customer loans, daily EMI collections, and loan statements efficiently.

## Features

- **Dashboard:** Main entry point displaying overall loan statistics.
- **Add New Customer:** Register new customers with loan details including:
  - Loan amount, interest rate, interest amount, daily collection amount
  - Auto-generated EMI schedule for 100 days
- **Existing Customer Management:**
  - View and manage customer details
  - EMI statement table for tracking daily payments
- **Due Dates Window:**
  - Displays customers with pending EMIs
  - Last EMI entry from the customer’s statement is reflected here
- **All Statements Window:**
  - Overview of all customers, loan amounts, interest amounts, and repayment status (Ongoing/Closed)

## Technologies Used

- Python
- Tkinter & ttkbootstrap (for UI)
- SQLite3 (for database management)
- PIL (Pillow) for image processing
- ReportLab for PDF generation

## Dependencies

Ensure you have the following dependencies installed before running the project:

```bash
pip install ttkbootstrap pillow reportlab
```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/saraswati-bachat-gat.git
   ```
2. Navigate to the project directory:
   ```bash
   cd saraswati-bachat-gat
   ```
3. Install dependencies:
   ```bash
   pip install ttkbootstrap pillow reportlab
   ```
4. Run the application:
   ```bash
   python main.py
   ```

## Usage

1. Launch the application.
2. Register a new customer in the "Add New Customer" window.
3. Manage loan payments in the "Existing Customer" window.
4. Track EMI due dates in the "Due Dates" window.
5. View overall loan statements in the "All Statements" window.

## Database Structure (SQLite3)

- **Customers Table:** Stores customer details
- **Loans Table:** Records loan amount, interest, and EMI schedule
- **EMI Table:** Maintains daily EMI payments per customer

## Contribution

Feel free to contribute by submitting issues or pull requests!

## License

This project is licensed under the CC BY 4.0 License.

---

---



