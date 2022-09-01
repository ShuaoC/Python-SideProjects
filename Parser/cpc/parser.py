import re
import os
import datetime
import shutil
import sys
import smtplib
import configparser
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Current Path
cwd = sys.path[0]

# Developmnent Path:
txtoutputPath = os.path.dirname(os.path.abspath(__file__))+"\\txtoutput\\"
hl7outputPath = os.path.dirname(os.path.abspath(__file__))+"\\hl7output\\"
archive_folder_path = os.path.dirname(os.path.abspath(__file__))+"\\archive\\txt\\"
archive_pdf_path = os.path.dirname(os.path.abspath(__file__))+"\\archive\\pdf\\"
error_pdf_path = os.path.dirname(os.path.abspath(__file__))+"\\error_handle\\pdf\\"
error_path = os.path.dirname(os.path.abspath(__file__))+"\\error_handle\\"
configFilePath = os.path.dirname(os.path.abspath(__file__))+"\\config.txt"
configMainPath = r"C:\Users\felixc\Desktop\pythonDev\Parser\configMain.txt"

# Server Path:
# txtoutputPath = cwd + "/txtoutput/"
# hl7outputPath = cwd + "/hl7output/"
# archive_folder_path = cwd + "/archive/txt/"
# archive_pdf_path = cwd + "/archive/pdf/"
# error_pdf_path = cwd + "/error_handle/pdf/"
# error_path = cwd + "/error_handle/"
# configFilePath =  cwd + "/config.txt"
# configMainPath = "/home/ubuntu/Parser/configMain.txt"

# Configuration file
configParser = configparser.RawConfigParser()
configParser.read(configFilePath)
configParserMain = configparser.RawConfigParser()
configParserMain.read(configMainPath)

dir_list = os.listdir(txtoutputPath)

sender = configParserMain.get('Notification' , 'sender')
app_pass = configParserMain.get('Notification' , 'app_pass')
receivers = [configParserMain.get('Notification' , 'receiver1'), configParserMain.get('Notification' , 'receiver2')]

msg = MIMEMultipart()
msg['From'] = sender
msg['To'] = 'felix.chen@deldxlabs.com'
msg['Subject'] = configParser.get('Email' , 'Subject')

# Client configuration
clientID = configParser.get('Client' , 'clientID')
referringDoctor = configParser.get('Client' , 'referringDoctor')
race = configParser.get('Client' , 'race')
ethnic = configParser.get('Client' , 'ethnic')

errorEmail = ""

# patterns for parsing
namePattern = configParser.get('Regex' , 'namePattern')
altNamePattern = configParser.get('Regex' , 'altNamePattern')
dobPattern = configParser.get('Regex' , 'dobPattern')
genderPattern = configParser.get('Regex' , 'genderPattern')
numberPattern = configParser.get('Regex' , 'numberPattern')
addressFirstLinePattern = configParser.get('Regex' , 'addressFirstLinePattern')
addressSecondLinePattern = configParser.get('Regex' , 'addressSecondLinePattern')
addressThirdLinePattern = configParser.get('Regex' , 'addressThirdLinePattern')
altAddressPattern = configParser.get('Regex' , 'altAddressPattern')
clientIDPattern = configParser.get('Regex' , 'clientIDPattern')
requisitionPattern = configParser.get('Regex' , 'requisitionPattern')
testCodePattern = configParser.get('Regex' , 'testCodePattern')
insuranceIDPattern = configParser.get('Regex' , 'insuranceIDPattern')
insuranceGroupPattern = configParser.get('Regex' , 'insuranceGroupPattern')
insurancePolicyHolderPattern = configParser.get('Regex' , 'insurancePolicyHolderPattern')
insuranceCompanyPattern = configParser.get('Regex' , 'insuranceCompanyPattern')

# use pattern to get name from a txt file
def getData(pattern, text):
    name = re.search(pattern, text)
    if name:
        return name.group()
    else:
        return ""

def InsuranceCompanyTranslator(company):
    companyCode = ""
    if company == "":
        return companyCode
    else:
        print()
    return companyCode

