import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from tkinter import *


class DatabaseManager:
    def __init__(self, host, port, user, password, database):
        try:
            self.db = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
            )
            self.cursor = self.db.cursor()
            self.create_tables()
            self.db_manager = self  
        except mysql.connector.Error as e:
            messagebox.showerror("Database Connection Error", f"Error: {e}")

    def create_tables(self):
        try:
            create_tables_query = """
            CREATE TABLE IF NOT EXISTS customers (
                customer_id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                password VARCHAR(255) NOT NULL,
                phone VARCHAR(15) NOT NULL,
                payment_method VARCHAR(20)
            );

            CREATE TABLE IF NOT EXISTS customers_order (
            booking_id INT AUTO_INCREMENT PRIMARY KEY,
            pickup_location VARCHAR(255) NOT NULL,
            pickup_time VARCHAR(255) NOT NULL,
            pickup_date VARCHAR(255) NOT NULL,
            dropoff_location VARCHAR(255) NOT NULL,
            customer_id INT,
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
            driver_id INT,
            FOREIGN KEY (driver_id) REFERENCES drivers(id)
);

            );

            CREATE TABLE IF NOT EXISTS drivers (
                driver_id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                password VARCHAR(255) NOT NULL,
                phone VARCHAR(15) NOT NULL,
                license_number VARCHAR(20)
            );
            """
            self.cursor.execute(create_tables_query, multi=True)
            self.db.commit()

        except mysql.connector.Error as e:
            messagebox.showerror("Table Creation Error", f"Error: {e}")

            
    def get_customer_id(self, username):
        try:
            query = 'SELECT customer_id FROM customers WHERE name=%s'
            self.cursor.execute(query, (username,))
            row = self.cursor.fetchone()

            if row:
                return row[0]
            else:
                messagebox.showerror('Error', 'Customer not found.')
                return None

        except mysql.connector.Error as e:
            messagebox.showerror('Error', f'Database Error: {e}')
            return None



    def register_user(self, table, name, email, password, phone, additional_info):
        try:
            query = f"INSERT INTO {table} (name, email, password, phone, {additional_info['field']}) VALUES (%s, %s, %s, %s, %s)"
            values = (name, email, password, phone, additional_info['value'])
            self.cursor.execute(query, values)
            self.db.commit()
            print(f"{table.capitalize()} registration successful.")
        except mysql.connector.Error as e:
            print(f"Error: {e}")
            messagebox.showerror("Registration Error", f"Failed to register {table}.")


    def book_order(self, table, pickup_location, pickup_time, pickup_date, dropoff_location, additional_info):
        try:
            query = f"INSERT INTO {table} (pickup_location, pickup_time, pickup_date, dropoff_location, {additional_info['field']}) VALUES (%s, %s, %s, %s, %s)"
            values = (pickup_location, pickup_time, pickup_date, dropoff_location, additional_info['value'])
            self.cursor.execute(query, values)
            self.db.commit()
            print(f"{table.capitalize()} registration successful.")
        except mysql.connector.Error as e:
            print(f"Error: {e}")
            messagebox.showerror("Registration Error", f"Failed to register {table}.")

class BaseRegistrationForm:
    def __init__(self, root, role, database_manager):
        self.root = root
        self.role = role
        self.database_manager = database_manager
        self.root.title(f"{self.role} Registration")
        self.root.geometry("400x300")
        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self.root, text="Name:").place(x=50, y=10)
        self.name_entry = ttk.Entry(self.root)
        self.name_entry.place(x=130, y=10)

        ttk.Label(self.root, text="Email:").place(x=50, y=50)
        self.email_entry = ttk.Entry(self.root)
        self.email_entry.place(x=130, y=50)

        ttk.Label(self.root, text="Password:").place(x=50, y=90)
        self.password_entry = ttk.Entry(self.root, show="*")
        self.password_entry.place(x=130, y=90)

        ttk.Label(self.root,text='Phone No.:').place(x=50,y=130)
        self.phone_entry = ttk.Entry(self.root)
        self.phone_entry.place(x=130, y=130)

        self.additional_fields()
        

        ttk.Button(self.root, text="Register", command=self.register).place(x=150, y=200)
        Button(self.root, text='Click here to login', fg='blue', border=0, cursor='hand2',command=self.to_login).place(x=130, y=230)
    
    def to_login(self):
        self.root.destroy()
        reg_window = tk.Tk()
        LoginForm(reg_window, self.root)

    def additional_fields(self):
        pass

    def register(self):
        
        name = self.name_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()
        phone =self.phone_entry.get()

        additional_info = self.get_additional_info()
        if name==''or email=='' or  password=='' or phone==''or additional_info is None:
            messagebox.showerror('Error','All fields are required!')
        else:

            table = 'customers' if self.role.lower() == 'customer' else 'drivers'
            self.database_manager.register_user(table, name, email, password, phone, additional_info)

    def get_additional_info(self):
        return ""

