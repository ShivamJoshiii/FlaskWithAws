from flask import Flask, render_template, request
import datetime
import os
import re
import sys
application = app = Flask(__name__)
@app.route('/',methods=['GET','POST'])
def send():
    if request.method == 'POST':
        Input_File = request.files['filename']
        f2 = Input_File.filename
        Input_File.save(f2)
        f1 = open(f2,"r")
        os.remove(f2)
        tpair = []                                        #This list combine Hours and Minutes
        backup = ""
        lenthback = 0
        Found_IT = 0
        for lines in f1:                                #read lines from the file
            ans = re.search("^Time.*og.*$", lines)
            if ans:
                Found_IT=1
            if Found_IT==1:
                datecon = re.split(":",lines)
                for plase in datecon:                       #access the list
                    try:
                        if (plase[2]=="p" or plase[2]=="P"):
                            Minutes = plase[0]+plase[1]
                            String_Hours = backup[lenthback-2]+backup[lenthback-1]
                            Converted_Hours = int(String_Hours)
                            hrs = 12 + Converted_Hours
                            if (hrs==24):
                                hrs=12
                            tpair.append(str(hrs)+":"+str(Minutes))
                        elif (plase[2]=="a" or plase[2]=="A"):             
                            Minutes = plase[0]+plase[1]
                            String_Hours = backup[lenthback-2]+backup[lenthback-1]
                            hrs = int(String_Hours)
                            if (hrs==12):
                                hrs=00
                            tpair.append(str(hrs)+":"+str(Minutes))
                        else:
                            pass
                    except:
                        pass
                    backup = plase                               #For previous element
                    lenthback = len(backup)
            else:
                continue   
        sum = 0
        for subt in range(0,len(tpair),2):                 #All calculation with 24-hours time
            Start_Time = tpair[subt]
            End_Time = tpair[subt+1]
            Start_Date = datetime.datetime.strptime(Start_Time, '%H:%M')
            End_Date = datetime.datetime.strptime(End_Time, '%H:%M')
            diff = (End_Date - Start_Date)                     #difference of starting time and ending time
            TotalTime = diff.seconds
            sum = sum+TotalTime
            sum1 = sum/3600
            Sum_Hours = int(sum1)
            Sum_Minute = int((sum/60)%60)
        return render_template('output.html',dt="Total: "+str(Sum_Hours)+" hours "+str(Sum_Minute)+" minutes.")
    else:
        return render_template('try.html')

if __name__ == '__main__':
    app.run(debug=True)