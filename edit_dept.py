from tkinter import *
from PIL import ImageTk
from tkinter import ttk, messagebox
import mysql.connector

class UpdateDepts:
    def __init__(self, win, values):
        self.win = win   
        self.win.geometry("370x340")
        self.win.title("Edit Department")
        self.win.configure(bg="#7ebaef")
        self.win.focus_force()  

        self.values = values

        self.dept_name = StringVar()
        self.dept_head = StringVar()

        self.dept_name.set(values[1])
        self.dept_head.set(values[2])

        tittle_label = Label(self.win, background="#7ebaef", text="Edit Department", font=('Calibari',12, 'bold'))
        tittle_label.place(x=10, y=10)

        dept_name_label = Label(self.win,font=('Calibari',10), text="Department Name",bg="#7ebaef").place(x=20,y=60,height=20)
        dept_name_entry = Entry(self.win,font=('Calibari',10),bg="#fffff0", textvariable=self.dept_name).place(x=140,y=60,width=200,height=20)

        dept_head_label = Label(self.win,font=('Calibari',10), text="Department Head",bg="#7ebaef").place(x=20,y=100,height=20)
        dept_head_entry = Entry(self.win,font=('Calibari',10),bg="#fffff0", textvariable=self.dept_head).place(x=140,y=100,width=200,height=20)

        submit_btn = Button(self.win, text="Update", font=('Cilibari', 10),bg="#dc3545", fg="#ffffff", command=self.updateDept).place(x=130,y=160,height=25,width=120)
        
        self.win.mainloop()

    #========================================================================================================================================#
    # functions

    def updateDept(self):
        try:
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="root",
                database="empmangsys"
            )
            mycursor = mydb.cursor()

            query = "UPDATE department SET Name=%s, Department_Head=%s;" 
            vals = (self.dept_name.get(), self.dept_head.get(),)

            mycursor.execute(query, vals)

            mydb.commit()

            messagebox.showinfo("Done", "Department Updated Successfully", parent=self.win)

        except Exception as Ex:
            messagebox.showerror("Error", f"Error Occured Due To {Ex}", parent=self.win)