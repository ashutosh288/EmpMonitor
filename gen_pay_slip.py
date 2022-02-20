from tkinter import *
from PIL import ImageTk
from tkinter import ttk, messagebox
import mysql.connector

class GenPaySlip:
    def __init__(self, win):
        self.win = win
        self.win.geometry("600x500")
        self.win.title("Update Employee Details")
        self.win.configure(bg="#ffffff")
        self.win.focus_force()

        txt = '''
\t\t\t  ABC Infotech Pvt Limited 
\t     Ganesh Tower Gandhi Nagar, Surat, Gujrat - 556625

\t\t\t\tPAY SLIP
==========================================================================
Employee ID     : 001                  Profile     : Software Engineer
Employee Name   : Abhinav Srivastav	   Department  : Software Development 
--------------------------------------------------------------------------
Basic Salary    : 21000 Rs
Overtime        : 600   Rs
Conveyance      : 2000  Rs 
--------------------------------------------------------------------------
Total           : 23600 Rs
--------------------------------------------------------------------------
Deduction 		: 2400  Rs
--------------------------------------------------------------------------
                                            Net Salary To Pay : 21200 Rs
==========================================================================



Date : 27-06-2009                                     Authority Signature
'''

        title = Label(self.win,text="Update Employee Details", font=('Calibari',11),fg="#ffffff",bg='#0d6efd').place(x=0,y=0,height=30,width=600)

        bill_frame = Text(self.win, background="#ffffff", border=2)
        bill_frame.place(x=0,y=31,height=470,width=600)

        bill_frame.insert(END, "\t\t\t  ABC Infotech Pvt Limited\n")
        bill_frame.insert(END, "\t     Ganesh Tower Gandhi Nagar, Surat, Gujrat - 556625\n\n")
        bill_frame.insert(END, "\t\t\t\tPAY SLIP\n")
        bill_frame.insert(END, "==========================================================================\n")
        bill_frame.insert(END, f"Employee ID     : {entry_values[0]}\t\t\t\t\tProfile     : {entry_values[2]}\n")
        bill_frame.insert(END, f"Employee Name   : {entry_values[1]}\t\t\t\t\tDepartment  : {entry_values[3]}\n")
        bill_frame.insert(END, f"--------------------------------------------------------------------------\n")
        bill_frame.insert(END, f"Basic Salary    : {entry_values[4]}\tRs\n")
        bill_frame.insert(END, f"Overtime        : {entry_values[5]}\t\t Rs\n")
        bill_frame.insert(END, f"Conveyance      : {entry_values[6]}\t Rs\n")
        bill_frame.insert(END, f"--------------------------------------------------------------------------\n")

        total = float(entry_values[4])+float(entry_values[5])+float(entry_values[6])

        bill_frame.insert(END, f"Total           : {total}0\tRs\n")
        bill_frame.insert(END, f"--------------------------------------------------------------------------\n")
        bill_frame.insert(END, f"Deduction 		: {entry_values[7]}\t Rs\n")
        bill_frame.insert(END, f"--------------------------------------------------------------------------\n")
        bill_frame.insert(END, f"\t\t\t\t\t  Net Salary To Pay : {entry_values[8]} Rs\n")
        bill_frame.insert(END, f"==========================================================================\n\n\n\n")
        bill_frame.insert(END, f"Date : {entry_values[9][0:10]}                                    Authority Signature")
        
        self.win.mainloop()

if __name__ == '__main__':
    root = Tk()
    new_win = GenPaySlip(root)