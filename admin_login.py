from tkinter import *
from tkinter import ttk, messagebox
from PIL import ImageTk
import mysql.connector
from werkzeug.security import check_password_hash
from admin_registration import AdminRegistration
from dashboard import Dashborad

class AdminLogin:
    def __init__(self, win):
        self.win = win
        self.win.geometry("1000x600")
        self.win.title("Admin Login")
        self.win.configure(bg="#ffffff")

        self.username = StringVar()
        self.password = StringVar()

        bg_img = ImageTk.PhotoImage(file="Images/bg-2.png")
        background = Label(self.win, image=bg_img).place(relwidth=1,relheight=1)

        login_frame = Frame(self.win,border=2, background="#7ebaef")
        login_frame.place(x=70, y=180, width=350, height=360)
        
        login_logo = ImageTk.PhotoImage(file="Images/login.png")
        login_label = Label(login_frame, image=login_logo, background="#7ebaef")
        login_label.place(x=147, y=10)

        tittle_label = Label(login_frame, background="#7ebaef", text="Admin Login", font=('Calibari',14))
        tittle_label.place(x=120, y=80)

        username_label = Label(login_frame,font=('Calibari',10), text="Username",bg="#7ebaef").place(x=50,y=127,height=20)
        username_entry = Entry(login_frame,font=('Calibari',10),bg="#fffff0", textvariable=self.username).place(x=120,y=127,width=170,height=20)

        password_label = Label(login_frame,font=('Calibari',10), text="Password",bg="#7ebaef").place(x=50,y=165,height=20)
        password_entry = Entry(login_frame,font=('Calibari',10),bg="#fffff0", textvariable=self.password).place(x=120,y=165,width=170,height=20)

        create_acc_btn = Button(login_frame, text="Not a User! Create Account", font=('Cilibari', 10,),bg="#7ebaef",  border=0, anchor=W, command=self.register_admin)
        create_acc_btn.place(x=50, y=203, width=170)

        login_btn = Button(login_frame, text="Login", font=('Cilibari', 10),bg="#dc3545", fg="#ffffff", command=self.login_admin).place(x=130,y=250,height=25,width=90)

        self.win.mainloop()

    def register_admin(self):
        new_obj = Toplevel(self.win)
        new_win = AdminRegistration(new_obj)

    def admin_dashboard(self, vals_list):
        values = vals_list
        new_obj = Toplevel(self.win)
        new_win = Dashborad(new_obj, values)

    #==================================================================================================================================================================#
    # fuctions

    def login_admin(self):
        try:
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="root",
                database="empmangsys"
            )
            mycursor = mydb.cursor()

            if self.username.get() == "" or self.password.get() == "":
                messagebox.showerror('Error', 'Username or Password Must Be Filled!', parent=self.win)
                return

            query = "SELECT ADMINID, Name, Password FROM admin WHERE Username = %s;"
            value = (self.username.get(),)

            mycursor.execute(query, value)
            user = mycursor.fetchone()

            if user != None:
                print(user)
                pwhashed = user[2]

                vals_list = {
                    'adminID' : user[0],
                    'Name' : user[1]
                }

                if check_password_hash(pwhashed, self.password.get()):
                    self.admin_dashboard(vals_list)
                else:
                    messagebox.showerror('Error', 'Password Does not Matched', parent=self.win)
            else:
                messagebox.showerror('Error', 'Username Does not Exist!', parent=self.win)

        except Exception as ex:
            print(ex)
                
if __name__ == '__main__':
    root = Tk()
    new_win = AdminLogin(root)