from tkinter import *
from PIL import ImageTk
from tkinter import ttk, messagebox
import random
import os
import mysql.connector
from twilio.rest import Client
from werkzeug.security import check_password_hash
from new_pswd import NewPasswd

class ChangePasswd:
    def __init__(self, win):
        self.win = win
        self.win.geometry("350x400")
        self.win.title("Change Password")
        self.win.configure(bg="#7ebaef")
        self.win.focus_force()

        self.adminID = 0

        # Twilio Account System
        account_sid = os.environ["TWILIO_ACC_SID"]
        auth_token = os.environ["TWILIO_AUTH_TOKEN"]
        
        self.client = Client(account_sid, auth_token)

        self.username = StringVar()
        self.password = StringVar()

        self.otp = IntVar()

        tittle_label = Label(self.win, background="#7ebaef", text="Change Password", font=('Calibari',12, 'bold'))
        tittle_label.place(x=10, y=10)

        username_label = Label(self.win,font=('Calibari',10), text="Username",bg="#7ebaef").place(x=50,y=60,height=20)
        username_entry = Entry(self.win,font=('Calibari',10),bg="#fffff0", textvariable=self.username).place(x=120,y=60,width=170,height=20)

        password_label = Label(self.win,font=('Calibari',10), text="Password",bg="#7ebaef").place(x=50,y=90,height=20)
        password_entry = Entry(self.win,font=('Calibari',10),bg="#fffff0", textvariable=self.password).place(x=120,y=90,width=170,height=20)

        get_OTP_btn = Button(self.win, text="Get OTP", font=('Cilibari', 10),bg="#dc3545", fg="#ffffff", command=self.validate_user).place(x=215,y=120,height=25,width=75)

        self.otp_msg_label = Label(self.win, text="A 4-Digit OTP is sent to your registered\nMobile no.", font=('Cilibari', 10,),bg="#7ebaef",  border=0)
        #self.otp_msg_label.place(x=50, y=160)

        self.otp_label = Label(self.win,font=('Calibari',10), text="OTP",bg="#7ebaef")
        #self.otp_label.place(x=50,y=210,height=20)

        self.otp_entry = Entry(self.win,font=('Calibari',10),bg="#fffff0", textvariable=self.otp)
        #self.otp_entry.place(x=120,y=210,width=170,height=20)

        self.submit_btn = Button(self.win, text="Submit", font=('Cilibari', 10), bg="#0d6efd", command=self.check_otp)
        #self.submit_btn.place(x=120,y=250,height=25,width=90)

        self.resend_btn = Button(self.win, text="Resend OTP", font=('Cilibari', 10), bg="#ffc107", command=self.resend_otp)
        
        self.win.mainloop()

    def new_pswd_win(self, admin_id):
        adminID = admin_id
        new_obj = Toplevel(self.win)
        new_win = NewPasswd(new_obj, adminID)

    #==========================================================================================================================================================#
    # functions

    def send_otp(self, mobile_no):
        self.otp_val = random.randint(1000, 9999)
        self.mobile_no = mobile_no

        print(self.otp_val)

        msg = "Your OTP for Change Password is " + str(self.otp_val)
        
        body = "Message: " + str(msg)

        self.client.messages.create(
            to= self.mobile_no,
            from_= os.environ["TWILIO_PHONE_NUM"],
            body= body
        )
        print('OTP Sent')

    def validate_user(self):
        try:
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="root",
                database="empmangsys"
            )
        
            mycursor = mydb.cursor()
            
            if self.username.get() == "" or self.password.get() == "":
                messagebox.showerror('Error', 'Fill All Entries', parent=self.win)

            else:
                query = "SELECT ADMINID, Mobile, Password FROM admin WHERE Username = %s;"
                value = (self.username.get(),)

                mycursor.execute(query, value)
                user = mycursor.fetchone()

                if user != None:
                    self.adminID = user[0]
                    mobile_num = user[1]
                    psswd = user[2]
        
                    print(mobile_num, psswd)

                    if check_password_hash(psswd, self.password.get()):
                        self.send_otp(mobile_num)

                        self.otp_msg_label.place(x=50, y=160)
                        self.otp_label.place(x=50,y=210,height=20)
                        self.otp_entry.place(x=120,y=210,width=170,height=20)
                        self.submit_btn.place(x=120,y=250,height=25,width=90)
                        self.resend_btn.place(x=120,y=290,height=25,width=90)
                    else:
                        messagebox.showerror('Error', 'Password Does not Matched', parent=self.win)
                else:
                    messagebox.showerror('Error', 'Invalid Username or Password. Please Check and try again', parent=self.win)
        
        except Exception as ex:
            messagebox.showerror('Error', f'Error Occured Due To {ex}', parent=self.win)

    def resend_otp(self):
        self.otp_val = random.randint(1000, 9999)
        msg = "Your OTP for Change Password is" + str(self.otp_val)

        print(self.otp_val)

        msg = "Your OTP for Change Password is " + str(self.otp_val)
        
        body = "Message: " + str(msg)

        self.client.messages.create(
            to= self.mobile_no,
            from_= os.environ["TWILIO_PHONE_NUM"],
            body= body
        )
        print('OTP Sent')

    def check_otp(self):
        try:
            if len(str(self.otp.get())) != 4:
                messagebox.showerror('Error', 'OTP Must Have Only 4 Characters', parent=self.win)
                return
            else:
                if self.otp_val == self.otp.get():
                    print(self.otp.get())
                    self.new_pswd_win(self.adminID)
                else:
                    messagebox.showerror('Error', 'Wrong OTP. Please Check Again', parent=self.win)

        except Exception:
            messagebox.showerror('Error', 'Invalid OTP. Please Check Again', parent=self.win)

if __name__ == '__main__':
    root = Tk()
    new_win = ChangePasswd(root)