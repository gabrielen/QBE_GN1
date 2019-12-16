# Importações
from tkinter import *
from tkinter.ttk import *
import database
from database import *
import pandas


class Esquema:

    def getColumList(listTable, mylistcolum, gablista, lista):
        lista_coluna = []

        if listTable.size() > 0:
            texto = listTable.curselection()[0]  # pega a posição do clique (a seleção)
            tabela = lista[texto]  # pega o nome da tabela que foi selecionada
            tab_from = listTable.get(texto)
            cur.execute("select COLUMN_NAME from information_schema.columns where table_name ='" + tabela + "'")
            dadosColum = cur.fetchall()
            # adiociono a lista dadosColum na lista lista para que o formato de exibição não fique como: ('ps_partkey', )
            for dados in dadosColum:
                if len(dados) > 0:
                    lista_coluna.append(dados[0])

            # deleta os itens da listbox para repopular com as colunas da nova tabela selecionada
            mylistcolum.delete(0, 'end')

            # Popula a lista de colunas
            for line in lista_coluna:
                mylistcolum.insert(END, str(line))
            gablista.append(tab_from)

    def ShowColumSelected(mylistcolum, mylistfunctions, listselected, group_func, gablista, lista_tabelas_selecionadas):

        #group_by_colunas = []
        if mylistcolum.size() > 0:
            texto = mylistcolum.curselection()[0]
            coluna = mylistcolum.get(texto)
            lista_tabelas_selecionadas.append(gablista[-1])

            if len(mylistfunctions.curselection()) > 0:

                texto = mylistfunctions.curselection()[0]
                funcao = mylistfunctions.get(texto)

                if funcao == "(nenhuma)":
                    campo = coluna
                else:
                    campo = funcao + "(" + coluna + ")"
                    group_func.append(campo)
            else:
                campo = coluna
            listselected.insert(END, str(campo))
            arraylist.append(campo)

    def remove(listselected, group_func, lista_tabelas_selecionadas):

        if listselected.size() > 0:
            teste = listselected.curselection()[0]
            coluna_removida = listselected.get(teste)  # pega a posição do clique (a seleção)
            arraylist.remove(coluna_removida)
            lista_tabelas_selecionadas.remove(lista_tabelas_selecionadas[teste])

            if coluna_removida in group_func:
                group_func.remove(coluna_removida)
            else: pass
            listselected.delete(ACTIVE)

    def readfromdatabase(main_frame, group_func, condicoes, lista_tabelas_selecionadas):
        table = []
        select_columns = []
        result_frame = Frame(main_frame)
        result_frame.place(relx=0.016, rely=0.475, relheight=0.500, relwidth=0.968)
        result_frame.configure(relief='groove', borderwidth="1")

        label_resultados_string = Label(result_frame, text="Resultado da consulta ao banco:",
                                        background="#d9d9d9").grid(column=0, row=1)


        # Cria o FROM
        for x in lista_tabelas_selecionadas:
            if x not in table:
                table.append(x)
        str_tables = ', '.join(table)

        # Ajusta os campos do SELECT para que apareçam as tabelas origem
        for y in range(len(arraylist)):

            if arraylist[y] in group_func:
                ind = arraylist[y].find('(')+1
                ind2 = arraylist[y][ind:-1]
                select_columns.append(arraylist[y][:ind] + lista_tabelas_selecionadas[y] + '.' + ind2+')')
            else:
                select_columns.append(lista_tabelas_selecionadas[y] + '.' + arraylist[y])
        columns = ', '.join(select_columns)

        # Retorna as condições de junção entre tabelas
        lista_join = Esquema.joins(lista_tabelas_selecionadas)
        str_join = ' and '.join(lista_join)

        # Declara a consulta inicial, sem o campo WHERE
        qry = columns + ' from ' + str_tables

        # Cria o campo WHERE, atribuindo valores definidos nas condições e nos joins
        if len(condicoes) > 0 and condicoes != ['']:
            print('condicoes: ',condicoes)
            cond = ' '.join(condicoes)
            print('cond: ', cond)
            if len(str_join)>0:
                qry = qry + ' where ' + cond + ' and ' + str_join
            else:
                qry = qry + ' where ' + cond
        else:
            if len(str_join) > 0:
                qry = qry + ' where ' + str_join

        # Cria GROUP BY em caso de haver alguma agregação
        group_by_colunas = arraylist.copy()
        if len(group_func) > 0 and len(group_by_colunas) >1:
            for item in group_func:
                group_by_colunas.remove(item)
            group_by = ', '.join(group_by_colunas)
            qry = qry + ' group by ' + group_by
        else:
            pass

        # Executa consulta para exibição dos 15 primeiros resultados.
        print('qry final : select ', qry)
        querypandaExibe = pandas.io.sql.read_sql('select TOP 10 ' + qry, con)
        # Executa consulta para exportação em csv
        querypandaTXT = pandas.io.sql.read_sql('select ' + qry, con)

        # exporta resultado da consulta_2 pra csv
        querypandaTXT.to_csv('testecomTELA.txt', encoding='utf-8')

        # exibe resultado da consulta_1:
        linhas = len(querypandaExibe)
        colunas = len(querypandaExibe.iloc[0])
        for index in range(linhas):
            for indey in range(colunas):
                titulo = Label(result_frame, text=arraylist[indey]).grid(row=2, column=indey)
                # titulo.place(relx=0.9, rely=0.023, relheight=0.38, relwidth=0.19)
                rows = Label(result_frame, text=querypandaExibe.iloc[index, indey]).grid(
                    row=index + 3, column=indey)

    def condicoes(lista_tabelas_selecionadas, condicoes):
        second_frame = Tk()
        second_frame.title("Condições")
        second_frame.geometry("420x276+305+194")
        #####DEFINIÇÃO DE VARIÁVEIS#########################################################
        list = []
        where_itens = []
        tables = []
        v = StringVar(master=second_frame)
        g = StringVar(master=second_frame)
        n = StringVar(master=second_frame)

        #####RADIOBUTTONS###################################################################
        Radiobutton(second_frame, text="=", value="=", variable=v).place(relx=0.02, rely=0.05)
        Radiobutton(second_frame, text=">", value=">", variable=v).place(relx=0.14, rely=0.05)
        Radiobutton(second_frame, text="<", value="<", variable=v).place(relx=0.26, rely=0.05)
        Radiobutton(second_frame, text=">=", value=">=", variable=v).place(relx=0.38, rely=0.05)
        Radiobutton(second_frame, text="<=", value="<=", variable=v).place(relx=0.50, rely=0.05)
        Radiobutton(second_frame, text="<>", value="<>", variable=v).place(relx=0.62, rely=0.05)
        Radiobutton(second_frame, text="!=", value="!=", variable=v).place(relx=0.74, rely=0.05)
        Radiobutton(second_frame, text="like", value="like", variable=v).place(relx=0.86, rely=0.05)
        and_ = Radiobutton(second_frame, text="e", value="and", variable=g)
        and_.place(relx=0.62, rely=0.15)
        and_.configure(state=DISABLED)
        or_ = Radiobutton(second_frame, text="ou", value="or", variable=g)
        or_.place(relx=0.74, rely=0.15)
        or_.configure(state=DISABLED)

        ###ENTRY's#########################################################################
        label_lista_de_colunas_selecionadas = Label(second_frame)
        label_lista_de_colunas_selecionadas.place(relx=0.13, rely=0.23, height=31, width=155)
        label_lista_de_colunas_selecionadas.configure(text="Dado: ")
        dado = Entry(second_frame)
        dado.place(relx=0.13, rely=0.33, height=25, width=310)

        label_lista_de_colunas_selecionadas = Label(second_frame)
        label_lista_de_colunas_selecionadas.place(relx=0.13, rely=0.45)
        label_lista_de_colunas_selecionadas.configure(text="Condições: ")
        show_condition = Entry(second_frame)
        show_condition.place(relx=0.13, rely=0.55, height=25, width=310)

        ###INSTÂNCIAS#######################################################################
        if len(lista_tabelas_selecionadas) > 0:
            for item in lista_tabelas_selecionadas:
                if item not in tables:
                    tables.append((item.split('.'))[-1])


            tables_str = "', '".join(tables)
            qry = ("select TABLE_SCHEMA, TABLE_NAME, COLUMN_NAME from information_schema.columns where table_name in ('%s')" % (tables_str))
            cur.execute(qry)
            columns_table = cur.fetchall()

        for data in columns_table:
            if len(data) > 0:
                list.append(data[2])
                where_itens.append(data[0]+'.'+data[1]+'.'+data[2])


        if len(condicoes)>0:
            condicoes_str = ' '.join(condicoes)
            show_condition.delete(0, 'end')
            show_condition.insert(END, condicoes_str)

        ###COMBOBOX#########################################################################
        combo = Combobox(second_frame, values= list, height=5)
        combo.place(relx=0.07, rely=0.15)
        combo.set("Coluna")

        ###BOTÕES###########################################################################
        add = Button(second_frame, command=lambda : adiciona_condicao(v,g, dado, combo, condicoes, and_, or_, show_condition, where_itens))
        add.place(relx=0.16, rely=0.7, height=40, width=80)
        add.configure(text="Adiciona")

        delete = Button(second_frame, command= lambda: del_condition(show_condition))
        delete.place(relx=0.41, rely=0.7, height=40, width=80)
        delete.configure(text="Deleta")

        exit = Button(second_frame, command=lambda: exit_button(condicoes))
        exit.place(relx=0.66, rely=0.7, height=40, width=80)
        exit.configure(text="Ok")

        def adiciona_condicao( v, g, dado, combo, condicoes, and_, or_, show_condition, where_itens):
            condicao_list = []
            condicao = g.get() + " " + where_itens[combo.current()] + " " + v.get() + " " + dado.get()
            condicao_list.append(condicao)
            condicoes.append(condicao)
            and_.configure(state=NORMAL)
            and_.invoke()
            or_.configure(state=NORMAL)
            #condicoes_str = ' '.join(condicao_list)
            condicoes_str = ' '.join(condicoes)
            show_condition.delete(0, 'end')
            show_condition.insert(END, condicoes_str)

        def exit_button(condicoes):
            condicoes.clear()
            condicoes.append(show_condition.get())
            second_frame.destroy()

        def del_condition(show_condition):
            condicoes.clear()
            show_condition.delete(0, 'end')
            and_.configure(state=DISABLED)
            or_.configure(state=DISABLED)
            g.set('')

    def joins(lista_tabelas_selecionadas):
        lista = []
        sublista = []
        join_relation = []
        lista_aux = []
        query_fk = 'SELECT OBJECT_NAME(f.parent_object_id) AS table_name, COL_NAME(fc.parent_object_id, fc.parent_column_id) AS constraint_column_name, OBJECT_NAME (f.referenced_object_id) AS referenced_object, COL_NAME(fc.referenced_object_id, fc.referenced_column_id) AS referenced_column_name, is_disabled FROM sys.foreign_keys AS f INNER JOIN sys.foreign_key_columns AS fc ON f.object_id = fc.constraint_object_id WHERE is_disabled = 0'
        table_constrains = pandas.io.sql.read_sql(query_fk, con)

        linhas = len(table_constrains)
        colunas = len(table_constrains.iloc[0])

        #trata lista_tabelas_selecionadas
        for item in lista_tabelas_selecionadas:
            texto = (item.split('.'))[-1]
            lista_aux.append(texto)

        #monta possiveis combinações entre as tabelas selecionadas
        if len(lista_aux) > 1:
            for item in range(len(lista_aux)):
                for item2 in range(len(lista_aux)):
                    if lista_aux[item] == lista_aux[item2]:
                        pass
                    elif lista_aux[item] + lista_aux[item2] in lista:
                        pass
                    else:
                        lista.append(lista_aux[item] + lista_aux[item2])
                        for index in range(linhas):
                            if table_constrains.iloc[index, 0] == lista_aux[item] and table_constrains.iloc[index, 2] == lista_aux[item2]:
                                join_relation.append(
                                    lista_aux[item] + '.' + table_constrains.iloc[index, 1] + ' = ' +
                                    lista_aux[item2] + '.' + table_constrains.iloc[index, 3])
                                print(lista_aux[item] + '.' + table_constrains.iloc[index, 1] + ' = ' +
                                    lista_aux[item2] + '.' + table_constrains.iloc[index, 3])
        else:
            pass
        return(join_relation)