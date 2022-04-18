from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import sys
from datetime import datetime



app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = "static/"

@app.route('/')
def upload_file():
    return render_template('index.html')
 
    
@app.route('/display', methods = ['GET', 'POST'])
def parse():  
    if request.method == 'POST':
        def timediff(x, y):
                t1 = datetime.strptime(x.upper().strip(), '%I:%M%p')
                t2 = datetime.strptime(y.upper().strip(), '%I:%M%p')
                return (t2-t1).seconds

        def number_of_hrs(times):
            total = 0
            for i in range(0,len(times)-1,2):
                try:
                    total += timediff(times[i], times[i+1])
                except Exception:
                    print('line {} has issue'.format(i+1))
            hrs = total/3600
            return hrs
         
        file = request.files['file']        
        filename = secure_filename(file.filename)
        file.save(app.config['UPLOAD_FOLDER'] + filename)
        f1 = open(app.config['UPLOAD_FOLDER']+filename,'r')
        Lines = f1.readlines()
        times = []
        for line in Lines[1:]:
            for i in range(len(line)-1):
                if line[i]==':' and line[i+1]!=' ':
                    times.append(line[i-2:i+5])
        
        num_hrs = number_of_hrs(times)
        result = "Total Number of hours in time logs from file : "+str(num_hrs)     
                 
        return render_template('index.html',final_output=result)
    return render_template('index.html')
                    

if __name__ == '__main__':
    app.run(debug = True)