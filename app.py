import os
import io
import time
import base64
import json
import fileutils
import zinc
from io import BytesIO
import urllib.request
from flask import Flask, request, redirect, jsonify
from werkzeug.utils import secure_filename
from pyresparser import ResumeParser
from urllib import request as uRequest

UPLOAD_FOLDER = './'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'docx', 'doc'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/zinc/search', methods=['POST'])
def searchZinc():  
    try:
        cid = request.json['cid']
        query = request.json['query']
        
        response = zinc.searchResume(payload)
        
        return (response.text, response.status_code, response.headers.items())
    except:
        resp = jsonify({'message' : 'Server Error'})
        resp.status_code = 503
        return resp  
    
@app.route('/zinc/populate', methods=['POST'])
def PopulateZinc():  
    try:
        docName = request.json['docName']
        docUrl = request.json['docUrl']
        
        fileName = str(time.time_ns()) + secure_filename(docName)
        filePath = os.path.join(app.config['UPLOAD_FOLDER'], fileName)
        fileExt = '.' + fileName.split('.')[1]
        
        uRequest.urlretrieve(docUrl, filePath)

        data = fileutils.extract_text(filePath, fileExt)

        if len(data) < 10:
            resp = jsonify({'message' : 'Not able to extract text from the file'})
            resp.status_code = 400
            return resp
        else:
            payload = json.dumps({
                "CID": request.json['CID'],
                "consultantID": request.json['consultantID'],
                "docName": docName,
                "data": ' '.join(data.split())
            })
            
            response = zinc.createResumeDoc(payload)
            
            os.remove(filePath)
            
            return (response.text, response.status_code, response.headers.items())
    except:
        resp = jsonify({'message' : 'Server Error'})
        resp.status_code = 503
        return resp

@app.route('/parse/base64', methods=['POST'])
def parseBase64():
    filename = request.json['filename']
    if allowed_file(filename):
        try:
            filename = str(time.time_ns()) + secure_filename(filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            filedata = base64.b64decode(request.json['filedata'])

            with open(filepath, 'wb') as f:
                f.write(filedata)
                
            data = ResumeParser(filepath).get_extracted_data()
            
            os.remove(filepath)
            
            resp = jsonify({'message' : 'File successfully uploaded', 'data' : data})
            resp.status_code = 201
            return resp
        except:
            resp = jsonify({'message' : 'Server Error'})
            resp.status_code = 503
            return resp
    else:
        resp = jsonify({'message' : 'Allowed file types are txt, pdf, png, jpg, jpeg, gif'})
        resp.status_code = 400
        return resp

@app.route('/parse/file', methods=['POST'])
def parse():
    # check if the post request has the file part
    if 'file' not in request.files:
        resp = jsonify({'message' : 'No file part in the request'})
        resp.status_code = 400
        return resp
    file = request.files['file']
    if file.filename == '':
        resp = jsonify({'message' : 'No file selected for uploading'})
        resp.status_code = 400
        return resp
    if file and allowed_file(file.filename):
        filename = str(time.time_ns()) + secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        data = ResumeParser(filepath).get_extracted_data()
        os.remove(filepath)
        resp = jsonify({'message' : 'File successfully uploaded', 'data' : data})
        resp.status_code = 201
        return resp
    else:
        resp = jsonify({'message' : 'Allowed file types are txt, pdf, png, jpg, jpeg, gif'})
        resp.status_code = 400
        return resp

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)