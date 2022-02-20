from tkinter import *
from PIL import ImageTk
from tkinter import ttk,messagebox
import mysql.connector
from cal_salary import CalEmpSalary
#from gen_pay_slip import GenPaySlip

class EmpPayroll:
    def __init__(self, win):
        self.win = win
        self.win.geometry("840x440+170+230")
        self.win.title("Employees Payroll")
        self.win.configure(bg="#ffffff")
        self.win.focus_force()

        self.win.bind('<FocusIn>', self.refresh)

        self.search_by = StringVar()
        self.serach_text = StringVar()

        title = Label(self.win, text="Employee Payroll", font=(
            'Calibari', 11), fg="#ffffff", bg='#0d6efd').place(x=0, y=0, height=30, width=840)

        search_frame = LabelFrame(self.win, text="Search Employee", font=('Calibari', 10), bg="#ffffff")
        search_frame.place(x=50, y=50, width=500, height=70)

        '''search_options = ttk.Combobox(search_frame, value=('Select', 'Employee ID', 'Name', 'Department'), state='readonly')
        search_options.place(x=10, y=10, width=150, height=20)
        search_options.current(0)

        search_input = Entry(search_frame, font=('Calibari', 10), bg="#fffff0").place(x=170, y=10, width=200, height=20)
        search_btn = Button(search_frame, text="Search", font=('Cilibari', 10), bg="#198754").place(x=380, y=10, height=20, width=100)'''

        search_options = ttk.Combobox(search_frame,textvariable=self.search_by, value=(
            'Select', 'EMPID', 'Name', 'Department'), state='readonly')
        search_options.place(x=10, y=10, width=110, height=20)
        search_options.current(0)

        search_input = Entry(search_frame,textvariable=self.serach_text, font=('Calibari', 10), bg="#fffff0").place(x=130, y=10, width=200, height=20)
        search_btn = Button(search_frame, text="Search", font=('Cilibari', 10), bg="#198754",command=self.searchEmp).place(x=340, y=10, height=20, width=70)
        clr_btn = Button(search_frame, text="Clear", font=('Cilibari', 10),bg="#6c757d", fg="#ffffff",command=self.clear).place(x=420, y=10, height=20, width=70)

        cal_slary_btn = Button(self.win, text="Calculate Salary", font=('Cilibari', 10), bg="#0dcaf0", command=self.CalSalary).place(x=570, y=88, height=30, width=120)
        print_btn = Button(self.win, text="Generate Pay Slip", font=('Cilibari', 10), bg="#6c757d", fg="#ffffff", command = self.genPaySlip).place(x=700, y=88, height=30, width=125)

        # list_frame1 = Frame(self.win, border=2, background="#6c757d").place(x=10,y=100,height=280,width=770)

        scrolly = Scrollbar(self.win, orient=VERTICAL)
        scrollx = Scrollbar(self.win, orient=HORIZONTAL)

        self.emp_table = ttk.Treeview(self.win, columns=('emp_id', 'name', 'profile', 'dept', 'salary','overtime','conveyance', 'deduction', 'net_salary', 'last_updated'), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)

        scrolly.place(x=810, y=140, height=280)
        scrolly.config(command=self.emp_table.yview)

        scrollx.place(x=10, y=404, width=810)
        scrollx.config(command=self.emp_table.xview)

        self.emp_table.heading("emp_id", text="Employee ID")
        self.emp_table.heading("name", text="Name")
        self.emp_table.heading("profile", text="Profile")
        self.emp_table.heading("dept", text="Department")
        self.emp_table.heading("salary", text="Salary (Rs)")
        self.emp_table.heading("overtime", text="Overtime (Rs)")
        self.emp_table.heading("conveyance", text="Conveyance (Rs)")
        self.emp_table.heading("deduction", text="Deduction (Rs)")
        self.emp_table.heading("net_salary", text="Net Salary To Pay (Rs)")
        self.emp_table.heading("last_updated", text="Last Updated")
        self.emp_table["show"] = "headings"

        self.emp_table.column("emp_id", width=90, minwidth=90, anchor=CENTER)
        self.emp_table.column("name", width=180, minwidth=180, anchor=CENTER)
        self.emp_table.column("profile", width=180, minwidth=180, anchor=CENTER)
        self.emp_table.column("dept", width=180, minwidth=180, anchor=CENTER)
        self.emp_table.column("salary", width=100, minwidth=90, anchor=CENTER)
        self.emp_table.column("overtime", width=100, minwidth=90, anchor=CENTER)
        self.emp_table.column("conveyance", width=100, minwidth=90, anchor=CENTER)
        self.emp_table.column("deduction", width=100, minwidth=90, anchor=CENTER)
        self.emp_table.column("net_salary", width=180, minwidth=120, anchor=CENTER)
        self.emp_table.column("last_updated", width=180, minwidth=120, anchor=CENTER)

        self.ShowPayrollList()

        self.emp_table.place(x=10, y=140, height=264, width=800)
        self.emp_table.bind('<ButtonRelease-1>', self.getEmp_data)
        self.vals_row_focus = []

        self.win.mainloop()

    def CalSalary(self):
        if len(self.vals_row_focus) <= 0:
            messagebox.showerror("Error", "Please Choose a Entry to Calculate Salary", parent=self.win)
            return
        else:
            vals_row_focus_obj = self.vals_row_focus
            new_obj = Toplevel(self.win)
            new_win = CalEmpSalary(new_obj, vals_row_focus_obj)

    def genPaySlip(self):
        if len(self.vals_row_focus) <= 0:
            messagebox.showerror("Error", "Please Choose a Entry to Print Salary Slip", parent=self.win)
            return
        else:
            entry_values = self.vals_row_focus
            # new_obj = Toplevel(self.win)
            # new_win = GenPaySlip(new_obj, vals_row_focus_obj)

            total = float(entry_values[4])+float(entry_values[5])+float(entry_values[6])

            txt = f'''
\t\t\t      ABC Infotech Pvt Limited
\t\t Ganesh Tower Gandhi Nagar, Surat, Gujrat - 556625

\t\t\t\t    PAY SLIP
====================================================================================
Employee ID     : {entry_values[0]}\t\t\t\tProfile     : {entry_values[2]}
Employee Name   : {entry_values[1]}\t\t\tDepartment  : {entry_values[3]}
------------------------------------------------------------------------------------
Basic Salary    : {entry_values[4]} Rs
Overtime        : {entry_values[5]} Rs
Conveyance      : {entry_values[6]} Rs
------------------------------------------------------------------------------------
Total           : {total}0 Rs
------------------------------------------------------------------------------------
Deduction\t: {entry_values[7]} Rs
------------------------------------------------------------------------------------
\t\t\t\t\t\t     Net Salary To Pay : {entry_values[8]} Rs
====================================================================================



Date : {entry_values[9][0:10]}\t\t\t\t\t\t Authority Signature
'''
            f = open('Pay Slips/'+str(entry_values[0])+" - "+str(entry_values[9][0:10])+'.txt', 'w')
            f.write("\t\t\t ABC Infotech Pvt Limited\n")
            f.write("\t    Ganesh Tower Gandhi Nagar, Surat, Gujrat - 556625\n\n")
            f.write("\t\t\t\tPAY SLIP\n")
            f.write("========================================================================\n")
            f.write(f"Employee ID     : {entry_values[0]}\t\t     Profile     : {entry_values[2]}\n")
            f.write(f"Employee Name   : {entry_values[1]}\t     Department  : {entry_values[3]}\n")
            f.write("------------------------------------------------------------------------\n")
            f.write(f"Basic Salary    : {entry_values[4]} Rs\n")
            f.write(f"Overtime        : {entry_values[5]} Rs\n")
            f.write(f"Conveyance      : {entry_values[6]} Rs\n")
            f.write("------------------------------------------------------------------------\n")
            f.write(f"Total           : {total}0 Rs\n")
            f.write("------------------------------------------------------------------------\n")
            f.write(f"Deduction\t: {entry_values[7]} Rs\n")
            f.write("------------------------------------------------------------------------\n")
            f.write(f"\t\t\t\t\tNet Salary To Pay : {entry_values[8]} Rs\n")
            f.write("========================================================================\n\n\n\n")
            f.write(f"Date : {entry_values[9][0:10]}\t\t\t\t    Authority Signature")


            f.close()
    #========================================================================================================#
    # functions

    def getEmp_data(self,ev):
        row = self.emp_table.focus()
        content = (self.emp_table.item(row))
        vals = content['values']
        self.vals_row_focus = vals
        print(self.vals_row_focus)

    def refresh(self, ev):
        self.ShowPayrollList()

    def ShowPayrollList(self):
        try:
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="root",
                database="empmangsys"
            )
            mycursor = mydb.cursor()

            query = "SELECT * FROM salary;"
            mycursor.execute(query)

            rows = mycursor.fetchall()
            self.emp_table.delete(*self.emp_table.get_children())
            for row in rows:
                query2 = "SELECT Name, Profile, Department FROM employee WHERE EMPID = %s;"
                vals = (row[0],)
                mycursor.execute(query2, vals)

                results = mycursor.fetchall()

                self.emp_table.insert(parent='', index='end', text="Employee Salary", values=[row[0],results[0][0],results[0][1],results[0][2],row[1],row[2],row[3],row[4],row[5],row[6]])

            mydb.commit()

        except Exception as Ex:
            messagebox.showerror("Error", str(Ex), parent=self.win)

    def searchEmp(self):
        try:
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="root",
                database="empmangsys"
            )
            mycursor = mydb.cursor()

            if self.search_by.get() == "Select":
                messagebox.showerror("Error","Please Select Serach By Option", parent=self.win)

            elif self.serach_text.get() == "":
                messagebox.showerror("Error","Please enter Search Details", parent=self.win)

            elif self.search_by.get() == "EMPID":
                query = "SELECT * FROM salary WHERE " + str(self.search_by.get()) + " LIKE '%" + str(self.serach_text.get()) + "%';"
                mycursor.execute(query)

                rows = mycursor.fetchall()
                self.emp_table.delete(*self.emp_table.get_children())
                for row in rows:
                    query2 = "SELECT Name, Profile, Department FROM employee WHERE EMPID = %s;"
                    vals = (row[0],)
                    mycursor.execute(query2, vals)

                    results = mycursor.fetchall()

                    self.emp_table.insert(parent='', index='end', text="Employee Salary", values=[row[0],results[0][0],results[0][1],results[0][2],row[1],row[2],row[3],row[4],row[5],row[6]])
                
                mydb.commit()

            else:
                query = "SELECT * FROM employee WHERE " + str(self.search_by.get()) + " LIKE '%" + str(self.serach_text.get()) + "%';"
                mycursor.execute(query)

                rows = mycursor.fetchall()
                self.emp_table.delete(*self.emp_table.get_children())
                for row in rows:
                    print(row)
                    query2 = "SELECT Overtime_Rs, Conveyance_Rs, Deduction_Rs, Net_Salary_Rs, Last_Updated FROM salary WHERE EMPID = %s;"
                    vals = (row[0],)
                    mycursor.execute(query2, vals)

                    results = mycursor.fetchall()

                    self.emp_table.insert(parent='', index='end', text="Employee Salary", values=[row[0],row[1],row[7],row[8],row[9],results[0][0],results[0][1],results[0][2],results[0][3],results[0][4]])
                
                mydb.commit()

        except Exception as Ex:
            messagebox.showerror("Error", str(Ex))

    def clear(self):
        self.search_by.set("Select")
        self.serach_text.set("")

        self.ShowPayrollList()