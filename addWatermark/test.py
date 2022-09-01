from PyPDF2 import PdfFileWriter, PdfFileReader
import io
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


req_path = os.path.dirname(os.path.abspath(__file__))+"\\requsitionNum.txt"
def requisitionGeneration():

    requisition = ""

    if((os.stat(req_path).st_size == 0)):
        reqFile = open(req_path, 'a')
        requisition = "AA01"
        reqFile.write(requisition)
        reqFile.close()
    else:
        reqFile = open(req_path, 'a')
        reqRead = open(req_path, 'r')
        newLetter = ""
        newNum = ""
        txt = reqRead.read()
        latestReq = txt[len(txt)-7 : len(txt)]
        letters = latestReq[3:5]
        numbers = latestReq[5:8]

        if(numbers == "99"):
            if(letters == "ZZ"):
                file = open(req_path, 'r+')
                file.truncate(0)
                file.close()
                newLetter = "AA"
            else:
                if(letters[1] == "Z"):
                        char = letters[0]
                        i = ord(char[0])
                        i+= 1
                        newLetter = chr(i) + letters[1]
                else:
                    char = letters[1]
                    i = ord(char[0])
                    i+= 1
                    newLetter = letters[0] + chr(i)
            newNum = "01"
        else:
            newLetter = letters
            newNum = str((int(numbers) + 1)).zfill(2)
        
        requisition = newLetter + newNum
        reqFile.write(requisition)
        reqFile.close()
        reqRead.close()
    
    return requisition


print(requisitionGeneration())