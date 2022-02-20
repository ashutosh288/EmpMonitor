from tkinter import *
from PIL import ImageTk
from tkinter import ttk, messagebox
import mysql.connector
from werkzeug.security import generate_password_hash
#from dashboard import Dashborad

class NewPasswd:
    def __init__(self, win, AdminID):
        self.win = win
        self.win.geometry("370x340")
        self.win.title("New Password")
        self.win.configure(bg="#7ebaef")
        self.win.focus_force()

        self.AdminID = AdminID

        self.pswd = StringVar()
        self.cnf_pswd = StringVar()

        tittle_label = Label(self.win, background="#7ebaef", text="New Password", font=('Calibari',12, 'bold'))
        tittle_label.place(x=10, y=10)

        paswd_label = Label(self.win,font=('Calibari',10), text="New Password",bg="#7ebaef").place(x=20,y=60,height=20)
        paswd_entry = Entry(self.win,font=('Calibari',10),bg="#fffff0", textvariable=self.pswd).place(x=170,y=60,width=170,height=20)

        cnf_pswd_label = Label(self.win,font=('Calibari',10), text="Confirm New Password",bg="#7ebaef").place(x=20,y=100,height=20)
        cnf_pswd_entry = Entry(self.win,font=('Calibari',10),bg="#fffff0", textvariable=self.cnf_pswd).place(x=170,y=100,width=170,height=20)

        submit_btn = Button(self.win, text="Update", font=('Cilibari', 10),bg="#dc3545", fg="#ffffff", command=self.update_pswd).place(x=130,y=160,height=25,width=120)
        
        self.win.mainloop()

    def dashboard_win(self):
        new_obj = Toplevel(self.win)
        new_win = Dashborad(new_obj)

    #========================================================================================================================================#
    # functions

    def update_pswd(self):
        try:
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="root",
                database="empmangsys"
            )
            mycursor = mydb.cursor()
            
            if self.pswd.get() == "" or self.cnf_pswd.get() == "":
                messagebox.showerror("Error", "Fill All Required Details", parent=self.win)
                return
            
            password_length = len(self.pswd.get())

            if password_length < 6 or password_length > 12:
                messagebox.showerror("Error", "Password Must Have 6 to 12 Characters", parent=self.win)
                print(self.pswd.get())
                return
            
            elif '@' not in str(self.pswd.get()) and '#' not in str(self.pswd.get()) and '$' not in str(self.pswd.get()) and '&' not in str(self.pswd.get()) and '^' not in str(self.pswd.get()) and "!" not in str(self.pswd.get()) and "_" not in str(self.pswd.get()):
                messagebox.showerror("Error", "Password Must Contain One Special Character from ( @,#,$,&,^,!,_ )", parent=self.win)
                print(self.pswd.get())
                return

            else:
                if self.pswd.get() == self.cnf_pswd.get():
                    encrypt_passwd = generate_password_hash(str(self.pswd.get()), method='md5')
                    print(encrypt_passwd)

                    # Updating Admin Details

                    query = "UPDATE admin SET Password=%s WHERE ADMINID = %s;" 
                    vals = (encrypt_passwd, self.AdminID,)

                    mycursor.execute(query, vals)
                    mydb.commit()

                    messagebox.showinfo("Succes", "Password Changed Successfully!", parent=self.win)
                else:
                    messagebox.showerror("Error", "Password & Confirm Password Value does not matched!", parent=self.win)

        except Exception as ex:
            messagebox.showerror("Error", f"An Error Occured {ex}. Please Try Again!", parent=self.win)