class CustomerRegistrationForm(BaseRegistrationForm):
    def additional_fields(self):
        self.combo = ttk.Combobox(self.root, values=['Cash', 'Mobile Wallet', 'Online Banking'])
        self.combo.place(x=50, y=160)
        self.combo.bind('<<ComboboxSelected>>')
        self.combo.set("Cash")
        self.combo['state'] = 'readonly'

    def get_additional_info(self):
        selected_payment_method = self.combo.get()
        if selected_payment_method == "Select Payment Method":
            messagebox.showerror("Error", "Please select a payment method.")
            return None
        else:
            return {'field': 'payment_method', 'value': selected_payment_method}

        

class DriverRegistrationForm(BaseRegistrationForm):
    def additional_fields(self):
        ttk.Label(self.root, text="License No.:").place(x=50, y=160)
        self.license_entry = ttk.Entry(self.root)
        self.license_entry.place(x=130, y=160)

    def get_additional_info(self):
        if self.license_entry.get()=='':
            messagebox.showerror("Error", "Please enter you plate number.")
            return None
        else:
            return {'field': 'license_number', 'value': self.license_entry.get()}
    
class LoginForm:
    def __init__(self, root, main_window):
        self.root = root
        self.main_window = main_window
        print("LoginForm created")
        self.root.title('Login Page')
        self.root.geometry('400x300')

        ttk.Label(self.root, text='Username:').place(x=50, y=10)
        self.username_entry = ttk.Entry(self.root)
        self.username_entry.place(x=130, y=10)

        ttk.Label(self.root, text='Password:').place(x=50, y=50)
        self.password_entry = ttk.Entry(self.root, show='*')
        self.password_entry.place(x=130, y=50)

        ttk.Button(self.root, text='Login', command=self.login_and_close_main).place(x=150, y=90)
        Button(self.root, text='Click here to register', fg='blue', border=0, cursor='hand2',command=self.back_to_reg).place(x=130, y=130)

    def back_to_reg(self):
        self.root.destroy()
        reg_window = tk.Tk()
        RegistrationApp(reg_window, self.root)

    def login_and_close_main(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        self.db_manager = db_manager

        try:
            with mysql.connector.connect(host='localhost', user='root', password='Devil_B0y', database='taxi_booking') as con:
                mycursor = con.cursor()

            # Query for admin
                if username == 'admin' and password == 'password':
                    messagebox.showinfo('Login Successful', 'Welcome, Admin!')
                    self.root.destroy()
                    from admin import Adminpage
                    root = Tk()
                    Adminpage(root)
                    return 

            # Reset cursor for the customer query
                mycursor.close()
                mycursor = con.cursor()

            # Query for customers
                query = 'SELECT * FROM customers WHERE name=%s AND password=%s'
                mycursor.execute(query, (username, password))
                row = mycursor.fetchone()

                if row:
                    messagebox.showinfo('Success', 'Login Successful')
                    self.root.destroy()
                    from customer import Customerpage
                    root = Tk()
                    Customerpage(root, self.db_manager, username)
                    return  # Exit the function after successful customer login

            # Reset cursor for the driver query
                mycursor.close()
                mycursor = con.cursor()

            # Query for drivers
                query = 'SELECT * FROM drivers WHERE name=%s AND password=%s'
                mycursor.execute(query, (username, password))
                row1 = mycursor.fetchone()

                if row1:
                    messagebox.showinfo('Success', 'Login Successful')
                    self.root.destroy()
                    from driverpage import Driverpage
                    root = Tk()
                    Driverpage(root)
                    return  

        except mysql.connector.Error as e:
            messagebox.showerror('Error', f'Database Error: {e}')

        messagebox.showerror('Error', 'Username or password is invalid')

           
        

class RegistrationApp:
    def __init__(self, root, database_manager):
        self.root = root
        self.root.title("Registration")
        self.root.geometry("400x300")
        self.database_manager = database_manager
        self.create_role_selection()

    def create_role_selection(self):
        ttk.Label(self.root, text="Select Role:").pack(pady=10)
        self.role_var = tk.StringVar()
        role_options = ["Customer", "Driver"]
        self.role_combobox = ttk.Combobox(self.root, textvariable=self.role_var, values=role_options)
        self.role_combobox.pack(pady=10)
        self.role_combobox.set("Customer")

        ttk.Button(self.root, text="Continue", command=self.open_registration_form).pack(pady=10)
        loginlab = Label(self.root, text='Already have an account?').place(x=130, y=120)
        login = Button(self.root, text="Click here to login", border=0, fg='blue', cursor='hand2',command=self.open_login_page).place(x=150, y=140)

    def open_registration_form(self):
        role = self.role_var.get()

        if role == "Customer":
            registration_form = CustomerRegistrationForm(tk.Toplevel(), role, self.database_manager)
        elif role == "Driver":
            registration_form = DriverRegistrationForm(tk.Toplevel(), role, self.database_manager)
        else:
            registration_form = tk.Toplevel()
        self.root.withdraw()

    def open_login_page(self):
        self.root.destroy()
        login_window = tk.Tk()
        login_form = LoginForm(login_window, self.root)

if __name__ == "__main__":
    db_manager = DatabaseManager("localhost", 3306, "root", "Devil_B0y", "taxi_booking")
    root = tk.Tk()
    app = RegistrationApp(root, db_manager)
    root.mainloop()
