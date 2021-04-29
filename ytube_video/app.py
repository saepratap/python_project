from flask import Flask, render_template,request
import requests
import os
import re

#video = moviepy.editor.VideoFileClip("D:\path\to\video.mp4")
app = Flask(__name__, static_folder='static')

@app.route('/',methods=['GET','POST'])
def index():
    list1=[]
    if request.method=='POST':
        search_name=request.form.get('query')
        print("Exact name",search_name)
        list1 = os.listdir("./static")
        print("my list:",list1)
        if search_name in list1:
            return render_template('index.html',videos=search_name)
        else:
            return "Nothing is available.."
            #return render_template('index.html',videos=list1)
        #list1 = os.listdir("/Users/apple/Documents/Video Songs")
        #list1=["AWE Theme-Awe Video Songs - అ!.mp4"]
    return render_template('index.html',videos=list1)


app.run(port='5001')
