import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from tkinter import *
import pymysql



def logout(root):
    root.destroy()
    from regandlog import LoginForm
    login_root = Tk()
    LoginForm(login_root, root)

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
        except mysql.connector.Error as e:
            messagebox.showerror("Database Connection Error", f"Error: {e}")


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
        
    def book_taxi(self, pickup_location, pickup_time, pickup_date, dropoff_location, customer_id):
        try:
            query = "INSERT INTO customers_order (pickup_location, pickup_time, pickup_date, dropoff_location, customer_id) VALUES (%s, %s, %s, %s, %s)"
            values = (pickup_location, pickup_time, pickup_date, dropoff_location, customer_id)
            self.cursor.execute(query, values)
            self.db.commit()
            print("Taxi booking successful.")
        except mysql.connector.Error as e:
            print(f"Error: {e}")
            messagebox.showerror("Booking Error", "Failed to book taxi.")

    def create_tables(self):
        try:
            create_tables_query =("""
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

            """)
            self.cursor.execute(create_tables_query, multi=True)
            self.db.commit()

        except mysql.connector.Error as e:
            messagebox.showerror("Table Creation Error", f"Error: {e}")



class Customerpage:
    def __init__(self, root, db_manager, logged_in_username=None):
        self.root = root
        self.db_manager = db_manager  
        self.logged_in_username = logged_in_username
        self.root.geometry("1200x550+100+100")
        self.root.title('Customer Page')
        self.root.config(bg='yellow')
        self.customer()

    def customer(self):
        frame = Frame(self.root, bg='white', bd=3, relief='ridge')
        frame.place(x=10, y=40, width=200, height=200)

        self.pickup_location = Label(frame, text='Pickup Location', bg='white')
        self.pickup_location.place(x=15, y=15)
        self.pickup_location_entry = Entry(frame, border=2)
        self.pickup_location_entry.place(x=25, y=35)

        self.pickup_time = Label(frame, text='Pickup Time', bg='white')
        self.pickup_time.place(x=15, y=55)
        self.pickup_time_opt = self.generate_time_options()

        selected_option = tk.StringVar()
        selected_option.set(self.pickup_time_opt[0])

        self.dropdown_menu = ttk.Combobox(frame, textvariable=selected_option, values=self.pickup_time_opt)
        self.dropdown_menu.place(x=25, y=75)

        self.pickup_date = Label(frame, text='Pickup Date', bg='white')
        self.pickup_date.place(x=15, y=100)
        self.pickup_date_entry = Entry(frame, border=2)
        self.pickup_date_entry.place(x=25, y=120)
        self.dropoff_location = Label(frame, text='Dropoff Location', bg='white')
        self.dropoff_location.place(x=15, y=140)
        self.dropoff_location_entry = Entry(frame, border=2)
        self.dropoff_location_entry.place(x=25, y=160)

        self.bookbutton = Button(self.root, text='Book', font=('Microsoft YaHei UI light', 15, 'bold'), cursor='hand2',command=self.book)
        self.bookbutton.place(x=10, y=255, width=200, height=50)

        self.cancelbutton = Button(self.root, text='Cancel Booking', font=('Microsoft YaHei UI light', 15, 'bold'), cursor='hand2',command=self.delete_booking)
        self.cancelbutton.place(x=10, y=310, width=200, height=50)

        self.frame2 = Frame(self.root, bg='white', bd=3, relief='ridge')
        self.frame2.place(x=250, y=40, width=900, height=430)
        self.show_booking()

        self.logoutbutton = Button(self.root, text='Log Out', font=('Microsoft YaHei UI light', 15, 'bold'),command=lambda: logout(self.root), cursor='hand2')
        self.logoutbutton.place(x=10, y=365, width=200, height=50)
        self.exitbutton = Button(self.root, text='EXIT', font=('Microsoft YaHei UI light', 15, 'bold'), command=quit,cursor='hand2')
        self.exitbutton.place(x=10, y=420, width=200, height=50)

    def generate_time_options(self):
        time_options = []
        for hour in range(0, 24):
            for minute in range(0, 60, 15):
                time_str = f"{hour:02d}:{minute:02d}"
                time_options.append(time_str)
        return time_options

    def book(self):
        pickup_location = self.pickup_location_entry.get()
        pickup_time = self.dropdown_menu.get()
        pickup_date = self.pickup_date_entry.get()
        dropoff_location = self.dropoff_location_entry.get()

        if pickup_location == '' or pickup_time == '' or pickup_date == '' or dropoff_location == '':
            messagebox.showerror('Error', 'All fields are required!')
        else:
            # Import LoginForm inside the book method
            from regandlog import LoginForm
            # Get the customer ID using the DatabaseManager
            customer_id = self.db_manager.get_customer_id(self.logged_in_username)

            if customer_id is not None:
                table = 'customers_order'
                # Pass additional_info as a dictionary
                print("Upto Here 1")
                additional_info = {'field': 'customer_id', 'value': customer_id}
                self.db_manager.book_order(table, pickup_location, pickup_time, pickup_date, dropoff_location, additional_info)
                print("Upto Here 2")
                self.refresh_display()

    def show_booking(self):
        self.booking_tree = ttk.Treeview(self.frame2, columns=("ID", "pickup_location", "dropoff_location", "pickup_time", "pickup_date"), show="headings", height=10)

        # Add headings to the Treeview
        self.booking_tree.heading("ID", text="ID")
        self.booking_tree.heading("pickup_location", text="pickup_location")
        self.booking_tree.heading("dropoff_location", text="dropoff_location")
        self.booking_tree.heading("pickup_time", text="pickup_time")
        self.booking_tree.heading("pickup_date", text="pickup_date")
       

        # Set column widths
        self.booking_tree.column("ID", width=100, anchor="center")
        self.booking_tree.column("pickup_location", width=150, anchor="center")
        self.booking_tree.column("dropoff_location", width=150, anchor="center")
        self.booking_tree.column("pickup_time", width=100, anchor="center")
        self.booking_tree.column("pickup_date", width=100, anchor="center")
        
        booking_details = self.booking_details()
        for bookings in booking_details:
            self.booking_tree.insert("", "end", values=bookings)
        

        self.booking_tree.pack(side=TOP, expand=YES, fill=BOTH)

    def booking_details(self):
        try:
            con = pymysql.connect(host="localhost", user="root", password="Devil_B0y")
            mycursor = con.cursor()
            mycursor.execute('use taxi_booking')
            query = "SELECT booking_id, pickup_location, dropoff_location, pickup_time, pickup_date FROM customers_order "
            mycursor.execute(query)
            booking_details = mycursor.fetchall()
            con.close()
            return booking_details
        except pymysql.Error as e:
            messagebox.showerror("Error", f"Database connectivity problem: {e}")
            return []
    
    def delete_booking(self):
        try:
            self.db = mysql.connector.connect(
                host='localhost',
                port=3306,
                user='root',
                password='Devil_B0y',
                database='taxi_booking'
            )
            self.cursor = self.db.cursor()

            query = "DELETE FROM customers_order WHERE booking_id = %s"
        
            selected_item = self.booking_tree.selection()
            if selected_item:
                booking_id = self.booking_tree.item(selected_item, 'values')[0]

                self.cursor.execute(query, (booking_id,))
                self.db.commit()
                messagebox.showinfo("Success", "Item deleted successfully.")
                # Update the display after deletion if needed
                # self.show_booking()
                self.refresh_display()
            else:
                messagebox.showwarning("Warning", "Please select an item to delete.")

        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Database error: {e}")

        finally:
        # Close the database connection
            if self.db.is_connected():
                self.cursor.close()
                self.db.close()

    def refresh_display(self):
        # Fetch the updated data from the database and update the Treeview
        booking_details = self.booking_details()
        self.booking_tree.delete(*self.booking_tree.get_children())  # Clear existing items in Treeview

        for bookings in booking_details:
            self.booking_tree.insert("", "end", values=bookings)


if __name__ == "__main__":
    db_manager = DatabaseManager("localhost", 3306, "root", "Devil_B0y", "taxi_booking")
    root = tk.Tk()

    # Replace 'replace_with_logged_in_username' with the actual logged-in username
    logged_in_username = 'replace_with_logged_in_username'

    cu = Customerpage(root, db_manager, logged_in_username)
    print("Customerpage created")
    root.mainloop()