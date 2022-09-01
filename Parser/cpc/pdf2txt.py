from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
import io
import os
import shutil
import sys

# Current Path
cwd = sys.path[0]

# Developmnent Path:
inputPath = os.path.dirname(os.path.abspath(__file__))+"\\input\\"
txtoutputPath = os.path.dirname(os.path.abspath(__file__))+"\\txtoutput\\"
archive_folder_path = os.path.dirname(os.path.abspath(__file__))+"\\archive\pdf\\"

# Server Path:
# inputPath = cwd + "/input/"
# txtoutputPath = cwd + "/txtoutput/"
# archive_folder_path = cwd + "/archive/pdf/"

dir_list = os.listdir(inputPath)

# Turn pdf files into txt files
def pdf_to_text(input_file,output):
    i_f = open(input_file,'rb')
    print(i_f)
    resMgr = PDFResourceManager()
    retData = io.StringIO()
    TxtConverter = TextConverter(resMgr,retData, laparams= LAParams())
    interpreter = PDFPageInterpreter(resMgr,TxtConverter)
    for page in PDFPage.get_pages(i_f):
        interpreter.process_page(page)
 
    txt = retData.getvalue()
    print(txt)
    with open(output,'w') as of:
        of.write(txt)

    i_f.close()


# Generate txt output
for i in dir_list:
    pdf_to_text(inputPath + i, txtoutputPath + i.replace(".pdf",".txt").replace(" ","")) 
    # Move all the processed pdf files into an archive folder
    shutil.move(os.path.join(inputPath, i), os.path.join(archive_folder_path, i.replace(" ","")))
    

