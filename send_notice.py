from tkinter import *
from PIL import ImageTk
from tkinter import ttk
import smtplib
from Passwords import pswds

class SendNotice:
    def __init__(self, win):
        self.win = win
        self.win.geometry("490x470+540+150")
        self.win.title("Send Notice")
        self.win.configure(bg="#ffffff")
        self.win.focus_force()

        self.sender_mail = StringVar()
        self.recipient_mail = StringVar()

        title = Label(self.win,text="Send Notice", font=('Calibari',11),fg="#ffffff",bg='#0d6efd').place(x=0,y=0,height=30,width=490)

        self.send_notice_frame = LabelFrame(self.win, text="Send Notice",font=('Calibari',10),bg="#ffffff")
        self.send_notice_frame.place(x=20,y=40,width=450,height=410)

        self.sender_label = Label(self.send_notice_frame,font=('Calibari',10), text="From :",bg="#ffffff",).place(x=20,y=20,height=20)
        self.sender_entry = Entry(self.send_notice_frame,font=('Calibari',10),bg="#fffff0", textvariable=self.sender_mail).place(x=95,y=20,width=320,height=20)

        self.recipient_label = Label(self.send_notice_frame,font=('Calibari',10), text="To :",bg="#ffffff").place(x=20,y=60,height=20)
        self.recipient_entry = Entry(self.send_notice_frame,font=('Calibari',10),bg="#fffff0", textvariable=self.recipient_mail).place(x=95,y=60,width=320,height=20)

        self.subject_label = Label(self.send_notice_frame,font=('Calibari',10), text="Subject :",bg="#ffffff").place(x=20,y=100,height=20)
        self.subject_entry = Text(self.send_notice_frame,font=('Calibari',10),bg="#fffff0")
        self.subject_entry.place(x=95,y=100,width=320,height=50)

        self.message_label = Label(self.send_notice_frame,font=('Calibari',10), text="Message :",bg="#ffffff").place(x=20,y=170,height=20)
        self.message_entry = Text(self.send_notice_frame,font=('Calibari',10),bg="#fffff0")
        self.message_entry.place(x=95,y=170,width=320,height=150)

        self.send_btn = Button(self.win, text="Send Mail", font=('Cilibari', 10),bg="#0d6efd",command=self.SendEmail).place(x=210,y=400,height=25,width=120)

        self.win.mainloop()

    #===========================================================================================================================#
    # functions

    def SendEmail(self):
        if self.sender_mail.get() == "" or self.recipient_mail.get() == "" or self.subject_entry.get(1.0, ) == "" or self.message_entry.get(1.0, ) == "":
            messagebox.showerror("Error", "Fill All Required Details", parent=self.win)
        else:
            server = smtplib.SMTP("smtp.gmail.com",587)
            server.starttls()

            username_list = pswds.keys()

            if self.sender_mail.get() not in username_list:
                print("Enter Valid Email Address")
                return

            username = str(self.sender_mail.get())
            password = pswds[username]

            server.login(username, password)

            subject = str(self.subject_entry.get(1.0, END))
            text = str(self.message_entry.get(1.0, END))

            message = f"Subject:{subject}\n\n{text}"

            server.sendmail(str(self.sender_mail.get()),str(self.recipient_mail.get()), message)
            print("Mail Sends Successfully....")

            server.quit()

if __name__ == "__main__":
    root = Tk()
    new_win = SendNotice(root)