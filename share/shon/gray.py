import os
from PIL import Image

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

# dataset = "/home/shon/mystuff/tensorflow/gender/total/female"
dataset = "/home/shon/mystuff/tensorflow/gender/total/male"
#print(dataset)
flist = getfilelist(dataset)
#print flist
#print(len(flist))

# img = Image.open("test/2.jpg")
# print img.size, img.mode
# #img.show()
# out = img.resize((128,128), Image.ANTIALIAS)
# print out.size, img.mode
# out.show()

#for f in flist:
for i in range(len(flist)):
    img = Image.open(flist[i]).convert('L')
    fn = "./grayresize/male/" + str(i) + '.jpg'
    # fn = "./grayresize/female/" + str(i) + '.jpg'
    #print fn
    out = img.resize((128, 128), Image.ANTIALIAS)
    out.save(fn)