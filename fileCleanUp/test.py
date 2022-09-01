import os 
import datetime
import sys
path = sys.path[0] + "/files/"

today = datetime.datetime.today()#gets current time
os.chdir(path) #changing path to current path(same as cd command)

#we are taking current folder, directory and files 
#separetly using os.walk function
for root,directories,files in os.walk(path,topdown=False): 
    for name in files:
        #this is the last modified time
        t = os.stat(os.path.join(root, name))[8] 
        filetime = datetime.datetime.fromtimestamp(t) - today

        #checking if file is more than 7 days old 
        #or not if yes then remove them
        if filetime.days <= -10:
            print(os.path.join(root, name), filetime.days)
            os.remove(os.path.join(root, name))