# Sort mm/dd/yyyy format into yyyymmdd format
def convertDate(dob):
    month = 0
    day = 0
    year = 0
    firstencounter = True
    pointer = 0
    for i in range(len(dob)-4):
        pointer+=1
        if (dob[i] == "/" and pointer == 2 and firstencounter == True):
            month = "0" + str(dob[i-1])
            pointer = 0
            firstencounter = False
        elif (dob[i] == "/" and pointer == 3 and firstencounter == True):
            month = str(dob[i-2])+str(dob[i-1])
            pointer = 0
            firstencounter = False
        elif (dob[i] == "/" and pointer == 2 and firstencounter == False):
            day = "0" + str(dob[i-1])
        elif (dob[i] == "/" and pointer == 3 and firstencounter == False):
            day = str(dob[i-2])+str(dob[i-1])
    year = str(dob[len(dob)-4]) + str(dob[len(dob)-3]) +str(dob[len(dob)-2]) +str(dob[len(dob)-1])
    dob = str(year) + str(month) + str(day)
    return dob

def send_email(message):
    message += "THIS IS AN AUTOMATED EMAIL. DO NOT REPLY."
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

# Turn information extracted into hl7 acceptable format
def getInfo(txt, i):

    # Start of regex modify section
    testCodes = re.findall(testCodePattern, txt)
    name = getData(namePattern, txt).replace(" ","").replace("-","").replace(",", "^")
    if(name == ""):
      name = getData(altNamePattern, txt).replace(" ","").replace("-","").replace(",", "^")
    try:
        dob = convertDate(getData(dobPattern, txt).replace(" ","").replace("\n",""))
    except IndexError:
        dob = ""

    gender = getData(genderPattern, txt).replace("\n","").replace(" ","")
    number = getData(numberPattern, txt).replace("(","").replace(")","").replace("\n","").replace(" ","").replace("-","")
    firstAddress = getData(addressFirstLinePattern, txt).replace("\n","").replace("yo","")
    secondAddress = getData(firstAddress + addressSecondLinePattern, txt).replace(firstAddress,"").replace(",","").replace("\n","")
    thirdAddress = getData(secondAddress + addressThirdLinePattern, txt).replace(secondAddress,"").replace(",","").replace(" ","^").replace("\n","")
    address = firstAddress + "^^" + secondAddress + thirdAddress
    if(firstAddress == "" and secondAddress == ""):
      address = getData(altAddressPattern, txt).replace("\n","^").replace(" ","^")
      
    patientId = getData(clientIDPattern, txt)

    insuranceCompany = []
    insuranceID = []
    insuranceGroup = []
    insurancePolicyHolder = []
    insuranceCompany = re.findall(insuranceCompanyPattern, txt)
    insuranceID = re.findall(insuranceIDPattern, txt)
    insuranceGroup = re.findall(insuranceGroupPattern, txt)
    insurancePolicyHolder = re.findall(insurancePolicyHolderPattern, txt)

    if len(insuranceID) == 0:
        insuranceID = [""] * 2
        insuranceGroup = [""] * 2
        insuranceCompany = [""] * 2
        insurancePolicyHolder = [""] * 2

    if len(insuranceID) == 1:
        if len(insuranceGroup) == 0:
            insuranceGroup = [""] * 2
        insuranceID.append("")
        insuranceGroup.append("")
        insuranceCompany.append("")
        insurancePolicyHolder.append("")

    if len(insuranceID) == 2 and len(insuranceGroup) == 0:
        insuranceGroup = [""] * 2
    
    if len(insuranceID) == 2 and len(insuranceGroup) == 1:
        pattern = '(?<=' + insuranceID[0] +'\nGroup:\s)(.*?)(?=\n)'
        group = getData(pattern, txt)
        if group == "":
            insuranceGroup.insert(0, "")
        else:
            insuranceGroup.append("")

    # insuranceCode = []
    # if len(insuranceCompany) != 0:
    #     for x in range(len(insuranceCompany)):
    #         insuranceCode[x] = InsuranceCompanyTranslator(insuranceCompany[0])
    
    requisition = getData(requisitionPattern, txt)

    dt = str(datetime.datetime.now()).replace("-","").replace(" ","").replace(":","").replace(".","")
    dts = ""
    for x in range(12):
        dts += dt[x]
    collectionTime = dts
    # End of regex modify section

    # Error Check
    if len(testCodes) == 0 or name == "" or dob == "" or gender == "" or number == "" or address == "" or patientId == "" or requisition == "" or collectionTime == "":
        error_msg = "One or more errors occurred in file: [" + i + "] "

        try:
            shutil.move(os.path.join(archive_pdf_path, i.replace(".txt",".pdf")), os.path.join(error_pdf_path, i.replace(".txt",".pdf")))
        except Exception as e:
            error_msg += str(e)
        try:
            shutil.move(os.path.join(txtoutputPath, i), os.path.join(error_path, i))
        except Exception as e:
            error_msg += str(e)

        if len(testCodes) == 0:
            error_msg += "Missing test code. "
        if name == "":
            error_msg += "Missing patient name. "
        if dob == "":
            error_msg += "Missing patient date of birth. "
        if gender == "":
            error_msg += "Missing patient gender. "    
        if number == "":
            error_msg += "Missing patient phone number. " 
        if address == "":
            error_msg += "Missing patient address. "
        if patientId == "":
            error_msg += "Missing patient id. "
        if requisition == "":
            error_msg += "Missing requisition number. "       
        if collectionTime == "":
            error_msg += "Missing collection time. "       
        return error_msg

    if (len(testCodes) == 1):
    # HL7 basic format
        hl7 = '''MSH|^~\&|DDL|MIRTH||DDL|202108202334||ORM^O01||T|2.5.1|
PID|1|{}|{}||{}||{}|{}||{}|{}||{}|||||||||{}|
PV1|{}|||||||{}||||||||||||
IN1|1||{}|||||{}||||||||{}||||||||||||||||||||{}|
IN1|2||{}|||||{}||||||||{}||||||||||||||||||||{}|
ORC|NW|{}|{}|||||||||{}|
OBR|1|{}||{}|||{}|||||||||{}|||||||||||^^^^^0|
DG1|1|I10|Z79899||
'''.format(
        patientId, patientId, name, dob, gender,race, address, number, ethnic,
        patientId, referringDoctor,
        insuranceCompany[0], insuranceGroup[0], insurancePolicyHolder[0], insuranceID[0],
        insuranceCompany[1], insuranceGroup[1], insurancePolicyHolder[1], insuranceID[1],
        requisition,requisition,clientID,
        requisition,str(testCodes[0]),collectionTime,clientID)
    elif (len(testCodes) == 2):
        hl7 = '''MSH|^~\&|DDL|MIRTH||DDL|202108202334||ORM^O01||T|2.5.1|
PID|1|{}|{}||{}||{}|{}||{}|{}||{}|||||||||{}|
PV1|{}|||||||{}||||||||||||
IN1|1||{}|||||{}||||||||{}||||||||||||||||||||{}|
IN1|2||{}|||||{}||||||||{}||||||||||||||||||||{}|
ORC|NW|{}|{}|||||||||{}|
OBR|1|{}||{}|||{}|||||||||{}|||||||||||^^^^^0|
DG1|1|I10|Z79899||
OBR|2|{}||{}|||{}|||||||||{}|||||||||||^^^^^0|
DG1|1|I10|Z79899||
'''.format(
        patientId, patientId, name, dob, gender,race, address, number, ethnic,
        patientId, referringDoctor,
        insuranceCompany[0], insuranceGroup[0], insurancePolicyHolder[0], insuranceID[0],
        insuranceCompany[1], insuranceGroup[1], insurancePolicyHolder[1], insuranceID[1],
        requisition,requisition,clientID,
        requisition,str(testCodes[0]),collectionTime,clientID,
        requisition,str(testCodes[1]),collectionTime,clientID)

    output = open(hl7outputPath + i.replace(".txt",".hl7"),'w')
    output.write(hl7)
    return ""


for i in dir_list:
    file = open(txtoutputPath + i, 'r')
    txt = file.read()
    file.close()
    result = getInfo(txt,i)
    if(result != ""):
        errorEmail += (result + "\n\n")
        continue
    shutil.move(os.path.join(txtoutputPath, i), os.path.join(archive_folder_path, i))

if(errorEmail != ""):
    send_email(errorEmail)

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
            os.remove(os.path.join(root, name))

os.chdir(archive_pdf_path) #changing path to current path(same as cd command)

#we are taking current folder, directory and files 
#separetly using os.walk function
for root,directories,files in os.walk(archive_pdf_path,topdown=False): 
    for name in files:
        #this is the last modified time
        t = os.stat(os.path.join(root, name))[8] 
        filetime = datetime.datetime.fromtimestamp(t) - today

        #checking if file is more than 30 days old 
        #or not if yes then remove them
        if filetime.days <= -30:
            os.remove(os.path.join(root, name))