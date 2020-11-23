from flask import Flask, render_template, request
import datetime as dt
import re
from datetime import datetime
import sys

app = Flask(__name__) #creating the Flask class object   

@app.route('/')
def upload_file():
   return render_template("home.html")
   
@app.route('/uploader', methods = ['POST']) #decorator drfines the   
def home(): 
    if request.method == 'POST':
        f = request.files['file']
        name=f.filename
        f.save(f.filename)
        with open(name,'r') as file_in:
            sttime = []
            edtime = []
            for line in file_in:
                  
                endTime = line.partition("- ")[2].partition(' ')[0]
                STime = ''
                
                if endTime != "":
                    edtime.append(endTime)
                    #print("eTime "+ endTime)
                    startTime = line.partition('-')[0]
                    
                    regexp = re.compile('/')
                    if regexp.search(startTime):
                        startTime = line.partition('-')[0].partition(': ')[2]
                        STime = startTime
                    else:
                        STime = startTime.partition(' ')[2].replace(' ','')
                    #print("sTime "+STime)
                    sttime.append(STime)
            sum = 0
            try:
                for x in range(len(sttime)):
                    
                    st = sttime[x].replace(' ','')
                    sin_time = dt.datetime.strptime(st, "%I:%M%p") # parses a string into a time object
                    sout_time = dt.datetime.strftime(sin_time, "%H:%M") # Time object to 24hour time format
                    #print(sout_time)
                    
                    et=edtime[x].replace('\n','')
                    ein_time = dt.datetime.strptime(et, "%I:%M%p") 
                    eout_time = dt.datetime.strftime(ein_time, "%H:%M")
                    #print(eout_time)
                    
                    start_dt = dt.datetime.strptime(sout_time, '%H:%M')
                    end_dt = dt.datetime.strptime(eout_time, '%H:%M')
                    diff = (end_dt - start_dt) 
                    
                    TotalTime = diff.seconds
                    sum = sum + TotalTime 
                    sums = sum/3600
                    sumh = int(sums)
                    summi = int((sum/60)%60)
                    
                return render_template("home.html",data="Total : "+str(sumh) + " h"+ str(summi) + " m")
            except:
                    return render_template("home.html",data="Excepion")

		
if __name__ == '__main__':
   app.run(debug = True)