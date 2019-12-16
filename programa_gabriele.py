from tkinter import *
from tkinter.ttk import *
#import tkinter as Tk
from functions_ import Esquema
#import condicoes

from database import *
import pandas.io.sql

# Labels da topbar:

class tcc_gabriele:
    gablista = []
    arraylist = []
    lista = listaggg.copy()
    group_func = []
    condicoes = []
    lista_tabelas_selecionadas = []
    def __init__(self):
        
        main_frame = Tk()
        self.main_frame = main_frame

        self.main_frame.title("TCC_Gabriele")
        self.main_frame.geometry("620x426+305+194")

        self.label_lista_de_tabelas = Label(main_frame)
        self.label_lista_de_tabelas.place(relx=0.015, rely=0.012, height=35, width=135)
        self.label_lista_de_tabelas.configure(text="Lista de tabelas:")

        self.label_lista_de_colunas = Label(main_frame)
        self.label_lista_de_colunas.place(relx=0.217, rely=0.012, height=35, width=145)
        self.label_lista_de_colunas.configure(text="Lista de colunas:")

        self.label_lista_de_colunas_selecionadas = Label(main_frame)
        self.label_lista_de_colunas_selecionadas.place(relx=0.415, rely=0.0142, height=31, width=155)
        self.label_lista_de_colunas_selecionadas.configure(text="Colunas selecionadas:")

        self.label_lista_de_funcoes = Label(main_frame)
        self.label_lista_de_funcoes.place(relx=0.617, rely=0.0172, height=31, width=155)
        self.label_lista_de_funcoes.configure(text="Funções:")
        # Declaração dos objetos

        # Exibe lista de tabelas do banco
        self.listTable = Listbox(main_frame)
        self.listTable.place(relx=0.015, rely=0.07, relheight=0.38, relwidth=0.19)

        for line in range(len(schema_table)):
            tabela = schema_table[line]
            self.listTable.insert(END, str(tabela))# popula a lista de tabelas

        self.scrol1 = Scrollbar(self.listTable)
        self.scrol1.pack(side=RIGHT,fill=Y)
        self.scrol1.config(command=self.listTable.yview)
        self.listTable.config(yscrollcommand=self.scrol1.set)

        # Exibe lista de colunas por tabela
        self.mylistcolum = Listbox(main_frame)
        self.mylistcolum.place(relx=0.217, rely=0.07, relheight=0.38, relwidth=0.19)

        self.scrol2 = Scrollbar(self.mylistcolum)
        self.scrol2.pack(side=RIGHT, fill=Y)
        self.scrol2.config(command=self.mylistcolum.yview)
        self.mylistcolum.config(yscrollcommand=self.scrol2.set)

        # Exibe colunas selecionadas
        self.listselected = Listbox(main_frame, exportselection=0)
        self.listselected.place(relx=0.417, rely=0.07, relheight=0.38, relwidth=0.19)

        self.scrol3 = Scrollbar(self.listselected)
        self.scrol3.pack(side=RIGHT, fill=Y)
        self.scrol3.config(command=self.listselected.yview)
        self.listselected.config(yscrollcommand=self.scrol3.set)

        # Exibe lista de funções
        self.mylistfunctions = Listbox(main_frame, exportselection=0)
        self.mylistfunctions.place(relx=0.617, rely=0.07, relheight=0.25, relwidth=0.19)
        self.mylistfunctions.insert(END, "Avg", "Sum", "Count", "Max", "Min", "(nenhuma)")
        self.mylistfunctions.focus()

        self.scrol4 = Scrollbar(self.mylistfunctions)
        self.scrol4.pack(side=RIGHT, fill=Y)
        self.scrol4.config(command=self.mylistfunctions.yview)
        self.mylistfunctions.config(yscrollcommand=self.scrol4.set)


        # BOTÕES

        # Deleta iten da lista de colunas selecionada
        self.deleta_table = Button(main_frame, command= lambda: Esquema.remove(self.listselected, self.group_func, self.lista_tabelas_selecionadas))
        self.deleta_table.place(relx=0.627, rely=0.34, height=44, width=107)
        self.deleta_table.configure(text='Deleta coluna')

        # Executa consulta SQL
        self.exec_consulta = Button(main_frame, command= lambda: Esquema.readfromdatabase(self.main_frame, self.group_func, self.condicoes, self.lista_tabelas_selecionadas))
        self.exec_consulta.place(relx=0.815, rely=0.19, height=44, width=110)
        self.exec_consulta.configure(text='Executa consulta')

        # Botão para acionar condição
        self.add_condicao = Button(main_frame, command= lambda: Esquema.condicoes(self.lista_tabelas_selecionadas, self.condicoes))
        self.add_condicao.place(relx=0.815, rely=0.07, height=44, width=110)
        self.add_condicao.configure(text='Adiciona condicao')

        ######### AÇÕES #############################
        self.listTable.bind("<Double-Button-1>", lambda x: Esquema.getColumList(self.listTable, self.mylistcolum, self.gablista, self.lista))
        self.mylistcolum.bind("<Double-Button-1>", lambda x: Esquema.ShowColumSelected(self.mylistcolum,self.mylistfunctions,self.listselected, self.group_func, self.gablista, self.lista_tabelas_selecionadas))

        main_frame.mainloop()

