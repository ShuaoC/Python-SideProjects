import os
import smtplib
import datetime
import sys
import shutil
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


sender = 'felix.chen@deldxlabs.com'
app_pass = 'hiiwgtwiavejmuen'
receivers = ['felix.chen@deldxlabs.com','felix19981228@gmail.com']

msg = MIMEMultipart()
msg['From'] = sender
msg['To'] = 'felix.chen@deldxlabs.com'
msg['Subject'] = 'HL7 Parser Error Notice'
message = ""

error = ""

# Current Path
cwd = sys.path[0]

# Developmnent Path:
txtoutputPath = r"C:\Users\felixc\Desktop\pythonDev\Parser\cpc\archive\txt\\"
archive_folder_path = r"C:\Users\felixc\Desktop\pythonDev\Parser\cpc\archive\pdf\\"
hl7outputPath = r"C:\Users\felixc\Desktop\pythonDev\Parser\cpc\hl7output\\"
error_handle_path = r"C:\Users\felixc\Desktop\pythonDev\Parser\cpc\error_handle\\"
error_pdf_path = r"C:\Users\felixc\Desktop\pythonDev\Parser\cpc\error_handle\pdf\\"
error_txt_path = r"C:\Users\felixc\Desktop\pythonDev\Parser\cpc\error_handle\txt\\"
output_path = r"C:\Users\felixc\Desktop\pythonDev\Parser\cpc\output"

# Server Path:
# txtoutputPath = cwd + "/archive/txt/"
# archive_folder_path = cwd + "/archive/pdf/"
# hl7outputPath = cwd + "/hl7output/"
# error_handle_path = cwd + "/error_handling/"
# error_pdf_path = cwd + "/error_handling/pdf/"
# error_txt_path = cwd + "/error_handling/txt/"
# output_path = cwd + "/output/"

try:
    hl7_list = os.listdir(hl7outputPath)
except FileNotFoundError:
    print("No files in the hl7 output folder")
    sys.exit()

# Turn HL7 message into 2D array
def make2DArray(content):
    sArray = []
    tArray = []
    st = ''

    for ch in content:
        if ch == '|':
            sArray.append(st)
            sArray.append(ch)
            st = ''
        elif ch == '\n':
            sArray.append(ch)
            tArray.append(sArray)
            sArray = []
            
        else:
            st += ch

    tArray.append(sArray)

    return tArray

# Error checking
def error_check(hl7,error_msg):
    
    try:
        #PID ERROR
        if hl7[1][2] == '' :
            error_msg += " **Error: Missing [{}][Field {}][{}]** ".format(hl7[1][0],"1","Set ID - PID")
        if hl7[1][6] == '' :
            error_msg += " **Error: Missing [{}][Field {}][{}]** ".format(hl7[1][0],"3","Patient Identifier List")
        if hl7[1][10] == '' :
            error_msg += " **Error: Missing [{}][Field {}][{}]** ".format(hl7[1][0],"5","Patient Name")        
        if hl7[1][14] == '' :
            error_msg += " **Error: Missing [{}][Field {}][{}]** ".format(hl7[1][0],"7","Date/Time of Birth")    
        if hl7[1][16] == '' :
            error_msg += " **Error: Missing [{}][Field {}][{}]** ".format(hl7[1][0],"8","Administrative Sex")        
        if hl7[1][20] == '' :
            error_msg += " **Error: Missing [{}][Field {}][{}]** ".format(hl7[1][0],"10","Race")        
        if hl7[1][22] == '' :
            error_msg += " **Error: Missing [{}][Field {}][{}]** ".format(hl7[1][0],"11","Patient Address")        
        if hl7[1][26] == '' :
            error_msg += " **Error: Missing [{}][Field {}][{}]** ".format(hl7[1][0],"13","Phone Number - Home")        
        if hl7[1][44] == '' :
            error_msg += " **Error: Missing [{}][Field {}][{}]** ".format(hl7[1][0],"22","Ethnic Group")      

        #PV1 ERROR
        if hl7[2][2] == '' :
            error_msg += " **Error: Missing [{}][Field {}][{}]** ".format(hl7[2][0],"1","Set ID - PV1")
        if hl7[2][16] == '' :
            error_msg += " **Error: Missing [{}][Field {}][{}]** ".format(hl7[2][0],"8","Referring Doctor") 
        
        #ORC ERROR
        if hl7[4][2] == '' :
            error_msg += " **Error: Missing [{}][Field {}][{}]** ".format(hl7[4][0],"1","Order Control")
        if hl7[4][4] == '' :
            error_msg += " **Error: Missing [{}][Field {}][{}]** ".format(hl7[4][0],"2","Placer Order Number")
        if hl7[4][6] == '' :
            error_msg += " **Error: Missing [{}][Field {}][{}]** ".format(hl7[4][0],"3","Filler Order Number")        
        if hl7[4][24] == '' :
            error_msg += " **Error: Missing [{}][Field {}][{}]** ".format(hl7[4][0],"12","Ordering Provider")    

        #OBR ERROR
        if hl7[5][2] == '' :
            error_msg += " **Error: Missing [{}][Field {}][{}]** ".format(hl7[5][0],"1","Set ID - OBR")
        if hl7[5][4] == '' :
            error_msg += " **Error: Missing [{}][Field {}][{}]** ".format(hl7[5][0],"2","Placer Order Number")
        if hl7[5][8] == '' :
            error_msg += " **Error: Missing [{}][Field {}][{}]** ".format(hl7[5][0],"4","Universal Service Identifier")        
        if hl7[5][14] == '' :
            error_msg += " **Error: Missing [{}][Field {}][{}]** ".format(hl7[5][0],"7","Observation Date/Time")  
        if hl7[5][32] == '' :
            error_msg += " **Error: Missing [{}][Field {}][{}]** ".format(hl7[5][0],"16","Ordering Provider")        
        if hl7[5][54] == '' :
            error_msg += " **Error: Missing [{}][Field {}][{}]** ".format(hl7[5][0],"27","Quantity/Timing")

        #DG1 ERROR
        if hl7[6][2] == '' :
            error_msg += " **Error: Missing [{}][Field {}][{}]** ".format(hl7[6][0],"1","Set ID - DG1")
        if hl7[6][4] == '' :
            error_msg += " **Error: Missing [{}][Field {}][{}]** ".format(hl7[6][0],"2","Diagnosis Coding Method")
        if hl7[6][6] == '' :
            error_msg += " **Error: Missing [{}][Field {}][{}]** ".format(hl7[6][0],"3","Diagnosis Code - DG1")

       
        #OBR ERROR
        if hl7[7][2] == '' :
            error_msg += " **Error: Missing [{}][Field {}][{}]** ".format(hl7[7][0],"1","Set ID - OBR")
        if hl7[7][4] == '' :
            error_msg += " **Error: Missing [{}][Field {}][{}]** ".format(hl7[7][0],"2","Placer Order Number")
        if hl7[7][8] == '' :
            error_msg += " **Error: Missing [{}][Field {}][{}]** ".format(hl7[7][0],"4","Universal Service Identifier")        
        if hl7[7][14] == '' :
            error_msg += " **Error: Missing [{}][Field {}][{}]** ".format(hl7[7][0],"7","Observation Date/Time")  
        if hl7[7][32] == '' :
            error_msg += " **Error: Missing [{}][Field {}][{}]** ".format(hl7[7][0],"16","Ordering Provider")        
        if hl7[7][54] == '' :
            error_msg += " **Error: Missing [{}][Field {}][{}]** ".format(hl7[7][0],"27","Quantity/Timing")

        #DG1 ERROR
        if hl7[8][2] == '' :
            error_msg += " **Error: Missing [{}][Field {}][{}]** ".format(hl7[8][0],"1","Set ID - DG1")
        if hl7[8][4] == '' :
            error_msg += " **Error: Missing [{}][Field {}][{}]** ".format(hl7[8][0],"2","Diagnosis Coding Method")
        if hl7[8][6] == '' :
            error_msg += " **Error: Missing [{}][Field {}][{}]** ".format(hl7[8][0],"3","Diagnosis Code - DG1")
    except IndexError as e:
        return str(e)
    
    
    return error_msg

