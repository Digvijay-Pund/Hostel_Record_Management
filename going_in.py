import numpy as np
import cv2
import os
import face_recognition
from datetime import datetime

def show_image(image):
    cv2.imshow('XYZ', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

path = 'images'
images = []
names = []
myList = os.listdir(path)

print(myList)
for file in myList:
    current = cv2.imread(f'{path}/{file}')
    images.append(current)
    names.append(os.path.splitext(file)[0])
print(images,names)

def find_encodings(images):
    encoded_list = []
    for image in images:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(image)[0]
        encoded_list.append(encode)
    
    return encoded_list
encoding_known = find_encodings(images)
def entry(name):
  #  print("name",name)
    now = datetime.now()
    time = now.strftime('%H:%M:%S')
    if '-H' in name:
        with open('hostelite.csv', 'r+') as f:
            my_list = f.readlines()
            name_list = []
          #  print(my_list)
            for line in my_list:
                entry = line.split(',')
                name_list.append(entry[0])
          #  print(name_list)
            if(name not in name_list):

                f.writelines(f'\n{name},{time}')
            else:
                ans = []
                
                for i in my_list:
                    ans.append(i.split())
            #    print(ans)
                for i in range(len(ans)-1,0,-1):
                    if not ans[i]:
                        continue
                    else:
                        if name in ans[i][0] and len(ans[i][0]) >= 25:
               #             print('hi')
                            f.writelines(f'\n{name},{time}')
                        else:
                            break
    else:
        with open('non-hostelite.csv', 'r+') as f:
            my_list = f.readlines()
            name_list = []
          #  print(my_list)
            for line in my_list:
                entry = line.split(',')
                name_list.append(entry[0])
          #  print(name_list)
            if(name not in name_list):

                f.writelines(f'\n{name},{time}')
            else:
                ans = []
                
                for i in my_list:
                    ans.append(i.split())
           #     print(ans)
                for i in range(len(ans)-1,0,-1):
                    if not ans[i]:
                        continue
                    else:
                        if name in ans[i][0] and len(ans[i][0]) >= 25:
                       #     print('hi')
                            f.writelines(f'\n{name},{time}')
                        else:
                            break
cap = cv2.VideoCapture('video.mp4')
#cap = cv2.VideoCapture(0)

while True:
    _, img = cap.read()
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
        
    img_small = cv2.resize(img, (0,0), None, 0.50, 0.50)
    img_small = cv2.cvtColor(img_small, cv2.COLOR_BGR2RGB)
    
    faces_current = face_recognition.face_locations(img_small)
    encode_current = face_recognition.face_encodings(img_small, faces_current)
    
    for encodeF, faceLoc in zip(encode_current, faces_current):
        matches = face_recognition.compare_faces(encoding_known, encodeF)
        face_dis = face_recognition.face_distance(encoding_known, encodeF)
        matched_index = np.argmin(face_dis)
        
        if matches[matched_index]:
            name = names[matched_index].upper()
            #print(name)
            entry(name)
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1*2, x2*2, y2*2, x1*2
            cv2.rectangle(img, (x1+10, y1+10), (x2+10, y2+8), (0,255,0),2)
            cv2.rectangle(img,(x1+8, y2-20), (x2+7, y2+8), (0,255,0), cv2.FILLED)
            cv2.putText(img, name, (x1+10, y2-3), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255,255,255), 1)
            
    cv2.imshow('frame', img)
    
            
cap.release()
cv2.destroyAllWindows()