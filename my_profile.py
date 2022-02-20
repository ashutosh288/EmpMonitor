from tkinter import *
from PIL import ImageTk
from tkinter import messagebox
import mysql.connector

class MyProfile:
    def __init__(self, win, admin_vals):
        self.win = win
        self.win.geometry("370x450")
        self.win.title("My Profile")
        self.win.configure(bg="#7ebaef")
        self.win.focus_force()

        self.admin_vals = admin_vals

        self.adminid = IntVar()
        self.name = StringVar()
        self.mail = StringVar()
        self.gender = StringVar()
        self.mobile = StringVar()
        self.username = StringVar()

        self.adminid.set(self.admin_vals[0])
        self.name.set(self.admin_vals[1])
        self.mail.set(self.admin_vals[3])
        self.gender.set(self.admin_vals[2])
        self.mobile.set(self.admin_vals[4])
        self.username.set(self.admin_vals[5])

        tittle_label = Label(self.win, background="#7ebaef", text="My Profile", font=('Calibari',12, 'bold'))
        tittle_label.place(x=10, y=10)

        adminID_label = Label(self.win,font=('Calibari',10), text="Admin ID",bg="#7ebaef").place(x=35,y=60,height=20)
        adminID_entry = Entry(self.win,font=('Calibari',10),bg="#fffff0", textvariable=self.adminid).place(x=120,y=60,width=200,height=20)

        name_label = Label(self.win,font=('Calibari',10), text="Name",bg="#7ebaef").place(x=35,y=100,height=20)
        name_entry = Entry(self.win,font=('Calibari',10),bg="#fffff0", textvariable=self.name).place(x=120,y=100,width=200,height=20)

        email_label = Label(self.win,font=('Calibari',10), text="Email",bg="#7ebaef").place(x=35,y=140,height=20)
        email_entry = Entry(self.win,font=('Calibari',10),bg="#fffff0", textvariable=self.mail).place(x=120,y=140,width=200,height=20)

        gender_label = Label(self.win,font=('Calibari',10), text="Gender",bg="#7ebaef").place(x=35,y=180,height=20)
        gender_entry = Entry(self.win,font=('Calibari',10),bg="#fffff0", textvariable=self.gender).place(x=120,y=180,width=200,height=20)

        mobile_label = Label(self.win,font=('Calibari',10), text="Mobile No.\n(include +91)",bg="#7ebaef").place(x=30,y=220,height=40)
        mobile_entry = Entry(self.win,font=('Calibari',10),bg="#fffff0", textvariable=self.mobile).place(x=120,y=220,width=200,height=20)

        username_label = Label(self.win,font=('Calibari',10), text="Username",bg="#7ebaef").place(x=35,y=270,height=20)
        username_entry = Entry(self.win,font=('Calibari',10),bg="#fffff0", textvariable=self.username).place(x=120,y=270,width=200,height=20)

        self.submit_btn = Button(self.win, text="Update", font=('Cilibari', 10), bg="#0d6efd", command=self.UpdateAdmin).place(x=120,y=320,height=25,width=90)
        
        self.win.mainloop()

    #========================================================================================================================================#
    # functions
    
    def UpdateAdmin(self):
        try:
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="root",
                database="empmangsys"
            )
            mycursor = mydb.cursor()

            if self.adminid.get() == "" or self.name.get() == "" or self.mail.get() == "" or self.gender.get() == "" or self.mobile.get() == "" or self.username.get() == "":
                messagebox.showerror("Error", "Fill All Required Details", parent=self.win)
            else:
                query = "SELECT * FROM admin WHERE ADMINID = %s;"
                value = (self.adminid.get(),)

                mycursor.execute(query, value)
                row = mycursor.fetchone()
                
                if row == None:
                    messagebox.showerror("Error", "Invalid Admin ID! Please Check and Try Again", parent=self.win)
                    return

                query = "UPDATE admin SET ADMINID = %s, Name = %s, Gender = %s, Email = %s, Mobile = %s, Username = %s"
                vals = (self.adminid.get() ,self.name.get(), self.gender.get(), self.mail.get(), self.mobile.get(), self.username.get(),)

                mycursor.execute(query, vals)
                mydb.commit()

                messagebox.showinfo("Done", "Admin Data Updated Successfully", parent=self.win)

        except Exception as Ex:
            messagebox.showerror("Error", str(Ex), parent=self.win)

if __name__ == '__main__':
    root = Tk()
    new_win = MyProfile(root)