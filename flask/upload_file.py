#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
from flask import Flask, request, redirect, url_for
from werkzeug import secure_filename
from flask import send_from_directory


UPLOAD_FOLDER = '/home/xucb/data/stroke_images'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def hello_world():
    return 'Hello World!'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/stroke_images', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        print dir(request.form)
        print request.form['tag'].encode('utf-8')
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="/stroke_images" method=post enctype=multipart/form-data>
    tag:<input type="text" name="tag" placeholder="学">
    </br>
    file:<input type=file name="file">
         <input type=submit value=Upload>
    </form>
    '''
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)
if __name__ == '__main__':
    app.run(host='192.168.100.22',port=7000)
    #app.run(host='192.168.100.22',port=7001,debug=True)

