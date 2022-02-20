from tkinter import *
from PIL import ImageTk
from tkinter import ttk, messagebox
from add_emp import AddEmp
from update_emp_details import UpdateEmp
import mysql.connector


class EmpSection:
    def __init__(self, win):
        self.win = win
        self.win.geometry("850x440+170+230")
        self.win.title("Employees")
        self.win.configure(bg="#ffffff")
        self.win.focus_force()

        self.win.bind('<FocusIn>', self.refresh)

        self.search_by = StringVar()
        self.serach_text = StringVar()

        title = Label(self.win, text="Employees List", font=(
            'Calibari', 11), fg="#ffffff", bg='#0d6efd').place(x=0, y=0, height=30, width=850)

        search_frame = LabelFrame(
            self.win, text="Search Employee", font=('Calibari', 10), bg="#ffffff")
        search_frame.place(x=10, y=50, width=500, height=70)

        search_options = ttk.Combobox(search_frame,textvariable=self.search_by, value=(
            'Select', 'EMPID', 'Name', 'Department'), state='readonly')
        search_options.place(x=10, y=10, width=110, height=20)
        search_options.current(0)

        search_input = Entry(search_frame,textvariable=self.serach_text, font=('Calibari', 10), bg="#fffff0").place(
            x=130, y=10, width=200, height=20)
        search_btn = Button(search_frame, text="Search", font=(
            'Cilibari', 10), bg="#198754", command=self.searchEmp).place(x=340, y=10, height=20, width=70)
        clr_btn = Button(search_frame, text="Clear", font=(
            'Cilibari', 10),bg="#6c757d", fg="#ffffff", command=self.clear).place(x=420, y=10, height=20, width=70)

        add_emp = Button(self.win, text="+ Add Employee", font=('Cilibari', 10),
                         bg="#0d6efd", command=self.addEmp).place(x=520, y=88, height=30, width=120)
        update_btn = Button(self.win, text="Update", font=('Cilibari', 10), bg="#dc3545",
                            fg="#ffffff", command=self.UpdateEmp).place(x=650, y=88, height=30, width=90)
        delete_btn = Button(self.win, text="Delete", font=(
            'Cilibari', 10), bg="#ffc107", command=self.delEmployee).place(x=745, y=88, height=30, width=90)

        # list_frame1 = Frame(self.win, border=2, background="#6c757d").place(x=10,y=100,height=280,width=770)

        scrolly = Scrollbar(self.win, orient=VERTICAL)
        scrollx = Scrollbar(self.win, orient=HORIZONTAL)

        self.emp_table = ttk.Treeview(self.win, columns=('emp_id', 'name', 'dob', 'gender', 'mob', 'email', 'doj',
                                 'profile', 'dept', 'salary', 'conveyance'), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)

        scrolly.place(x=820, y=140, height=280)
        scrolly.config(command=self.emp_table.yview)

        scrollx.place(x=10, y=404, width=812)
        scrollx.config(command=self.emp_table.xview)

        self.emp_table.heading("emp_id", text="Employee ID")
        self.emp_table.heading("name", text="Name")
        self.emp_table.heading("dob", text="D.O.B")
        self.emp_table.heading("gender", text="Gender")
        self.emp_table.heading("mob", text="Mobile No.")
        self.emp_table.heading("email", text="E-mail")
        self.emp_table.heading("doj", text="D.O.J")
        self.emp_table.heading("profile", text="Profile")
        self.emp_table.heading("dept", text="Department")
        self.emp_table.heading("salary", text="Salary(in Rs)")
        self.emp_table.heading("conveyance", text="Conveyance(in Rs)")
        self.emp_table["show"] = "headings"

        self.emp_table.column("emp_id", width=90, minwidth=90, anchor=CENTER)
        self.emp_table.column("name", width=180, minwidth=180, anchor=CENTER)
        self.emp_table.column("dob", width=80, minwidth=80, anchor=CENTER)
        self.emp_table.column("gender", width=80, minwidth=80, anchor=CENTER)
        self.emp_table.column("mob", width=100, minwidth=80, anchor=CENTER)
        self.emp_table.column("email", width=190, minwidth=180, anchor=CENTER)
        self.emp_table.column("doj", width=80, minwidth=80, anchor=CENTER)
        self.emp_table.column("profile", width=180, minwidth=180, anchor=CENTER)
        self.emp_table.column("dept", width=180, minwidth=180, anchor=CENTER)
        self.emp_table.column("salary", width=90, minwidth=90, anchor=CENTER)
        self.emp_table.column("conveyance", width=90, minwidth=120, anchor=CENTER)

        self.showEmployee()

        self.emp_table.place(x=10, y=140, height=264, width=812)
        self.emp_table.bind('<ButtonRelease-1>', self.updateEmployee)
        self.vals_row_focus = []

        self.win.mainloop()

    def addEmp(self):
        new_obj = Toplevel(self.win)
        new_win = AddEmp(new_obj)

    def UpdateEmp(self):
        if len(self.vals_row_focus) <= 0:
            messagebox.showerror("Error", "Please Choose a Entry to Update", parent=self.win)
            return
        else:
            vals_row_focus_obj = self.vals_row_focus
            new_obj = Toplevel(self.win)
            new_win = UpdateEmp(new_obj, vals_row_focus_obj)

    #=========================================================================================================#
    # functions

    def refresh(self, ev):
        self.showEmployee()

    def showEmployee(self):
        try:
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="root",
                database="empmangsys"
            )
            mycursor = mydb.cursor()

            query = "SELECT * FROM employee;"
            mycursor.execute(query)

            rows = mycursor.fetchall()
            self.emp_table.delete(*self.emp_table.get_children())
            for row in rows:
                self.emp_table.insert(parent='', index='end', text="Employee", values=row)

            mydb.commit()

        except Exception as Ex:
            messagebox.showerror("Error", str(Ex))

    def updateEmployee(self,ev):
        row = self.emp_table.focus()
        content = (self.emp_table.item(row))
        vals = content['values']
        self.vals_row_focus = vals
        print(self.vals_row_focus)

    def delEmployee(self):
        try:
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="root",
                database="empmangsys"
            )
            mycursor = mydb.cursor()

            row = self.emp_table.focus()
            content = (self.emp_table.item(row))
            vals = content['values']

            if len(vals) <= 0:
                messagebox.showerror("Error", "Please Choose a Entry to Delete", parent=self.win)
                return
            else:
                '''query="DELETE FROM employee WHERE EMPID=7;"'''

                opt = messagebox.askyesno("Delete", "Are You Sure Want To Delete", parent=self.win)

                if opt==True:
                    empID = vals[0]
                    query1 = "DELETE FROM salary WHERE EMPID=%s;"

                    query2 = "DELETE FROM employee WHERE EMPID=%s;"

                    val = (empID,)
                    
                    mycursor.execute(query1, val)
                    mycursor.execute(query2, val)
                    
                    mydb.commit()

                    messagebox.showinfo("Done", "Employee Delete Successfully", parent=self.win)
                    self.showEmployee()

        except Exception as Ex:
            messagebox.showerror("Error", str(Ex))
        
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

            else:
                query = "SELECT * FROM employee WHERE " + str(self.search_by.get()) + " LIKE '%" + str(self.serach_text.get()) + "%';"
                mycursor.execute(query)

                rows = mycursor.fetchall()
                self.emp_table.delete(*self.emp_table.get_children())
                for row in rows:
                    self.emp_table.insert(parent='', index='end', text="Employee", values=row)

                mydb.commit()

        except Exception as Ex:
            messagebox.showerror("Error", str(Ex))

    def clear(self):
        self.search_by.set("Select")
        self.serach_text.set("")

        self.showEmployee()

if __name__ == '__main__':
    root = Tk()
    new_win = EmpSection(root)