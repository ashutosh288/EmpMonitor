from tkinter import *
from tkinter import ttk, messagebox
from PIL import ImageTk
import datetime
import os
import mysql.connector
from emp_section import EmpSection
from payroll_list import EmpPayroll
from send_notice import SendNotice
from change_pswd import ChangePasswd
from my_profile import MyProfile
from edit_dept import UpdateDepts
from add_depts import AddDepts

class Dashborad:
    def __init__(self, win, vals):
        self.win = win
        self.win.geometry("1000x600")
        self.win.title("Employee Management System")
        self.win.configure(bg="#ffffff")
        self.win.focus_force()

        self.vals = vals

        self.win.bind('<FocusIn>', self.refresh)

        title_bar=Label(self.win,anchor=W,text="Employee Management System",fg="#ffffff",bg='#0d6efd',font=('Calibari',11),padx=5).place(x=0,y=0,relwidth=1,height=35)

        dashboard=Label(self.win,text="Dashbaord",font=('Calibari',15, 'bold'),bg="#ffffff").place(x=160,y=43)

        date_time = datetime.datetime.now()
        
        date = str(date_time.strftime("%d")) + "/" + str(date_time.strftime("%m")) + "/" + str(date_time.strftime("%Y"))
        time = str(date_time.strftime("%I")) + " : " + str(date_time.strftime("%M")) + " " + str(date_time.strftime("%p"))

        date_label=Label(self.win,text=date,font=('Calibari',12, 'bold'),bg="#ffffff").place(x=870,y=43)
        # clock_label=Label(self.win,text=time,font=('Calibari',12, 'bold'),bg="#ffffff").place(x=875,y=65)

        #Left Menu
        navbar = Frame(self.win, border=2, background="#212529")
        navbar.place(x=0,y=35,height=535,width=150)

        profile_icon = ImageTk.PhotoImage(file="Images/Icon.ico")
        profile_img = Label(navbar, image=profile_icon,background="#212529").place(x=50, y=10)
        
        admin_name = self.vals['Name'][:10]
        
        profile = Label(navbar, text=f"Welcome {admin_name}",font=('Calibari',9), background="#212529", foreground="#ffffff").place(x=10,y=62,height=20,width=140)
        emp_btn = Button(navbar, text="Employees", font=('Cilibari', 11,),bg="#ffffff",command=self.empDashboard).place(x=0,y=95,height=35,width=147)
        payroll_btn = Button(navbar, text="Payroll", font=('Cilibari', 11,),bg="#ffffff",command=self.empPayroll).place(x=0,y=130,height=35,width=147)
        notice_btn = Button(navbar, text="Send Notice", font=('Cilibari', 11,),bg="#ffffff", command=self.noticeWin).place(x=0,y=165,height=35,width=147)
        
        profile_btn = Button(navbar, text="Profile", font=('Cilibari', 10,),bg="#212529", fg="#0d6efd", border=0, anchor=W, command=self.get_admin_data).place(x=20, y=440, width=120)
        change_pasw_btn = Button(navbar, text="Change Password", font=('Cilibari', 10,),bg="#212529", fg="#0d6efd", border=0, anchor=W, command=self.change_pswd).place(x=20, y=470, width=120)
        logout_btn = Button(navbar, text="Logout", font=('Cilibari', 10,),bg="#212529", fg="#0d6efd", border=0, anchor=W, command=self.logout).place(x=20, y=500, width=120)

        self.get_total_emp()
        self.get_total_dept()

        #Data Labels
        emp_label=Label(self.win, text=f"Total emps\n-------------------------\n{self.total_emp}",font=('Calibari',12), background="#dc3545", foreground="#ffffff",justify="left").place(x=160,y=125,height=105,width=150)
        dep_label=Label(self.win, text=f"Total Departments\n-------------------------\n{self.total_dept}",font=('Calibari',12), background="#ffc107", foreground="#000000",justify="left").place(x=350,y=125,height=105,width=150)
        # present_label = Label(self.win, text="Today's Present\n-------------------------\n20",font=('Calibari',12), background="#198754", foreground="#ffffff",justify="left").place(x=540,y=125,height=105,width=150)

        # # Present List
        list_frame = Frame(self.win, border=2, background='#ffffff')
        list_frame.place(x=160,y=250,height=310,width=830)

        scrolly = Scrollbar(list_frame,orient=VERTICAL)
        scrollx = Scrollbar(list_frame,orient=HORIZONTAL)

        list_title = Label(list_frame, text="Department List",font=('Calibari',12, 'bold'),background="#ffffff").place(x=0,y=10,height=20,width=150)
        add_dept = Button(list_frame, text="+ Add Department", font=('Cilibari', 10),bg="#0d6efd", command=self.Add_Dept).place(x=510, y=10, height=30, width=120)
        delete_dept = Button(list_frame, text="Delete", font=('Cilibari', 10),bg="#dc3545", command=self.delDepts).place(x=635, y=10, height=30, width=90)
        edit_dept = Button(list_frame, text="Edit", font=('Cilibari', 10),bg="#ffc107", command=self.UpdateDept).place(x=730, y=10, height=30, width=80)

        self.list_table = ttk.Treeview(list_frame,columns=('sr_no','name','dept_head'),yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)

        scrolly.place(x=792, y=60, height=230)
        scrolly.config(command=self.list_table.yview)

        self.list_table.heading("sr_no", text="Sr No.")
        self.list_table.heading("name", text="Name")
        self.list_table.heading("dept_head", text="Department Head")
        self.list_table["show"]="headings"

        self.list_table.column("sr_no", minwidth=100, anchor=CENTER)
        self.list_table.column("name", minwidth=200, anchor=CENTER)
        self.list_table.column("dept_head", minwidth=170, anchor=CENTER)

        self.showDepartments()
        
        self.list_table.place(x=15,y=60,height=230,width=778)
        self.list_table.bind('<ButtonRelease-1>', self.updateDept)

        footer=Label(self.win,height=2,width=300,bg='#0d6efd').place(x=0,y=570)
        
        self.win.mainloop()

    def empDashboard(self):
        new_obj = Toplevel(self.win)
        new_win = EmpSection(new_obj)

    def empPayroll(self):
        new_obj = Toplevel(self.win)
        new_win = EmpPayroll(new_obj)

    def noticeWin(self):
        new_obj = Toplevel(self.win)
        new_win = SendNotice(new_obj)

    def change_pswd(self):
        new_obj = Toplevel(self.win)
        new_win = ChangePasswd(new_obj)

    def Add_Dept(self):
        new_obj = Toplevel(self.win)
        new_win = AddDepts(new_obj)

    def myProfile(self, user_data):
        new_obj = Toplevel(self.win)
        new_win = MyProfile(new_obj, user_data)

    def UpdateDept(self):
        if len(self.values) <= 0:
            messagebox.showerror("Error", "Please Choose a Entry to Update", parent=self.win)
            return
        else:
            values = self.values
            new_obj = Toplevel(self.win)
            new_win = UpdateDepts(new_obj, values)

    #======================================================================================================================================================================#
    # functions

    def refresh(self, ev):
        self.showDepartments()
        self.get_total_dept()
        self.get_total_emp()

    def showDepartments(self):
        try:
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="root",
                database="empmangsys"
            )
            mycursor = mydb.cursor()

            query = "SELECT * FROM department;"
            mycursor.execute(query)

            rows = mycursor.fetchall()
            self.list_table.delete(*self.list_table.get_children())
            sr_no = 1
            for row in rows:
                dept_row = (sr_no, row[0], row[1])
                self.list_table.insert(parent='', index='end', text="Employee", values=dept_row)
                sr_no += 1

            mydb.commit()

        except Exception as Ex:
            messagebox.showerror("Error", f'Error Ocuured Due TO {Ex}')

    def updateDept(self,ev):
        row = self.list_table.focus()
        content = (self.list_table.item(row))
        vals = content['values']
        self.values = vals
        print(self.values)

    def get_admin_data(self):
        try:
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="root",
                database="empmangsys"
            )
            mycursor = mydb.cursor()

            adminID = self.vals['adminID']
            print(adminID)

            query = "SELECT ADMINID, Name, Gender, Email, Mobile, Username FROM admin WHERE ADMINID = %s;"
            value = (adminID,)

            mycursor.execute(query, value)
            user = mycursor.fetchone()

            if user != None:
                self.myProfile(user)
            else:
                messagebox.showerror('Error', 'Please Enter Correct Admin ID', parent=self.win)

        except Exception as ex:
            messagebox.showerror('Error', f'Error Occured - {ex} ! Please Try Again Later!!', parent=self.win)

    def get_total_emp(self):
        try:
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="root",
                database="empmangsys"
            )
            mycursor = mydb.cursor()

            adminID = self.vals['adminID']

            query = "SELECT * FROM employee;"

            mycursor.execute(query)
            emps = mycursor.fetchall()

            if emps != None:
                self.total_emp = len(emps)
            else:
                self.total_emp = 0

        except Exception as ex:
            messagebox.showerror('Error', f'Error Occured - {ex} ! Please Try Again Later', parent=self.win)

    def get_total_dept(self):
        try:
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="root",
                database="empmangsys"
            )
            mycursor = mydb.cursor()

            adminID = self.vals['adminID']

            query = "SELECT * FROM department;"

            mycursor.execute(query)
            depts = mycursor.fetchall()

            if depts != None:
                self.total_dept = len(depts)
            else:
                self.total_dept = 0

        except Exception as ex:
            messagebox.showerror('Error', f'Error Occured - {ex} ! Please Try Again Later', parent=self.win)

    def delDepts(self):
        try:
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="root",
                database="empmangsys"
            )
            mycursor = mydb.cursor()

            row = self.list_table.focus()
            content = (self.list_table.item(row))
            vals = content['values']

            if len(vals) <= 0:
                messagebox.showerror("Error", "Please Choose a Entry to Delete", parent=self.win)
                return
            else:
                '''query="DELETE FROM employee WHERE EMPID=7;"'''

                opt = messagebox.askyesno("Delete", "Are You Sure Want To Delete", parent=self.win)

                if opt==True:
                    name = vals[1]
                    query = "DELETE FROM department WHERE Name=%s;"
                    val = (name,)
                    mycursor.execute(query, val)
                    mydb.commit()

                    messagebox.showinfo("Done", "Department Delete Successfully", parent=self.win)
                    self.showDepartments()

        except Exception as Ex:
            messagebox.showerror("Error", str(Ex))

    def logout(self):
        self.win.destroy()
        os.system("python admin_login.py")

if __name__ == '__main__':
    root = Tk()
    new_win = Dashborad(root)