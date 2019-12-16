from tkinter import *
from tkinter.ttk import *
import pyodbc
from functions_ import Esquema
#import condicoes
import programa_gabriele
from programa_gabriele import *
from database import *
import pandas.io.sql



class welcome():
    def __init__(self, main_frame):    
        self.server = DoubleVar()
        self.database = DoubleVar()
        self.user = DoubleVar()
        self.senha = DoubleVar()

        self.main_frame = main_frame
        self.main_frame.title("Welcome Page")
        self.main_frame.geometry("620x426+305+194")

        label1 = Label(self.main_frame, text="Server")
        label1.grid(row=1, column=1)

        label2 = Label(self.main_frame, text="Database")
        label2.grid(row=2, column=1)

        label3 = Label(self.main_frame, text="UID")
        label3.grid(row=3, column=1)

        label4 = Label(self.main_frame, text="PWD")
        label4.grid(row=4, column=1)

        entry1 = Entry(self.main_frame, textvariable=self.server)
        entry1.grid(row=1, column=2)

        entry2 = Entry(self.main_frame, textvariable=self.database)
        entry2.grid(row=2, column=2)

        entry3 = Entry(self.main_frame, textvariable=self.user)
        entry3.grid(row=3, column=2)

        entry4 = Entry(self.main_frame, textvariable=self.senha)
        entry4.grid(row=4, column=2)

        button1 = Button(self.main_frame, text="Continue to the next page", command=self.call_tela2)
        button1.grid(row=7, column=1)

    def call_tela2(self):
        self.main_frame.destroy()
        tcc_gabriele()

main_frame = Tk()
welcome(main_frame)
main_frame.mainloop()
#tcc_gabriele()