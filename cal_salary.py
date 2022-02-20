from tkinter import *
from PIL import ImageTk
from tkinter import ttk, messagebox
import mysql.connector
import datetime

class CalEmpSalary:
    def __init__(self, win, entry_values):
        self.win = win
        self.win.geometry("540x500+500+10")
        self.win.title("Add Employee")
        self.win.configure(bg="#ffffff")
        self.win.focus_force()

        self.empid = IntVar()
        self.name = StringVar()
        self.profile = StringVar()
        self.dept = StringVar()

        self.salary = DoubleVar()
        self.overtime = IntVar()
        self.conveyance = DoubleVar()
        self.absents = IntVar()

        self.net_salary = 0.00

        # Set Entry Variables Before Salary Calculation
        self.empid.set(entry_values[0])
        self.name.set(entry_values[1])
        self.profile.set(entry_values[2])
        self.dept.set(entry_values[3])

        self.salary.set(entry_values[4])

        self.conveyance.set(entry_values[6])

        title = Label(self.win,text="Payroll Details", font=('Calibari',11),fg="#ffffff",bg='#0d6efd').place(x=0,y=0,height=30,width=540)

        #Personal Details Form
        salary_details_frame = LabelFrame(self.win, text="Employee Details",font=('Calibari',10),bg="#ffffff")
        salary_details_frame.place(x=20,y=50,width=500,height=120)

        emp_id_label = Label(salary_details_frame,font=('Calibari',10), text="Employee ID*",bg="#ffffff").place(x=10,y=20,height=20)
        emp_id_entry = Entry(salary_details_frame,textvariable=self.empid,font=('Calibari',10),bg="#fffff0").place(x=105,y=20,width=110,height=20)

        name_label = Label(salary_details_frame,font=('Calibari',10), text="Name*",bg="#ffffff").place(x=230,y=20,height=20)
        name_entry = Entry(salary_details_frame,textvariable=self.name,font=('Calibari',10),bg="#fffff0").place(x=285,y=20,width=195,height=20)

        profile_label = Label(salary_details_frame,font=('Calibari',10), text="Profile*",bg="#ffffff").place(x=10,y=55,height=20)
        profile_entry = Entry(salary_details_frame,textvariable=self.profile,font=('Calibari',10),bg="#fffff0").place(x=65,y=55,width=150,height=20)

        dept_label = Label(salary_details_frame,font=('Calibari',10), text="Department*",bg="#ffffff").place(x=230,y=55,height=20)
        dept_entry = Entry(salary_details_frame,textvariable=self.dept,font=('Calibari',10),bg="#fffff0").place(x=315,y=55,width=165,height=20)

        #Salary Details Form

        salary_details_frame = LabelFrame(self.win, text="Salary Details",font=('Calibari',10),bg="#ffffff")
        salary_details_frame.place(x=20,y=200,width=500,height=120)

        basic_label = Label(salary_details_frame,font=('Calibari',10), text="Basic Salary*",bg="#ffffff").place(x=10,y=20,height=20)
        basic_entry = Entry(salary_details_frame,textvariable=self.salary,font=('Calibari',10),bg="#fffff0").place(x=105,y=20,width=120,height=20)

        overtime_label = Label(salary_details_frame,font=('Calibari',10), text="Overtime(Hrs)*",bg="#ffffff").place(x=255,y=20,height=20)
        overtime_entry = Entry(salary_details_frame,textvariable=self.overtime,font=('Calibari',10),bg="#fffff0").place(x=355,y=20,width=130,height=20)

        conveyance_label = Label(salary_details_frame,font=('Calibari',10), text="Conveyance*",bg="#ffffff").place(x=10,y=55,height=20)
        conveyance_entry = Entry(salary_details_frame,textvariable=self.conveyance,font=('Calibari',10),bg="#fffff0").place(x=105,y=55,width=120,height=20)
        
        absenties_label = Label(salary_details_frame,font=('Calibari',10), text="Absenties*",bg="#ffffff").place(x=255,y=55,height=20)
        absenties_entry = Entry(salary_details_frame,textvariable=self.absents,font=('Calibari',10),bg="#fffff0").place(x=355,y=55,width=130,height=20)

        submit_btn = Button(self.win, text="Calculate", font=('Cilibari', 10),bg="#0d6efd", command=self.calculate_salary).place(x=210,y=360,height=30,width=120)
        
        self.win.mainloop()
    #=========================================================================================================#
    #functions

    def calculate_salary(self):
        emp_salary = self.salary.get()
        conveyance = self.conveyance.get()
        absents = self.absents.get()
        overtime = self.overtime.get()

        overtime_rs = float(overtime) * 300.00
        emp_salary = emp_salary + overtime_rs
        print(emp_salary)

        emp_salary = emp_salary + conveyance
        print(emp_salary)

        if absents > 7:
            absent_days = absents - 7
            deduction = float(absent_days) * 500.00
        else:
            deduction = 0.0
        
        emp_salary = emp_salary - deduction
        print(emp_salary)
              
        self.net_salary = emp_salary

        net_salary_label = Label(self.win,font=('Calibari',10), text=f"Net Salary : {self.net_salary}",bg="#ffffff").place(x=20,y=450)

        updated_datetime = str(datetime.datetime.now())
        last_updated_datetime = updated_datetime[:16]

        mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="root",
                database="empmangsys"
            )
        mycursor = mydb.cursor()

        query = "UPDATE salary SET Overtime_Rs=%s, Deduction_Rs=%s, Net_Salary_Rs=%s, Last_Updated=%s WHERE EMPID = %s;"
        
        vals = (overtime_rs, deduction, self.net_salary, last_updated_datetime, self.empid.get())

        mycursor.execute(query, vals)
        mydb.commit()

if __name__ == '__main__':
    root = Tk()
    new_win = CalEmpSalary(root)