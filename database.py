import pyodbc
listaggg = []
schema_table = []
gablista = []
arraylist = []
where = []

Server= 'DESKTOP-1JSMTF2\SQLSERVER'
#Database= 'tpc-h'
Database= 'AdventureWorks'
UID= 'sa'
PWD= 'Gab2019'

str_connection = 'Driver={%s};Server=%s;Database=%s;UID=%s;PWD=%s' %(pyodbc.drivers()[0], Server, Database, UID, PWD)
con = pyodbc.connect(str_connection)
cur = con.cursor()
# Seleção das telas do banco para iniciar a interface


cur = con.cursor()
query = (
"select TABLE_NAME, CASE WHEN c.coun>1 THEN TABLE_SCHEMA ELSE '' END as TABLE_SCHEMA, c.coun from INFORMATION_SCHEMA.TABLES, (select COUNT(DISTINCT(TABLE_SCHEMA)) as coun from INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE') as c WHERE TABLE_TYPE = 'BASE TABLE' ORDER BY TABLE_NAME"
)

cur.execute(query)
     
dadosTable = cur.fetchall()
for dados in dadosTable:
    if len(dados) > 0:
        listaggg.append(dados[0])
        if dados[2]>1:
            schema_table.append(dados[1]+"."+dados[0])
        else:
            schema_table.append(dados[0])


