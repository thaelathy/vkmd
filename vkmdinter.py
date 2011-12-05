#-=-coding:utf-8-=-
from vkmd import *

from Tkinter import *

class App:

    def __init__(self, master):

        frame = Frame(master)
        frame.pack()

        email_label = Label(frame, text="User Name")
        email_label.grid(row=0)

        self.email_entry = Entry(frame, width=30)
        self.email_entry.grid(row=0, column=1)

        passw_label = Label(frame, text="Password")
        passw_label.grid(row=1)

        self.passw_entry = Entry(frame, width=30)
        self.passw_entry.grid(row=1, column=1)

        uid_label = Label(frame, text="Who")
        uid_label.grid(row=2)

        self.uid_entry = Entry(frame, width=30)
        self.uid_entry.grid(row=2, column=1)

        self.hi_there = Button(frame, text="GO", fg="red", command=self.go)
        self.hi_there.grid(row = 3)

    def go(self):
        print "hi there, everyone!"
        print self.email_entry.get()
        email = self.email_entry.get()
        print self.passw_entry.get()
        passw = self.passw_entry.get()
        print self.uid_entry.get()
        uid = self.uid_entry.get()

        main(email, passw, uid)

root = Tk()

app = App(root)

root.mainloop()
