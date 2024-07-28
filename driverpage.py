from tkinter import *
from regandlog import LoginForm
import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import pymysql

def logout(root):
    root.destroy()
    login_root = Tk()
    LoginForm(login_root, root)

class Driverpage:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1000x500")
        self.root.title('Driver Page')
        self.root.config(bg='yellow')
        self.driver()
        


    def driver(self):
        self.frame=Frame(self.root,bg='white',bd=3,relief='ridge').place(x=290,y=90,width=660,height=300)
        self.frame1=Frame(self.root,bg='yellow',bd=3).place(x=20,y=90,width=220,height=300)
        self.completebutton=Button(self.frame1,text="Complete Taxi Order",font=('Microsoft YaHei UI light', 15, 'bold'),cursor='hand2', command=self.delete_booking).place(x=30,y=120,width=250,height=50)
        self.logoutbutton=Button(self.frame1,text='Log Out',font=('Microsoft YaHei UI light', 15, 'bold'),cursor='hand2',command=lambda:logout(self.root)).place(x=30,y=190,width=250,height=50)
        self.exitbutton=Button(self.frame1,text='EXIT',font=('Microsoft YaHei UI light', 15, 'bold'),command=quit,cursor='hand2').place(x=30,y=260,width=250,height=50)
        self.show_booking()


    def show_booking(self):
        self.booking_tree = ttk.Treeview(self.frame, columns=("ID", "pickup_location", "dropoff_location", "pickup_time", "pickup_date", "customer_id"), show="headings", height=10)

        # Add headings to the Treeview
        self.booking_tree.heading("ID", text="ID")
        self.booking_tree.heading("pickup_location", text="pickup_location")
        self.booking_tree.heading("dropoff_location", text="dropoff_location")
        self.booking_tree.heading("pickup_time", text="pickup_time")
        self.booking_tree.heading("pickup_date", text="pickup_date")
        self.booking_tree.heading("customer_id", text="customer_id")
       

        # Set column widths
        self.booking_tree.column("ID", width=50, anchor="center")
        self.booking_tree.column("pickup_location", width=100, anchor="center")
        self.booking_tree.column("dropoff_location", width=100, anchor="center")
        self.booking_tree.column("pickup_time", width=50, anchor="center")
        self.booking_tree.column("pickup_date", width=100, anchor="center")
        self.booking_tree.column("customer_id", width=100, anchor="center")
        
        booking_details = self.booking_details()
        for bookings in booking_details:
            self.booking_tree.insert("", "end", values=bookings)
        

        self.booking_tree.place(x=290,y=90,width=660,height=300)

    def booking_details(self):
        try:
            con = pymysql.connect(host="localhost", user="root", password="Devil_B0y")
            mycursor = con.cursor()
            mycursor.execute('use taxi_booking')
            query = f"SELECT booking_id, pickup_location, dropoff_location, pickup_time, pickup_date, customer_id FROM customers_order"
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
                messagebox.showinfo("Success", "Ride Completed.")
                
                self.refresh_display()
            else:
                messagebox.showwarning("Warning", "No orders selected.")

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

if __name__=="__main__":
    root=Tk()
    dr=Driverpage(root)
    root.mainloop()