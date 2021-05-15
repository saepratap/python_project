import pandas as pd
from flask import Flask,request,render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("upload.html")

@app.route("/data",methods=['GET','POST'])
def main():
    try:
        if request.method == 'POST':
            f = request.form['myfile']
            print("value :",f)
            data_xls = pd.read_csv(f)
            print("what is getting for this :",data_xls)
        return render_template("nothing.html")
    except Exception as e:
            print("Here is the Exception :",e)


app.run(port=5010)
