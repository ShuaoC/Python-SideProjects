import csv

header = ['Requsition number', 'Check number', 'Tests']
row = ['123','321','123']
      
f = open(r'C:\Users\felixc\Desktop\pythonDev\excelExtract\123.csv', 'w')

writer = csv.writer(f)
writer.writerow(row)

f.close()
# with open('countries.csv', 'w', encoding='UTF8') as f:
#     writer = csv.writer(f)

#     # write the header
#     writer.writerow(header)

#     # write the data
#     writer.writerow(data)