# Send errors to email
def send_email(message):
    msg.attach(MIMEText(message))
    mailserver = smtplib.SMTP('smtp.gmail.com',587)
    # identify ourselves to smtp gmail client
    mailserver.ehlo()
    # secure our email with tls encryption
    mailserver.starttls()
    # re-identify ourselves as an encrypted connection
    mailserver.ehlo()
    mailserver.login(sender, app_pass)
    mailserver.sendmail(sender, receivers, msg.as_string())
    mailserver.quit()

# Check for error in files, and handle the solution
for i in hl7_list:
    error_msg = "One or more errors occurred in the hl7 files: "
    file = open(hl7outputPath + i, 'r')
    txt = file.read()
    file.close()
    error = error_check(make2DArray(txt),error_msg)
    
    if error == "One or more errors occurred in the hl7 files: ":
        # If files have no error,delete txt files
        try:
            shutil.move(os.path.join(hl7outputPath, i), os.path.join(output_path, i))
        except FileNotFoundError:
            continue
    else:
        # If error is detected in the file, move the archeve file and the txt file and the hl7 file into troubleshooting folder
        try:
            shutil.move(os.path.join(hl7outputPath, i), os.path.join(error_handle_path, i))
        except Exception as e:
            message += str(e)

        try:
            shutil.move(os.path.join(archive_folder_path, i.replace(".hl7",".pdf")), os.path.join(error_pdf_path, i.replace(".hl7",".pdf")))
        except Exception as e:
            message += str(e)

        try:
            shutil.move(os.path.join(txtoutputPath, i.replace(".hl7",".txt")), os.path.join(error_txt_path, i.replace(".hl7",".txt")))
        except Exception as e:
            message += str(e)
        message += "\n" + "[[[" + i + "]]]" + " " + error + "\n\n"
        
if(message != ""):
    send_email(message)

# Clean up any files in the archive folder that are more the one month old
today = datetime.datetime.today()#gets current time
os.chdir(archive_folder_path) #changing path to current path(same as cd command)

#we are taking current folder, directory and files 
#separetly using os.walk function
for root,directories,files in os.walk(archive_folder_path,topdown=False): 
    for name in files:
        #this is the last modified time
        t = os.stat(os.path.join(root, name))[8] 
        filetime = datetime.datetime.fromtimestamp(t) - today

        #checking if file is more than 30 days old 
        #or not if yes then remove them
        if filetime.days <= -30:
            print(os.path.join(root, name), filetime.days)
            os.remove(os.path.join(root, name))

os.chdir(txtoutputPath)
for root,directories,files in os.walk(txtoutputPath,topdown=False): 
    for name in files:
        #this is the last modified time
        t = os.stat(os.path.join(root, name))[8] 
        filetime = datetime.datetime.fromtimestamp(t) - today

        #checking if file is more than 30 days old 
        #or not if yes then remove them
        if filetime.days <= -30:
            print(os.path.join(root, name), filetime.days)
            os.remove(os.path.join(root, name))