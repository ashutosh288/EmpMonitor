from tkinter import *
from PIL import ImageTk
from tkinter import ttk, messagebox
import mysql.connector

class UpdateEmp:
    def __init__(self, win, entry_values):
        self.win = win
        self.win.geometry("540x500")
        self.win.title("Update Employee Details")
        self.win.configure(bg="#ffffff")
        self.win.focus_force()

        self.empid = IntVar()
        self.name = StringVar()
        self.gender = StringVar()
        self.mail = StringVar()
        self.dob = StringVar()
        self.phone = StringVar()
        
        self.doj = StringVar()
        self.profile = StringVar()
        self.dept = StringVar()
        self.salary = DoubleVar()
        self.conveyance = DoubleVar()

        # Set Entry Variables Before Updation
        self.empid.set(entry_values[0])
        self.name.set(entry_values[1])
        self.gender.set(entry_values[3])
        self.mail.set(entry_values[5])
        self.dob.set(entry_values[2])
        self.phone.set(entry_values[4])
        
        self.doj.set(entry_values[6])
        self.profile.set(entry_values[7])
        self.dept.set(entry_values[8])
        self.salary.set(entry_values[9])
        self.conveyance.set(entry_values[10])

        title = Label(self.win,text="Update Employee Details", font=('Calibari',11),fg="#ffffff",bg='#0d6efd').place(x=0,y=0,height=30,width=540)

        #Personal Details Form
        prsnl_detail_frame = LabelFrame(self.win, text="Personal Details",font=('Calibari',10),bg="#ffffff")
        prsnl_detail_frame.place(x=20,y=50,width=500,height=150)

        emp_id_label = Label(prsnl_detail_frame,font=('Calibari',10), text="Employee ID",bg="#ffffff").place(x=10,y=20,height=20)
        emp_id_entry = Entry(prsnl_detail_frame,textvariable=self.empid,font=('Calibari',10),bg="#fffff0").place(x=95,y=20,width=100,height=20)

        name_label = Label(prsnl_detail_frame,font=('Calibari',10), text="Name",bg="#ffffff").place(x=210,y=20,height=20)
        name_entry = Entry(prsnl_detail_frame,textvariable=self.name,font=('Calibari',10),bg="#fffff0").place(x=255,y=20,width=225,height=20)

        gender_label = Label(prsnl_detail_frame,font=('Calibari',10), text="Gender",bg="#ffffff").place(x=10,y=55,height=20)
        gender_entry = Entry(prsnl_detail_frame,textvariable=self.gender,font=('Calibari',10),bg="#fffff0").place(x=95,y=55,width=100,height=20)

        email_label = Label(prsnl_detail_frame,font=('Calibari',10), text="Email",bg="#ffffff").place(x=210,y=55,height=20)
        email_entry = Entry(prsnl_detail_frame,textvariable=self.mail,font=('Calibari',10),bg="#fffff0").place(x=255,y=55,width=225,height=20)

        dob_label = Label(prsnl_detail_frame,font=('Calibari',10), text="Date Of Birth",bg="#ffffff").place(x=10,y=90,height=20)
        dob_entry = Entry(prsnl_detail_frame,textvariable=self.dob,font=('Calibari',10),bg="#fffff0").place(x=95,y=90,width=100,height=20)

        phone_label = Label(prsnl_detail_frame,font=('Calibari',10), text="Mobile No.(add +91)",bg="#ffffff").place(x=210,y=90,height=20)
        pnone_entry = Entry(prsnl_detail_frame,textvariable=self.phone,font=('Calibari',10),bg="#fffff0").place(x=340,y=90,width=140,height=20)


        #Comapany Details Form
        comp_detail_frame = LabelFrame(self.win, text="Company Details",font=('Calibari',10),bg="#ffffff")
        comp_detail_frame.place(x=20,y=220,width=500,height=150)
        print(type(comp_detail_frame))

        doj_label = Label(comp_detail_frame,font=('Calibari',10), text="Date Of Joining",bg="#ffffff").place(x=10,y=20,height=20)
        doj_entry = Entry(comp_detail_frame,textvariable=self.doj,font=('Calibari',10),bg="#fffff0").place(x=110,y=20,width=100,height=20)

        profile_label = Label(comp_detail_frame,font=('Calibari',10), text="Work Profile",bg="#ffffff").place(x=220,y=20,height=20)
        profile_entry = Entry(comp_detail_frame,textvariable=self.profile,font=('Calibari',10),bg="#fffff0").place(x=305,y=20,width=175,height=20)

        salary_label = Label(comp_detail_frame,font=('Calibari',10), text="Salary(in Rs)",bg="#ffffff").place(x=10,y=56,height=20)
        salary_entry = Entry(comp_detail_frame,textvariable=self.salary,font=('Calibari',10),bg="#fffff0").place(x=110,y=56,width=100,height=20)

        dept_label = Label(comp_detail_frame,font=('Calibari',10), text="Department",bg="#ffffff").place(x=220,y=56,height=20)
        dept_entry = Entry(comp_detail_frame,textvariable=self.dept,font=('Calibari',10),bg="#fffff0").place(x=305,y=56,width=175,height=20)

        conveyance_label = Label(comp_detail_frame,font=('Calibari',10), text="Conveyance(in Rs)",bg="#ffffff").place(x=10,y=92,height=20)
        conveyance_entry = Entry(comp_detail_frame,textvariable=self.conveyance,font=('Calibari',10),bg="#fffff0").place(x=130,y=92,width=100,height=20)

        submit_btn = Button(self.win, text="Update", font=('Cilibari', 10),bg="#0d6efd",command=self.UpdateEmpData).place(x=210,y=390,height=30,width=120)

        date_label = Label(self.win,font=('Calibari',10), text="Date Format :- YYYY-MM-DD",bg="#ffffff").place(x=20,y=450)
        
        self.win.mainloop()

    #==========================================================================================================#
    # functions

    def UpdateEmpData(self):
        try:
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="root",
                database="empmangsys"
            )
            mycursor = mydb.cursor()

            if self.empid.get() == "" or self.name.get() == "" or self.gender.get() == "" or self.mail.get() == "" or self.dob.get() == "" or self.phone.get() == "" or self.doj.get() == "" or self.profile.get() == "" or self.dept.get() == "" or self.salary.get() == "" or self.conveyance.get() == "":
                messagebox.showerror("Error", "Fill All Required Details", parent=self.win)
            else:
                query = "SELECT * FROM employee WHERE EMPID = %s;"
                value = (self.empid.get(),)

                mycursor.execute(query, value)
                row = mycursor.fetchone()
                print(row)
                
                if row == None:
                    messagebox.showerror("Error", "Invalid Employee ID! Please Check and Try Again.")
                    return

                '''query = "UPDATE employee SET Salary=35000.00 WHERE EMPID=1;"'''

                '''
                    Date Format : YYYY-MM-DD
                '''

                query = "UPDATE employee SET Name = %s, DOB = %s, Gender = %s, Mobile = %s, Email = %s, DOJ = %s, Profile = %s,  Department = %s, Salary = %s, Conveyance = %s WHERE EMPID = %s;"
                vals = (self.name.get(), self.dob.get(), self.gender.get(), self.phone.get(), self.mail.get(), self.doj.get(), self.profile.get(), self.dept.get(),self.salary.get(),self.conveyance.get(),self.empid.get(),)

                mycursor.execute(query, vals)

                query1 = "UPDATE salary SET Basic_Salary = %s, Conveyance_Rs = %s WHERE EMPID = %s;"
                vals1 = (self.salary.get(),self.conveyance.get(),self.empid.get(),)

                mycursor.execute(query1, vals1)

                mydb.commit()

                messagebox.showinfo("Done", "Employee Data Updated Successfully", parent=self.win)

        except Exception as Ex:
            messagebox.showerror("Error", str(Ex))

if __name__ == '__main__':
    root = Tk()
    new_win = UpdateEmp(root)