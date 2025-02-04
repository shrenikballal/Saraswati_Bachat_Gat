from tkinter import *
from tkinter import ttk, messagebox
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
from dashboard import Dashboard


class Login:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1280x720+0+0")
        self.root.title("Login Page")

        # Title
        title_label = ttkb.Label(root, text="Welcome to the App", font=("Helvetica", 40, "bold"), bootstyle="primary inverse", anchor=CENTER)
        title_label.place(relx=0.5, y=10, anchor="n", relwidth=1, height=80)

        # Frame for form
        frame = ttkb.Frame(root, padding=20, style='TFrame')
        frame.place(relx=0.5, rely=0.4, anchor=CENTER)

        # User ID
        label_id = ttkb.Label(frame, text="User ID:", font=("Helvetica", 12))
        label_id.grid(row=0, column=0, padx=10, pady=10, sticky=W)
        self.entry_id = ttkb.Entry(frame, font=("Helvetica", 12))
        self.entry_id.grid(row=0, column=1, padx=10, pady=10)

        # Password
        label_password = ttkb.Label(frame, text="Password:", font=("Helvetica", 12))
        label_password.grid(row=1, column=0, padx=10, pady=10, sticky=W)
        self.entry_password = ttkb.Entry(frame, show="*", font=("Helvetica", 12))
        self.entry_password.grid(row=1, column=1, padx=10, pady=10)

        # Login Button
        login_button = ttkb.Button(root, text="Login", style="success.TButton", command=self.validate_login)
        login_button.place(relx=0.5, rely=0.6, anchor=CENTER)

    def validate_login(self):
        # Get the user input
        user_id = self.entry_id.get()
        password = self.entry_password.get()

        if user_id == "admin" and password == "password":
            messagebox.showinfo("Login Successful", "Welcome to the Dashboard!")

            # Hide the main window (root)
            self.root.withdraw()

            try:
                # Open the Dashboard in a new Toplevel window
                self.dashboard_window = Toplevel(self.root)
                self.dashboard_object = Dashboard(self.dashboard_window)
                self.dashboard_object.update_dashboard_labels()
                self.dashboard_window.grab_set()
                self.dashboard_window.wait_window()
                
            except Exception as e:
                print(f"Error occurred: {e}")

        else:
            messagebox.showerror("Login Failed", "Invalid ID or Password")
            # Optionally reset the entry fields after a failed login attempt
            self.entry_id.delete(0, END)
            self.entry_password.delete(0, END)
            self.entry_id.focus()


if __name__ == "__main__":
    root = ttkb.Window(themename="darkly")
    object = Login(root)
    root.mainloop()
