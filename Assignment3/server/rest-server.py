#!flask/bin/python
################################################################################################################################
#------------------------------------------------------------------------------------------------------------------------------                                                                                                                             
# This file implements the REST layer. It uses flask micro framework for server implementation. Calls from front end reaches 
# here as json and being branched out to each projects. Basic level of validation is also being done in this file. #                                                                                                                                  	       
#-------------------------------------------------------------------------------------------------------------------------------                                                                                                                              
################################################################################################################################
from flask import Flask, jsonify, abort, request, make_response, url_for,redirect, render_template
from flask_httpauth import HTTPBasicAuth
from werkzeug.utils import secure_filename
import os
import shutil 
import numpy as np
from search import recommend
import tarfile
from datetime import datetime
from scipy import ndimage
import random
from flask_cors import CORS
#from scipy.misc import imsave

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
from tensorflow.python.platform import gfile
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
auth = HTTPBasicAuth()
CORS(app, origins=['http://localhost'], supports_credentials=True)

def iter_files(rootDir):
    all_files = []
    for root, dirs, files in os.walk(rootDir):
        for file in files:
            file_name = os.path.join(root, file)
            all_files.append(file_name)
        for dirname in dirs:
            iter_files(dirname)
    return all_files

#==============================================================================================================================
#                                                                                                                              
#    Loading the extracted feature vectors for image retrieval                                                                 
#                                                                          						        
#                                                                                                                              
#==============================================================================================================================

img_files = iter_files('database/dataset')

all_files = img_files#boots_files + shoes_files + slippers_files + sandals_files + apparel_files

random.shuffle(all_files)

#num_images = 10000
num_images = min(10000,len(all_files))
extracted_features=np.zeros((num_images,2048),dtype=np.float32)
with open('saved_features_recom.txt') as f:
    		for i,line in enumerate(f):
        		extracted_features[i,:]=line.split()
print("loaded extracted_features") 


#==============================================================================================================================
#                                                                                                                              
#  This function is used to do the image search/image retrieval
#                                                                                                                              
#==============================================================================================================================
@app.route('/imgUpload', methods=['GET', 'POST'])
def upload_img():
    print("image upload")
    result = 'static/result'
    if not gfile.Exists(result):
          os.mkdir(result)
    shutil.rmtree(result)
 
    if request.method == 'POST' or request.method == 'GET':
        print(request.method)
        # check if the post request has the file part
        if 'file' not in request.files:
            print('No file part')
            return redirect(request.url)
        
        file = request.files['file']
        print(file.filename)
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
           
            print('No selected file')
            return redirect(request.url)
        if file:# and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            inputloc = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            recommend(inputloc, extracted_features)
            # os.remove(inputloc)
            image_path = "/static/result"

            # Traverse to find the image's tag
            typename = []
            tagpath = "./database/tags/"
            tagslist = os.listdir(tagpath)
            for image in os.listdir(result):
                
                imgName,extension = os.path.splitext(image)
                for tagfile in tagslist:
                    with open(tagpath+tagfile,'r',encoding = 'UTF-8') as f:
                        class_names = f.readlines()
                    class_names = [c.strip() for c in class_names]
                    if imgName[2:] in class_names:
                        tagName,_ = os.path.splitext(tagfile)
                        typename.append(tagName)
                        break


            image_list =[os.path.join(image_path, file) for file in os.listdir(result)
                              if not file.startswith('.')]

            images = {
			'image0':image_list[0],
            'image1':image_list[1],	
			'image2':image_list[2],	
			'image3':image_list[3],	
			'image4':image_list[4],	
			'image5':image_list[5],	
            'image0_type':typename[0],
            'image1_type':typename[1],
            'image2_type':typename[2],
            'image3_type':typename[3],
            'image4_type':typename[4],
            'image5_type':typename[5],

			# 'image6':image_list[6],	
			# 'image7':image_list[7],	
			# 'image8':image_list[8]
		      }				
            return jsonify(images)

#==============================================================================================================================
#                                                                                                                              
#                                           Main function                                                        	            #						     									       
#  				                                                                                                
#==============================================================================================================================
@app.route("/",methods=['GET', 'POST'])
def index():
    return render_template("index.html") 

@app.route("/camera",methods=['GET', 'POST'])
def camera():
    return render_template("takePicture.html") 


if __name__ == '__main__':
    app.run(debug = True, host= '0.0.0.0')
