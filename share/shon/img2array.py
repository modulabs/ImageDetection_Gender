import os
from PIL import Image
import numpy as np

# get image file list in dataset
def getfilelist(dirname):
    flist = []
    filenames = os.listdir(dirname)
    for filename in filenames:
        full_filename = os.path.join(dirname, filename)
        ext = os.path.splitext(full_filename)[-1]
        if ext == '.jpg' or ext == '.JPEG' or ext == '.jpeg':
            flist.append(full_filename)
            #print(full_filename)
    return flist

dataset = "/home/shon/mystuff/tensorflow/gender/total/grayresize/male"
flist = getfilelist(dataset)

img1 = Image.open("grayresize/male/1.jpg")
img1arr = np.array(img1)
X = np.reshape(img1arr, 16384)

for i in range(len(flist)):
    img = Image.open(flist[i]).convert('L')
    imgarr = np.array(img)
    imgvec = np.reshape(imgarr, 16384)
    X = np.vstack((X, imgvec))

dataset = "/home/shon/mystuff/tensorflow/gender/total/grayresize/female"
flist = getfilelist(dataset)
print len(X)-1, 3107

for i in range(len(flist)):
    img = Image.open(flist[i]).convert('L')
    imgarr = np.array(img)
    imgvec = np.reshape(imgarr, 16384)
    X = np.vstack((X, imgvec))

# print len(X)
X = X[1:]
print len(X), 3107+2252, 5359

np.save('X.npy', X)