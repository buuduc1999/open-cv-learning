import os
import cv2
import face_recognition
# from PIL import Image
import numpy as np
import pickle
import imutils
from datetime import datetime, timedelta
from csv import writer

BASE_DIR = os.path.dirname(os.path.abspath(__file__ )) 
# img_dir= os.path.join(BASE_DIR,"images")
img_dir='FaceOpenCvV2/images'
current_id =0 
label_ids={}
y_labels=[]
x_train=[]
stt=0

peopleCheckin ={}
def markAttendance(name):
        # Open file in append mode
    with open('Attendance.csv', 'a+', newline='') as write_obj:
        now = datetime.now()
        dtString= now.strftime('%H:%M:%S  %D')
        # Create a writer object from csv module
        csv_writer = writer(write_obj)
        # Add contents of list as last row in the csv file
        csv_writer.writerow([name,dtString])
    
def checkAttendance(name):
    if name not in peopleCheckin:
        peopleCheckin[name]={'time': datetime.now()-timedelta(seconds=50),'count': 1,'checkin': False}
    if datetime.now() - peopleCheckin[name]['time'] > timedelta(seconds=5):
        if peopleCheckin[name]['count']>2:
            peopleCheckin[name]['count']=0
            peopleCheckin[name]['checkin']=True
            peopleCheckin[name]['time']=datetime.now()
            markAttendance(name)
            
        else:
            peopleCheckin[name]['count']+=1
    # print(peopleCheckin[name])

def initAttendance():
    with open('Attendance.csv','w') as f:
        f.writelines('Name, Date \n')
def deleteFrameCheck():
    for key in peopleCheckin:
                peopleCheckin[key]['count']=0
def recForFace(frame,name,x,y,end_cord_x,end_cord_y):
    stroke =2 
    # color =(255,0,0)
    # check='unknown human'
    if (name == 'unknown'):
        color =(255,0,0)
        check='unknown human'
    elif peopleCheckin[name]['checkin']:
        color =(0,255,0)
        check ='checked'
    else:
        color =(0,0,255)
        check ='uncheck'
    cv2.rectangle(frame,(x,y),(end_cord_x,y-20),color,cv2.FILLED) #o unknown tren cung
    cv2.rectangle(frame,(x,y),(end_cord_x,end_cord_y),color,stroke)
    cv2.rectangle(frame,(x,end_cord_y-35),(end_cord_x,end_cord_y),color,cv2.FILLED) #o ten ben duoi
    cv2.putText(frame,name,(x+6,end_cord_y-6),cv2.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),1)# CHU XUAT HIEN BEN DUOI


    cv2.putText(frame,check,(x+6,y-2),cv2.FONT_HERSHEY_COMPLEX,0.25,(255,255,255),1)

with open('dataset_faces.dat', 'rb') as f:
	all_face_encodings = pickle.load(f)

# Grab the list of names and the list of encodings
faceNameArray = list(all_face_encodings.keys())
faceEncodeArray = np.array(list(all_face_encodings.values()))

initAttendance()
cap = cv2.VideoCapture(0)
while True: 
    # img=cv2.imread('FaceRecognition/ImagesBasic/wc2.jpg')
    success , realImg = cap.read()
    # realImg = cv2.resize(realImg,(480,320))
    realImg=imutils.resize(realImg,width=500)
    img = cv2.cvtColor(realImg, cv2.COLOR_BGR2RGB)
    print(len(face_recognition.face_locations(img)))
    
    for i in range(len(face_recognition.face_locations(img))):

        facesCurFrame = face_recognition.face_locations(img)[i]
        encodesCurFrame = face_recognition.face_encodings(img)[i]
        y1,x2,y2,x1 = facesCurFrame

        # cv2.rectangle(img,(facesCurFrame[3],facesCurFrame[0]),(facesCurFrame[1],facesCurFrame[2]),(255,0,255),2)
        matches = face_recognition.compare_faces(faceEncodeArray,encodesCurFrame)
        faceDis = face_recognition.face_distance(faceEncodeArray,encodesCurFrame)
        faceNameArrayTemp=faceNameArray
        while True:
            minIndex=np.argmin(faceDis)
            if matches[minIndex]:
                checkAttendance(faceNameArray[minIndex])
                recForFace(realImg,faceNameArray[minIndex],x1,y1,x2,y2+40)
                print(faceNameArray[minIndex])
                break
            if len(matches)<=1:
                break
            faceDis=np.delete(faceDis,minIndex)
            matches=np.delete(matches,minIndex)
            faceNameArrayTemp=np.delete(faceNameArrayTemp,minIndex)
        print(faceDis,matches)
        
        # recForFace(realImg,faceNameArray[index],x1,y1,x2,y2+40)


        # cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
        # cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
        # cv2.putText(img,'duc',(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
    resizeCamera=cv2.resize(realImg,(720,480))
    cv2.imshow('Webcam',resizeCamera)
    cv2.waitKey(20)
