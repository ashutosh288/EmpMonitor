from tkinter import *
from PIL import ImageTk
from tkinter import ttk, messagebox
import mysql.connector
from werkzeug.security import generate_password_hash

class AdminRegistration:
    def __init__(self, win):
        self.win = win
        self.win.geometry("540x500+380+120")
        self.win.title("Add Registration")
        self.win.configure(bg="#ffffff")
        self.win.focus_force()

        self.adminid = IntVar()
        self.name = StringVar()
        self.gender = StringVar()
        self.mail = StringVar()
        self.phone = StringVar()
        
        self.username = StringVar()
        self.password = StringVar()
        self.conf_password = StringVar()

        title = Label(self.win,text="Admin Registration", font=('Calibari',11),fg="#ffffff",bg='#0d6efd').place(x=0,y=0,height=30,width=540)

        #Personal Details Form
        prsnl_detail_frame = LabelFrame(self.win, text="Personal Details",font=('Calibari',10),bg="#ffffff")
        prsnl_detail_frame.place(x=20,y=50,width=500,height=150)

        admin_id_label = Label(prsnl_detail_frame,font=('Calibari',10), text="Admin ID*",bg="#ffffff").place(x=10,y=20,height=20)
        admin_id_entry = Entry(prsnl_detail_frame,textvariable=self.adminid ,font=('Calibari',10),bg="#fffff0").place(x=85,y=20,width=100,height=20)

        name_label = Label(prsnl_detail_frame,font=('Calibari',10), text="Name*",bg="#ffffff").place(x=205,y=20,height=20)
        name_entry = Entry(prsnl_detail_frame,textvariable=self.name ,font=('Calibari',10),bg="#fffff0").place(x=255,y=20,width=225,height=20)

        gender_label = Label(prsnl_detail_frame,font=('Calibari',10), text="Gender*",bg="#ffffff").place(x=10,y=55,height=20)
        gender_entry = Entry(prsnl_detail_frame,textvariable=self.gender ,font=('Calibari',10),bg="#fffff0").place(x=85,y=55,width=100,height=20)

        email_label = Label(prsnl_detail_frame,font=('Calibari',10), text="Email*",bg="#ffffff").place(x=205,y=55,height=20)
        email_entry = Entry(prsnl_detail_frame,textvariable=self.mail ,font=('Calibari',10),bg="#fffff0").place(x=255,y=55,width=225,height=20)

        phone_label = Label(prsnl_detail_frame,font=('Calibari',10), text="Mobile No.(add +91)*",bg="#ffffff").place(x=10,y=90,height=20)
        pnone_entry = Entry(prsnl_detail_frame,textvariable=self.phone ,font=('Calibari',10),bg="#fffff0").place(x=140,y=90,width=140,height=20)

        #Comapany Details Form
        login_detail_frame = LabelFrame(self.win, text="Login Details",font=('Calibari',10),bg="#ffffff")
        login_detail_frame.place(x=20,y=220,width=500,height=150)

        username_label = Label(login_detail_frame,font=('Calibari',10), text="Username*",bg="#ffffff").place(x=10,y=20,height=20)
        username_entry = Entry(login_detail_frame,textvariable=self.username,font=('Calibari',10),bg="#fffff0").place(x=85,y=20,width=160,height=20)

        password_label = Label(login_detail_frame,font=('Calibari',10), text="Password*",bg="#ffffff").place(x=250,y=20,height=20)
        password_entry = Entry(login_detail_frame,textvariable=self.password,font=('Calibari',10),bg="#fffff0").place(x=320,y=20,width=160,height=20)

        confirm_pswd_label = Label(login_detail_frame,font=('Calibari',10), text="Confirm Password*",bg="#ffffff").place(x=10,y=55,height=20)
        confirm_pswd_entry = Entry(login_detail_frame,textvariable=self.conf_password,font=('Calibari',10),bg="#fffff0").place(x=130,y=55,width=160,height=20)


        submit_btn = Button(self.win, text="Register", font=('Cilibari', 10),bg="#0d6efd", command=self.validate_then_save).place(x=210,y=390,height=30,width=120)
        
        self.win.mainloop()
    #=========================================================================================================#
    #functions

    def validate_then_save(self):
        try:
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="root",
                database="empmangsys"
            )
            mycursor = mydb.cursor()
            if self.adminid.get() == "" or self.name.get() == "" or self.gender.get() == "" or self.mail.get() == "" or self.phone.get() == "" or self.username.get() == "" or self.password.get() == "" or self.conf_password.get() == "":
                messagebox.showerror("Error", "Fill All Required Details", parent=self.win)
                return

            else:
                query = "SELECT * FROM admin WHERE ADMINID = %s;"
                value = (self.adminid.get(),)

                mycursor.execute(query, value)
                row = mycursor.fetchone()

                if row != None:
                    messagebox.showerror("Error", "This Admin ID Already Exists! Please Check and Try Again.", parent=self.win)
                    return

            username_length = len(self.username.get())

            if username_length < 6 or username_length > 8:
                messagebox.showerror("Error", "Username Must Have 6 to 8 Characters", parent=self.win)
                return
            
            elif '@' in str(self.username.get()) or '#' in str(self.username.get()) or '$' in str(self.username.get()) or '&' in str(self.username.get()) or '^' in str(self.username.get()) or "'" in str(self.username.get()) or '"' in str(self.username.get()) or "," in str(self.username.get()) or '.' in str(self.username.get()) or ':' in str(self.username.get()) or '!' in str(self.username.get()) or '_' in str(self.username.get()) or '-' in str(self.username.get()):
                messagebox.showerror("Error", "Username Must Not Contain Any Special Character", parent=self.win)
                return

            else:
                query = "SELECT * FROM admin WHERE Username = %s;"
                value = (self.username.get(),)

                mycursor.execute(query, value)
                existUser = mycursor.fetchone()

                if existUser != None:
                    messagebox.showerror("Error", "This Username Already Exists! Please Enter Another", parent=self.win)
                    return
            
            password_length = len(self.password.get())

            if password_length < 6 or password_length > 12:
                messagebox.showerror("Error", "Password Must Have 6 to 12 Characters", parent=self.win)
                print(self.password.get())
                return
            
            elif '@' not in str(self.password.get()) and '#' not in str(self.password.get()) and '$' not in str(self.password.get()) and '&' not in str(self.password.get()) and '^' not in str(self.password.get()) and "!" not in str(self.password.get()) and "_" not in str(self.password.get()):
                messagebox.showerror("Error", "Password Must Contain One Special Character from ( @,#,$,&,^,!,_ )", parent=self.win)
                print(self.password.get())
                return

            # elif '"' in str(self.password.get()) or "'" in str(self.password.get()) or ',' in str(self.password.get()) or ':' in str(self.password.get()) or ';' in str(self.password.get()) or '<' in str(self.password.get()) or '>' in str(self.password.get()):
            #     messagebox.showerror("Error", "Password Must Not Contain Special Character other than ( @,#,$,&,^,!,_ )", parent=self.win)
            #     return

            else:
                if self.conf_password.get() == self.password.get():
                    encrypt_passwd = generate_password_hash(str(self.password.get()), method='md5')
                    print(encrypt_passwd)

                    # Saving Admin Details

                    # INSERT INTO admin (ADMINID, Name, Gender, Email, Mobile, Username, Password) VALUES (01, 'Abhay Verma', 'Male', 'hr.abcpvtltd@gmail.com', '+915689742365', 'abhay_25', 'abhay.HR');

                    query = "INSERT INTO admin (ADMINID, Name, Gender, Email, Mobile, Username, Password) VALUES (%s,%s,%s,%s,%s,%s,%s);" 
                    vals = (self.adminid.get(), self.name.get(), self.gender.get(), self.mail.get(), self.phone.get(), self.username.get(), encrypt_passwd,)

                    mycursor.execute(query, vals)
                    mydb.commit()

                    messagebox.showinfo("Succes", "Admin Registered Successfully!", parent=self.win)
                else:
                    messagebox.showerror("Error", "Password & Confirm Password Value does not matched!", parent=self.win)

        except Exception as ex:
            print(ex)

if __name__ == "__main__":
    root=Tk()
    new_win = AdminRegistration(root)