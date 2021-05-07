import os
import cv2
from PIL import Image
import numpy as np
import pickle
BASE_DIR = os.path.dirname(os.path.abspath(__file__ )) 
img_dir= os.path.join(BASE_DIR,"images")
face_cascade=cv2.CascadeClassifier('FaceOpenCv/data/haarcascade_frontalface_alt2.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()
current_id =0 
label_ids={}
y_labels=[]
x_train=[]
stt=0
for root,dirs,files in os.walk(img_dir):
    for file in files:
        if file.endswith('png') or file.endswith('jpg'):
            path = os.path.join(root,file)
            label=os.path.basename(root).replace(' ','-').lower()
            # print(label,path)
            if not  label in label_ids:
                current_id+=1
                label_ids[label]=current_id
                id_= label_ids[label]
            # print(label_ids)
            # y_labels.append(label) 
            # x_train.append(path)
            pil_image=Image.open(path).convert('L') #grayscale
            size=(550,550)
            # final_image= pil_image.resize(size,Image.ANTIALIAS)
            final_image= pil_image
            image_array=np.array(final_image,'uint8')
            # print(image_array)    
            faces = face_cascade.detectMultiScale(image_array,scaleFactor=1.1,minNeighbors=4)

            for (x,y,w,h) in faces:
                roi = image_array[y:y+h,x:x+w]
                print(x_train)
                print(y_labels)
                x_train.append(roi)
                y_labels.append(id_)
                cv2.rectangle(image_array, (x, y), (x+w, y +h), (0, 255,0), 2)

                stt+=1
            cv2.imshow(f'{stt}',image_array)
                

with open('labels.pickle','wb') as f:
    pickle.dump(label_ids,f )


recognizer.train(x_train,np.array(y_labels))
recognizer.save("trainner.yml")
cv2.waitKey(0)