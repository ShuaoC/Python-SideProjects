from doctest import testfile
import re
import sys
import csv
import xlwt
from xlwt import Workbook

cwd = sys.path[0]
wb = Workbook()
sheet = wb.add_sheet('Sheet')
header = ['Requsition number', 'Check number', 'Tests']
data = ['123','321','123']

textFile = 'text4.txt'
csvFile = 'text4.csv'

reqPattern = '(\n|\s)([0-9]{2}([A-Z]{2}|[0-9]{2}|[A-Z]{1}[0-9]{1})[0-9]{9})(\n|\s)'
checkNumPattern = '\s[0-9]{0,9}\/([0-9]{0,8})\n'
pricePattern = '((.*?)\n(.*?)\n(.*?)\n(.*?)Total:(.*?)(\n|\s\n))'

pattern1 = '[0-9]+\/[0-9]+\/[0-9]+\s'
pattern2 = '[0-9]+\.[0-9]+\s'

def getInfo(txt):
    req = re.findall(reqPattern, txt)
    checkNum = re.findall(checkNumPattern, txt)
    price = re.findall(pricePattern, txt)
    with open(r'C:\Users\felixc\Desktop\pythonDev\excelExtract' + '\\' + csvFile, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        results = []
        for idx, x in enumerate(req):
            print(idx)
            results.append([])
            results[idx].append(x[1])
        for idx, y in enumerate(checkNum):
            print(idx)
            if y == "" :
                results[idx].append("")
            else :
                print(y)
                results[idx].append(y)
        for idx, z in enumerate(price):
            temp = re.sub(pattern1,"",str(z))
            temp2 = re.sub(pattern2,"",temp)
            #results[idx].append(temp2)
        for idx, h in enumerate(results):
            writer.writerow(results[idx])
        

file = open(cwd + '\\' + textFile, 'r')
txt = file.read()
getInfo(txt)
file.close()

