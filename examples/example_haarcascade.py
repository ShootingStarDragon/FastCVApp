#this example is importing from a higher level package: https://stackoverflow.com/a/41575089
import sys
sys.path.append('../FastCVApp')

import FastCVApp

app = FastCVApp.FCVA()
import cv2

if hasattr(sys, '_MEIPASS'):
    #if file is frozen by pyinstaller add the MEIPASS folder to path:
    sys.path.append(sys._MEIPASS)
    import os
    sourcing = os.path.join(sys._MEIPASS + os.sep + 'haarcascade_frontalface_default.xml')
    # print("source?", sourcing, flush = True)
    face_cascade = cv2.CascadeClassifier(sourcing)
else:
    #this example is importing from a higher level package: https://stackoverflow.com/a/41575089
    sys.path.append('../FastCVApp')
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')

def cascade_this(*args):
    #reference: https://stackoverflow.com/questions/70805922/why-does-the-haarcascades-does-not-work-on-opencv
    image = args[0]
    w_size = (700,500)
    image = cv2.resize(image,w_size)
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale( gray,scaleFactor=1.1,minNeighbors=5,minSize=(30, 30))

    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
    return cv2.flip(image,0)

app.appliedcv = cascade_this

if __name__ == '__main__' :
    app.source = "creativecommonsmedia/Elephants Dream charstart2.webm"
    app.fps = 1/30
    app.title = "Haarcascade example by Pengindoramu (\"works\" but Mediapipe is a lot better)"
    app.run()
    