import subprocess  
import os

printer='ZDesigner LP 2824 Plus (ZPL)' 

pdffile=r'C:\Users\felixc\Desktop\DDLUpload\requsitionLabel\req.pdf' 

acroread=r'C:\Users\felixc\Desktop\DDLUpload'+"\\Acrobat\\Acrobat\\Acrobat.exe"
print(acroread)
cmd='"%s" /N /T "%s" "%s"'%(acroread,pdffile,printer)  
proc = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
