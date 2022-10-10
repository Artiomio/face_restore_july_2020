import glob
from os import path
from time import time as current_time
import time
import keras

import dlib
import numpy as np
import cv2
from file_chooser import file_chooser



def dlib_and_opencv_facedetection(img, ):
    """  Функция для детектирования лица, которая
         в случае отсутствия лица в результатах dlib-а,
         запускает на всякий случай детектора лиц opencv
         NB: Считается, что на фото строго не больше одного лица
    """
    # dlib
    """
    dets = detector(img)
    faces_dlib = [(d.left(), d.top(), d.right(), d.bottom() ) for d in dets]
    if len(faces_dlib) > 0:
        return [(d.left(), d.top(), d.right(), d.bottom() ) for d in dets][0]

    
    # opencv
    """
    faces_opencv = face_cascade.detectMultiScale(img, 1.1, 3, minSize=(20, 20))

    if len(faces_opencv) > 0:
        x1, y1, a, b = faces_opencv[0]
        x2 = x1 + a
        y2 = y1 + b
        return x1, y1, x2, y2
    return None


webcam = cv2.VideoCapture(0)

want_to_exit = False 
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
detector = dlib.get_frontal_face_detector()


while True:

    
    model_path = file_chooser("./*.h5")
    model = keras.models.load_model(model_path)





    flipped = False
    zoom = 1

    start = current_time()
    frames_per_unit = 0

    x1, y1, x2, y2 = 0, 0, 200, 200
    d = 0
    i = 0

    print(model.summary())
    nn_input_shape =  model.layers[0].get_input_at(0).shape[1]
    print("nn_input_shape", nn_input_shape)
    N_DIM = nn_input_shape
    print("N_DIM", N_DIM)

    input("Press Enter to continue")

    bri = 1
    while(True):
        i += 1
        try:
            ret, frame = webcam.read()
            frame = cv2.blur(frame, (5, 5))

            frame -= frame.min()
            #frame = cv2.equalizeHist(frame)

            height, width, _ = frame.shape
            frame =  (cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) * bri)

            #frame -= frame.min()
            #frame /= 255
            
            if i % 100 == 0:
                
                faces = dlib_and_opencv_facedetection(frame)
                try:
                    x1, y1, x2, y2 = faces
                    #print((y2 - y1) / ( x2 - y2))
                except:
                    pass



            DISPLAY_WIDTH, DISPLAY_HEIGHT = 300, 300
            try:
                frame = frame[y1: y2, x1 : x2]
                #frame = cv2.resize(frame, (64, 64))

                frame = frame - frame.min()
                frame = frame / (frame.max() + 5 )
            except Exception as e:
                print('Error here', e)
                input('Press Enter to continue...')
                pass


#            frame = cv2.GaussianBlur(frame, (13, 13), 0)
            screen = cv2.resize(frame, (DISPLAY_WIDTH, DISPLAY_HEIGHT),
                                               interpolation=cv2.INTER_AREA)


            
            X = cv2.resize(frame[:frame.shape[0] // 2], (64, 32)).reshape(1, 64 * 32)
            #input()
 

            nn_img = model.predict(X, verbose=0).reshape(32, 64)
            nn_img = cv2.resize(nn_img, (DISPLAY_WIDTH, DISPLAY_HEIGHT // 2),
			interpolation=cv2.INTER_AREA)
            #cv2.imshow('Neural', nn_img)
            screen[DISPLAY_HEIGHT // 2:] = nn_img
            cv2.imshow('frame', screen)
        except Exception as e:
            print("Error!", e)


        
        key = cv2.waitKey(1)
        if key & 0xFF == 27:
            break


        if key & 0xFF == 32:
            flipped = not flipped

        if key & 0xFF == ord('q'):
            want_to_exit = True
            break
                           

        if key & 0xFF == ord('-'):
            d -= 1

        if key & 0xFF == ord('+'):
            d += 1

        if key & 0xFF == ord('3'):
            bri -= 0.05

        if key & 0xFF == ord('4'):
            bri += 0.05

                                    

    if want_to_exit:
        break
webcam.release()
cv2.destroyAllWindows()