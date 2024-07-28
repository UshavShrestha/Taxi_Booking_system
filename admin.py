from tkinter import *
from tkinter import ttk, messagebox
import pymysql
import mysql.connector


class Adminpage:
    def __init__(self, root):
        self.root = root
        self.root.title("Admin Page")
        self.root.geometry("1200x750+50+50")
        self.root.resizable(0, 0)
        self.root.config(bg="yellow")
        self.adminform()
        self.selected_driver_id = StringVar()
        self.driver_combobox = None
        self.display_orders()

    def adminform(self):
        Label(self.root,text='*Only for Admin',fg='red',bg='yellow',font=('bold',60)).pack()
        frame1 = Frame(self.root, bg='yellow')

        Booking_btn = Button(frame1, text="Customers' Order", font=('bold', 15), fg="black", bd=0, bg="yellow", cursor="hand2", command=self.display_orders)
        Booking_btn.place(x=25, y=100)

        customer_details_btn = Button(frame1, text="Customers Details", font=('bold', 15), fg="black", bd=0, bg="yellow", cursor="hand2", command=self.customer_details)
        customer_details_btn.place(x=25, y=170)

        driver_details_btn = Button(frame1, text="Drivers Details", font=('bold', 15), fg="black", bd=0, bg="yellow", cursor="hand2", command=self.get_driver_details)
        driver_details_btn.place(x=25, y=240)

        logout_btn = Button(frame1, text="Logout", font=('bold', 15), fg="black", bd=0, bg="yellow", cursor="hand2",command=self.logout)
        logout_btn.place(x=25, y=310)

        exit_btn = Button(frame1, text="Exit", font=('bold', 15), fg="black", bd=0, bg="yellow", cursor="hand2",command=quit)
        exit_btn.place(x=25, y=380)

        frame1.pack(side=LEFT)
        frame1.configure(width=200, height=500)

        self.frame2 = Frame(self.root, highlightbackground="black", highlightthickness=2)
        self.frame2.pack(side=LEFT)
        self.frame2.pack_propagate(False)
        self.frame2.configure(height=500, width=880)

    def logout(self):
        self.root.destroy()
        from regandlog import LoginForm
        login_root = Tk()
        
        LoginForm(login_root, root)

    def display_orders(self):
        for widget in self.frame2.winfo_children():
            widget.destroy()

        driver_ids = [str(driver[0]) for driver in self.collect_driver_info()]

        # Destroy the combobox if it already exists
        if self.driver_combobox:
            self.driver_combobox.destroy()

        # Create or update the combobox
        self.driver_combobox = ttk.Combobox(self.frame2, textvariable=self.selected_driver_id, values=[], state="readonly")
        self.driver_combobox.set("Select Driver ID")
        self.driver_combobox.pack(side=TOP, pady=10)

        # Bind an event to the combobox selection (optional)
        # self.driver_combobox.bind("<<ComboboxSelected>>", lambda event: self.get_driver_details())
        


        # Use self.driver_combobox here
        self.driver_combobox['values'] = driver_ids
        self.driver_combobox.set("Select Driver ID")

        self.selected_driver_label = Label(self.frame2, text="", font=('bold', 15))
        self.selected_driver_label.pack(pady=10)

        # Create a Treeview widget for displaying booking details in a table
        self.booking_tree = ttk.Treeview(self.frame2, columns=("ID", "pickup_location", "dropoff_location", "pickup_time", "pickup_date", "customer_id", "driver_id"), show="headings", height=10)

        # Add headings to the Treeview
        self.booking_tree.heading("ID", text="ID")
        self.booking_tree.heading("pickup_location", text="pickup_location")
        self.booking_tree.heading("dropoff_location", text="dropoff_location")
        self.booking_tree.heading("pickup_time", text="pickup_time")
        self.booking_tree.heading("pickup_date", text="pickup_date")
        self.booking_tree.heading('customer_id', text='customer_id')
        self.booking_tree.heading('driver_id', text='driver_id')

        # Set column widths
        self.booking_tree.column("ID", width=100, anchor="center")
        self.booking_tree.column("pickup_location", width=150, anchor="center")
        self.booking_tree.column("dropoff_location", width=150, anchor="center")
        self.booking_tree.column("pickup_time", width=100, anchor="center")
        self.booking_tree.column("pickup_date", width=100, anchor="center")
        self.booking_tree.column("customer_id", width=100, anchor="center")
        self.booking_tree.column("driver_id", width=100, anchor="center")

        self.fn1()

        self.booking_tree.pack(side=TOP, expand=YES, fill=BOTH)
        home_page_button = Button(self.frame2, text="Assign Driver", font=('bold', 15), fg="black", bd=0, bg="white", cursor="hand2", command=self.home_page_button_click)
        home_page_button.pack(pady=10)

    def home_page_button_click(self):
        selected_driver_id = self.selected_driver_id.get()
        if not selected_driver_id or selected_driver_id == "Select Driver ID":
            messagebox.showerror("Information", "Please select a driver ID.")
            return
    
        self.assign_driver(selected_driver_id)

   

    def assign_driver(self,driver_id):
        selected_item = self.booking_tree.selection()
        selected_id = self.booking_tree.item(selected_item, "values")[0]
        print(selected_id, driver_id)
        if selected_id:
            self.update_driver(selected_id , driver_id)
            messagebox.showinfo('Sucess','Sucessfully Assigned Driver')
            
        else:
            messagebox.showerror('Error','Select a driver')
  
        
    def fn1(self):
        booking_details = self.booking_details()
        for bookings in booking_details:
            self.booking_tree.insert("", "end", values=bookings)

    def booking_details(self):
        
        try:
            con = pymysql.connect(host="localhost", user="root", password="Devil_B0y")
            mycursor = con.cursor()
            mycursor.execute('use taxi_booking')
            query = "SELECT booking_id, pickup_location, dropoff_location, pickup_time, pickup_date, customer_id, driver_id FROM customers_order"
            mycursor.execute(query)
            booking_details = mycursor.fetchall()
            con.close()
            return booking_details
        except pymysql.Error as e:
            messagebox.showerror("Error", f"Database connectivity problem: {e}")
            return []
        

    def update_driver(self,booking_id,driver_id):
        self.db = mysql.connector.connect(
            host='localhost',
            port=3306,
            user='root',
            password='Devil_B0y',
            database='taxi_booking'
            )
        self.cursor = self.db.cursor()
        query='UPDATE customers_order SET driver_id=%s WHERE booking_id=%s'
        value=(driver_id,booking_id)
        self.cursor.execute(query,value)
        self.db.commit()
        self.cursor.close()
        self.display_orders()


    def get_driver_details(self):
        for widget in self.frame2.winfo_children():
            widget.destroy()

        tree = ttk.Treeview(self.frame2, columns=("ID", "Name", "License Plate"), show="headings", height=20)

        tree.heading("ID", text="ID")
        tree.heading("Name", text="Name")
        tree.heading("License Plate", text="License Plate")

        tree.column("ID", width=100, anchor="center")
        tree.column("Name", width=300, anchor="center")
        tree.column("License Plate", width=200, anchor="center")

        registered_driver_details = self.collect_driver_info()

        for driver in registered_driver_details:
            tree.insert("", "end", values=driver)

        tree.pack(expand=YES, fill=BOTH)

    def collect_driver_info(self, driver_id=None):
        try:
            con = pymysql.connect(host="localhost", user="root", password="Devil_B0y")
            mycursor = con.cursor()
            mycursor.execute('use taxi_booking')

            if driver_id:
                query = f"SELECT id, name, license_number FROM drivers WHERE id = {driver_id}"
            else:
                query = "SELECT id, name, license_number FROM drivers"

            mycursor.execute(query)
            registered_driver_details = mycursor.fetchall()
            con.close()
            return registered_driver_details
        except pymysql.Error as e:
            messagebox.showerror("Error", f"Database connectivity problem: {e}")
            return []

    

    def customer_details(self):
        for widget in self.frame2.winfo_children():
            widget.destroy()
        tree = ttk.Treeview(self.frame2, columns=("ID", "Name", "phone", "payment_method", "email"), show="headings", height=20)

        tree.heading("ID", text="ID", anchor="center")
        tree.heading("Name", text="Name", anchor="center")
        tree.heading("phone", text="phone", anchor="center")
        tree.heading("payment_method", text="payment_method", anchor="center")
        tree.heading("email", text="email", anchor="center")

        tree.column("ID", width=50, anchor="center")
        tree.column("Name", width=100, anchor="center")
        tree.column("phone", width=80, anchor="center")
        tree.column("payment_method", width=120, anchor="center")
        tree.column("email", width=100, anchor="center")

        registered_customer_details = self.fetch_registered_customer_details()

        for customer in registered_customer_details:
            tree.insert("", "end", values=customer)

        tree.pack(expand=YES, fill=BOTH)

    def fetch_registered_customer_details(self):
        try:
            con = pymysql.connect(host="localhost", user="root", password="Devil_B0y")
            mycursor = con.cursor()
            mycursor.execute('use taxi_booking')
            query = "SELECT customer_id, name, phone, payment_method, email FROM customers"
            mycursor.execute(query)
            registered_customer_details = mycursor.fetchall()
            con.close()
            return registered_customer_details
        except pymysql.Error as e:
            messagebox.showerror("Error", f"Database not connected: {e}")
            return []

if __name__ == "__main__":
    root = Tk()
    ad = Adminpage(root)
    root.mainloop()