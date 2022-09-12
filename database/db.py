import pymysql

connection = pymysql.connect(host="localhost",user="root",passwd="",database="firstcovid" )
cursor = connection.cursor()

client = "Comprehensive"
requsition = "CPAF789"
name = "Mike Jackson"

insert1 = "INSERT INTO ddlupload_record(Client, Requisition_Number, Patient_Name) VALUES('{}', '{}', '{}' );".format(client,requsition,name)
insert2 = "INSERT INTO ddlupload_record(Client, Requisition_Number, Patient_Name) VALUES('Comprehensive Pain', 'CPCC128', 'Alex John' );"
cursor.execute(insert1)
fetch = "SELECT Requisition_Number FROM ddlupload_record ORDER BY ID DESC LIMIT 0, 1"
cursor.execute(fetch)
rows = cursor.fetchall()
print(str(rows[0]).replace("\'","").replace(",","").replace("(","").replace(")",""))
connection.commit()
connection.close()
