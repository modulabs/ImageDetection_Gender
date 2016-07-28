# -*- coding: utf-8 -*-
# only LFW Face Database
import os
import sys
from django.http import request
from os import rename
import requests
import shutil

__author__ = 'Philip Masek'



def main(argv):
    #fileList = []
    #fileSize = 0
    #folderCount = 0
    rootdir = "rootdir" # 이미지 데이터가 있는 폴더
    maleFolder = "result/male"  # 남자 이미지를 copy 할 폴더(결과)
    femaleFolder = "result/female"  # 여자 이미지를 copy 할 폴더(결과)
    count = 0  # 진행 count
    tmp = ""

    for root, subFolders, files in os.walk(rootdir): # rootdir에서 시작하여 그 하위의 모든 폴더, 파일을 차례대로 방문
        #folderCount += len(subFolders)    # roodir 하위 폴더의 개수
        for file in files:
            f = os.path.join(root,file)  # file 경로
            #fileSize = fileSize + os.path.getsize(f)  # file size  
            fileSplit = file.split("_")  # filename 을 _ 로 분리
            #fileList.append(f)
            count += 1

            if count == 1:
                result = requests.get("http://api.genderize.io?name=%s" % fileSplit[0])    # http request 로 genderize.io api 사용 fileSplit[0] => 이미지 파일명의 _ 앞부분(즉, 이름), result => {"name":"Edward","gender":"male","probability":"1.00","count":1015}

                result = result.json()    # json 형식으로 변환
                tmp = fileSplit[0]
            elif tmp != fileSplit[0]:
                result = requests.get("http://api.genderize.io?name=%s" % fileSplit[0])
                result = result.json()
                tmp = fileSplit[0]
            else:
                tmp = fileSplit[0]

            try:
                if float(result['probability']) > 0.9:    # 예측 값이 0.9 초과인 경우
                    if result['gender'] == 'male':    # gender 속성의 값이 male 인 경우
                        shutil.copyfile(f,"%s/%s" % (maleFolder, file))    # maleFolder 에 file 복사
                    elif result['gender'] == 'female':
                        shutil.copyfile(f,"%s/%s" % (femaleFolder, file))
            except Exception as e:
                print result['name']    # exception 발생 시 name 출력

            print count   # 진행 되는 count 출력



if __name__ == "__main__":
    main(sys.argv)
