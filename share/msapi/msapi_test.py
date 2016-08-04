
# coding: utf-8

# In[1]:

import time 
import requests
import cv2
import operator
import numpy as np
#from __future__ import print_function

# Import library to display results
#import matplotlib.pyplot as plt
#get_ipython().magic(u'matplotlib inline')
# Display images within Jupyter


# In[2]:

_url = 'https://api.projectoxford.ai/face/v1.0/detect'
_key = '89493f7b061f47fba871939e0117a807'
_maxNumRetries = 10

malePath   = '/home/maru/Project/modu/label/male/'
femalePath = '/home/maru/Project/modu/label/female/'
etcPath    = '/home/maru/Project/modu/label/etc/'


# In[3]:

def processRequest( json, data, headers, params ):

    """
    Helper function to process the request to Project Oxford

    Parameters:
    json: Used when processing images from its URL. See API Documentation
    data: Used when processing image read from disk. See API Documentation
    headers: Used to pass the key information and the data type request
    """

    retries = 0
    result = None

    while True:
        try:
            response = requests.request( 'post', _url, json = json, data = data, headers = headers, params = params )
        except :
            print ("error")
        else :            
            if response.status_code == 429: 

                print( "Message: %s" % ( response.json()['error']['message'] ) )

                if retries <= _maxNumRetries: 
                    time.sleep(1) 
                    retries += 1
                    continue
                else: 
                    print( 'Error: failed after retrying!' )
                    break

            elif response.status_code == 200 or response.status_code == 201:

                if 'content-length' in response.headers and int(response.headers['content-length']) == 0: 
                    result = None 
                elif 'content-type' in response.headers and isinstance(response.headers['content-type'], str): 
                    if 'application/json' in response.headers['content-type'].lower(): 
                        result = response.json() if response.content else None 
                    elif 'image' in response.headers['content-type'].lower(): 
                        result = response.content
            else:
                print( "Error code: %d" % ( response.status_code ) )
                print( "Message: %s" % ( response.json()['error']['message'] ) )

            break
        

    return result


# In[4]:

def saveImage(img, label, filename, count):
    if label is not None:
        if label == 'male' :
            cv2.imwrite(malePath + str(count) + '_' + filename, img)
        elif label == 'female':
            cv2.imwrite(femalePath + str(count) + '_' + filename, img)
        else:
             cv2.imwrite(etcPath + str(count) + '_' + filename, img)        
        print ("save complate : ") , (filename)


# In[5]:

def resultImage( result, img, filename ):
    count = 0
    for currFace in result:
        faceRectangle = currFace['faceRectangle']
        #cv2.rectangle( img,(faceRectangle['left'],faceRectangle['top']),
        #                   (faceRectangle['left']+faceRectangle['width'], faceRectangle['top'] + faceRectangle['height']),
        #               color = (255,0,0), thickness = 1 )

        faceLandmarks = currFace['faceLandmarks']
        
        x = faceRectangle['left']
        y = faceRectangle['top']
        w = faceRectangle['width']
        h = faceRectangle['height']
        
        roi = img[ y : y + h, x : x + w ]
        
        gender = currFace['faceAttributes']['gender']
                
        saveImage(roi, gender, filename, count)
        
        count = count + 1


# In[6]:

def genderLabel(full_path, filename):
    # Load raw image file into memory
    pathToFileInDisk = full_path
    with open( pathToFileInDisk, 'rb' ) as f:
        data = f.read()

    # Face detection parameters
    params = { 'returnFaceAttributes': 'age,gender', 
               'returnFaceLandmarks': 'true'} 

    headers = dict()
    headers['Ocp-Apim-Subscription-Key'] = _key
    headers['Content-Type'] = 'application/octet-stream'

    json = None

    result = processRequest( json, data, headers, params )
    
    if result is not None:

        # Load the original image from disk
        data8uint = np.fromstring( data, np.uint8 ) # Convert string to an unsigned int array
        #img = cv2.cvtColor( cv2.imdecode( data8uint, cv2.IMREAD_COLOR ), cv2.COLOR_BGR2RGB )
        img = cv2.imdecode( data8uint, cv2.IMREAD_COLOR )
        resultImage( result, img, filename )
        


# In[15]:

def search(dirname):

    if os.path.isdir(dirname):
        filenames = os.listdir(dirname)
        res=[]
        #print (filenames)
        for filename in filenames:
            full_filename = os.path.join(dirname, filename)
            if os.path.isdir(full_filename):
                res=search(full_filename)
            else:
                ext = os.path.splitext(full_filename)[-1]
                if ext == '.jpg' or ext == '.png':                 
                    t=[]
                    t.append(full_filename)
                    t.append(filename)
                    res.append(t)       
        return res
    


# In[16]:

import os
pwd = '/home/maru/Project/modu/data'
res = search(pwd)

#print (res)

# In[19]:

for i in range(len(res)):
    full_path = res[i][0]
    filename = res[i][1]
    
    print (full_path)
    print (filename)
    
    genderLabel(full_path, filename)


# In[ ]:



