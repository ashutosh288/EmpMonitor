from tkinter import *
from PIL import ImageTk
from tkinter import ttk, messagebox
import mysql.connector

class AddEmp:
    def __init__(self, win):
        self.win = win
        self.win.geometry("540x500+500+10")
        self.win.title("Add Employee")
        self.win.configure(bg="#ffffff")
        self.win.focus_force()
        
        self.getDepartments()

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

        title = Label(self.win,text="Employee Details", font=('Calibari',11),fg="#ffffff",bg='#0d6efd').place(x=0,y=0,height=30,width=540)

        #Personal Details Form
        prsnl_detail_frame = LabelFrame(self.win, text="Personal Details",font=('Calibari',10),bg="#ffffff")
        prsnl_detail_frame.place(x=20,y=50,width=500,height=150)

        emp_id_label = Label(prsnl_detail_frame,font=('Calibari',10), text="Employee ID*",bg="#ffffff").place(x=10,y=20,height=20)
        emp_id_entry = Entry(prsnl_detail_frame,textvariable=self.empid ,font=('Calibari',10),bg="#fffff0").place(x=95,y=20,width=100,height=20)

        name_label = Label(prsnl_detail_frame,font=('Calibari',10), text="Name*",bg="#ffffff").place(x=210,y=20,height=20)
        name_entry = Entry(prsnl_detail_frame,textvariable=self.name ,font=('Calibari',10),bg="#fffff0").place(x=255,y=20,width=225,height=20)

        gender_label = Label(prsnl_detail_frame,font=('Calibari',10), text="Gender*",bg="#ffffff").place(x=10,y=55,height=20)
        gender_entry = Entry(prsnl_detail_frame,textvariable=self.gender ,font=('Calibari',10),bg="#fffff0").place(x=95,y=55,width=100,height=20)

        email_label = Label(prsnl_detail_frame,font=('Calibari',10), text="Email*",bg="#ffffff").place(x=210,y=55,height=20)
        email_entry = Entry(prsnl_detail_frame,textvariable=self.mail ,font=('Calibari',10),bg="#fffff0").place(x=255,y=55,width=225,height=20)

        dob_label = Label(prsnl_detail_frame,font=('Calibari',10), text="Date Of Birth*",bg="#ffffff").place(x=10,y=90,height=20)
        dob_entry = Entry(prsnl_detail_frame,textvariable=self.dob ,font=('Calibari',10),bg="#fffff0").place(x=95,y=90,width=100,height=20)

        phone_label = Label(prsnl_detail_frame,font=('Calibari',10), text="Mobile No.(add +91)*",bg="#ffffff").place(x=210,y=90,height=20)
        pnone_entry = Entry(prsnl_detail_frame,textvariable=self.phone ,font=('Calibari',10),bg="#fffff0").place(x=340,y=90,width=140,height=20)

        #Comapany Details Form
        comp_detail_frame = LabelFrame(self.win, text="Company Details",font=('Calibari',10),bg="#ffffff")
        comp_detail_frame.place(x=20,y=220,width=500,height=150)

        doj_label = Label(comp_detail_frame,font=('Calibari',10), text="Date Of Joining",bg="#ffffff").place(x=10,y=20,height=20)
        doj_entry = Entry(comp_detail_frame,textvariable=self.doj,font=('Calibari',10),bg="#fffff0").place(x=110,y=20,width=100,height=20)

        profile_label = Label(comp_detail_frame,font=('Calibari',10), text="Work Profile",bg="#ffffff").place(x=220,y=20,height=20)
        profile_entry = Entry(comp_detail_frame,textvariable=self.profile,font=('Calibari',10),bg="#fffff0").place(x=305,y=20,width=175,height=20)

        salary_label = Label(comp_detail_frame,font=('Calibari',10), text="Salary(in Rs)",bg="#ffffff").place(x=10,y=56,height=20)
        salary_entry = Entry(comp_detail_frame,textvariable=self.salary,font=('Calibari',10),bg="#fffff0").place(x=110,y=56,width=100,height=20)

        dept_label = Label(comp_detail_frame,font=('Calibari',10), text="Department",bg="#ffffff").place(x=220,y=56,height=20)
        # dept_entry = Entry(comp_detail_frame,textvariable=self.dept,font=('Calibari',10),bg="#fffff0").place(x=305,y=56,width=175,height=20)

        dept_entry = ttk.Combobox(comp_detail_frame,textvariable=self.dept, value=self.departments, state='readonly')
        dept_entry.place(x=305,y=56,width=175,height=20)
        dept_entry.current(0)

        conveyance_label = Label(comp_detail_frame,font=('Calibari',10), text="Conveyance(in Rs)",bg="#ffffff").place(x=10,y=92,height=20)
        conveyance_entry = Entry(comp_detail_frame,textvariable=self.conveyance,font=('Calibari',10),bg="#fffff0").place(x=130,y=92,width=100,height=20)

        submit_btn = Button(self.win, text="Add Employee", font=('Cilibari', 10),bg="#0d6efd",command=self.addEmployee).place(x=210,y=390,height=30,width=120)

        date_label = Label(self.win,font=('Calibari',10), text="Date Format :- YYYY-MM-DD",bg="#ffffff").place(x=20,y=450)
        
        self.win.mainloop()
    #=========================================================================================================#
    #functions

    def getDepartments(self):
        try:
            self.departments = []
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="root",
                database="empmangsys"
            )
            mycursor = mydb.cursor()

            query = "SELECT Name FROM department;"
            mycursor.execute(query)

            rows = mycursor.fetchall()

            for row in rows:
                self.departments.append(row[0])

            self.departments = tuple(self.departments)
            print(self.departments)

            mydb.commit()

        except Exception as Ex:
            messagebox.showerror("Error", f'Error Ocuured Due TO {Ex}')

    def addEmployee(self):
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
                
                if row != None:
                    messagebox.showerror("Error", "This Employee ID is Already Exists! Please Check and Try Again.")
                    return

                '''query = "INSERT INTO employee (EMPID, Name, DOB, Gender, Mobile, Email, DOJ, Profile,  Department, Salary, Conveyance) VALUES (3, 'Sholak Awasthi', '1995-02-24', 'Male', '+918965320147', 'awasthi_sholak@gmail.com', '2003-09-28', 'React Developer', 'Web Development','10000', '2000');"'''

                '''
                    Date Format : YYYY-MM-DD
                '''

                query = "INSERT INTO employee (EMPID, Name, DOB, Gender, Mobile, Email, DOJ, Profile,  Department, Salary, Conveyance) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);" 
                vals = (self.empid.get(), self.name.get(), self.dob.get(), self.gender.get(), self.phone.get(), self.mail.get(), self.doj.get(), self.profile.get(), self.dept.get(),self.salary.get(), self.conveyance.get(),)

                mycursor.execute(query, vals)

                query2 = "INSERT INTO salary (EMPID, Basic_Salary, Overtime_Rs, Conveyance_Rs, Deduction_Rs, Net_Salary_Rs, Last_Updated) VALUES (%s,%s,%s,%s,%s,%s,%s);"
                vals2 = (self.empid.get(), self.salary.get(), None, self.conveyance.get(), None, None, None)

                mycursor.execute(query2, vals2)

                mydb.commit()

                messagebox.showinfo("Done", "Employee Added Successfully", parent=self.win)

        except Exception as Ex:
            messagebox.showerror("Error", str(Ex), parent=self.win)