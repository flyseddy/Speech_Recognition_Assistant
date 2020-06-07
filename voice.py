
from PyQt5 import QtCore, QtGui, QtWidgets
import subprocess
import speech_recognition as sr 
import sys
from playsound import playsound
from gtts import gTTS
import os
import subprocess
import cv2
import numpy as np 
import threading
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import time
from multiprocessing import Process
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QIcon, QMovie

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        # MainWindow.resize(233, 336)
        MainWindow.setFixedSize(233, 350)
        MainWindow.setAutoFillBackground(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        self.button1 = QtWidgets.QPushButton(self.centralwidget)
        self.button1.setGeometry(QtCore.QRect(60, 160, 101, 31))
        self.button1.setObjectName("button1")
        
        self.button2 = QtWidgets.QPushButton(self.centralwidget)
        self.button2.setGeometry(QtCore.QRect(60, 200, 101, 31))
        self.button2.setObjectName('button2')
        self.button2.setEnabled(False)

        self.label1 = QtWidgets.QLabel(self.centralwidget)
        self.label1.setGeometry(QtCore.QRect(60, 110, 91, 21))
        self.label1.setAutoFillBackground(True)
        self.label1.setObjectName("label1")

        # Loading icon gif - we will set its visibility to false orignally
        self.label2 = QtWidgets.QLabel(self.centralwidget)
        self.label2.setGeometry(QtCore.QRect(60, 50, 100, 100))
        self.label2.setObjectName("wheel")
        self.label2.setHidden(True)

        self.gif = QMovie('loading_gif/loading.gif')
        # self.label2.setMovie(self.gif)
        

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 233, 20))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)  

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        app.aboutToQuit.connect(self.closeEvent)

        # The 2 button actions speak and end
        self.button1.clicked.connect(lambda: self.status())
        self.button2.clicked.connect(lambda: self.end_task('Say Something'))

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Khaleesi"))
        MainWindow.setWindowIcon(QtGui.QIcon('window_icon/icon.png'))
        self.button1.setText(_translate("MainWindow", "Speak"))
        self.button2.setText(_translate("MainWindow", "End"))
        self.label1.setText(_translate("MainWindow", "Say Something"))
    
    # Give it a status of running before it starts processing the request in another thread
    def status(self):
        # Hides the current label so the loading icon can show
        self.label1.setHidden(True)
        # Unhides the loading icon
        self.label2.setHidden(False)
        self.label2.setMovie(self.gif)
        self.gif.start()
        time.sleep(.2)
       # self.setLabel(text)
        threading.Thread(target=self.clicked).start()
    
    # Close method that kills all proccesses when user clicks red x in upper right hand corner
    def closeEvent(self):
        try:
            if p:
                stop_song()
                print("Window Closed")
                os._exit(0)
        except NameError:
            pass
        else:
            print("Window Closed")
            os._exit(0)
        
    # Speak Button Clicked method
    def clicked(self):
        # Enables the "end" button to kill the process
        self.button2.setEnabled(True)
        microphone_input()
        self.button2.setCheckable(True)
        self.update()
       
    # My own method to set the label to the input if it doesn't match a certain command
    def setLabel(self, text):
        self.label2.setHidden(True)
        self.label1.setHidden(False)
        self.label1.setText(text)
        self.update()

    # Automatically adjusts the label size
    def update(self):
        self.label1.adjustSize()


    # Same as end process
    def end_task(self, text):
        time.sleep(.2)
        self.setLabel(text)
        self.button2.setEnabled(False)
        self.button1.setEnabled(True)
        
def microphone_input():
    """ Process the Microphone input and tokenizes it"""
    # Turns speak button off while processing to prevent spam clicking
    ui.button1.setEnabled(False)

    # Obtain audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
    try:
        # Return nothing when end button is checked
        if ui.button2.isChecked():
            return None
        sentence = r.recognize_google(audio).lower()
        process_text_tokenize(sentence)
    except sr.UnknownValueError:
        # Return nothing when end button is checked
        if ui.button2.isChecked():
            return None
        # print("Google Speech Recognition could not understand audio")
        dont_recognize_command()
        sys.exit()
    except sr.RequestError as e:
        print("Could not request results from Speech Recognition service; {0}".format(e))

# this method filters the incoming sentence to get rid of stop words
def process_text_tokenize(processed_text):
    stop_words = set(stopwords.words('english'))

    words_tokens = word_tokenize(processed_text)
    # Empty list
    filtered_sentence = []
    for w in words_tokens:
        if w not in stop_words:
            filtered_sentence.append(w)
    process_text(filtered_sentence)

def process_text(text):
    global romantic
    if 'romantic' in text:
        threading.Thread(target=play_video, args=('videos/fireplace',)).start()
        # romantic = Process(target=play_video, args=('fireplace',))
        #romantic.start()
        start_playback_song('coffee')
    elif 'father' in text:
        tts = gTTS('You are my creator and I love you!', lang='en')
        tts.save('hey.mp3')
        playsound('hey.mp3')
        os.remove('hey.mp3')
        end_of_process()
    elif 'spotify' in text:
        subprocess.Popen('C:\\Users\\serdr\\AppData\\Roaming\\Spotify\\Spotify.exe')
        end_of_process()
    elif 'sad' in text:
        threading.Thread(target=play_video, args=('videos/sad_song',)).start()
        start_playback_song('505')
    else:
        dont_recognize_command()
        
def dont_recognize_command():
    ui.button2.setEnabled(False)
    ui.button1.setEnabled(True)
    ui.setLabel("Couldn't recognize command")

# Sets button2 to false (it cant be triggered)
def set_button2_false():
    ui.button2.setEnabled(False)

def start_playback_song(name_of_song):
    # Make a global variable so any method can access this object
    global p
    p = Process(target=playsound, args=(f'songs/{name_of_song}.mp3',))
    play_song()

def play_song():
    p.start()

def stop_song():
    p.terminate()

def play_video(name_of_video):
    # Create a VideoCapture object and read from imput file
    cap = cv2.VideoCapture(f"{name_of_video}.mp4")

    # Check if camera opened successfully
    if (cap.isOpened()==False):
        setLabel('Error Opening video file')
    
    cv2.namedWindow('Window', cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty('Window', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    # Read until the video is completed
    
    while(cap.isOpened()):
        ui.button1.setEnabled(False)
        # ui.button1.setEnabled(False) # Wont allow button to be pressed while video is opened
        # Capture frame by frame
        ret, frame = cap.read()
        if ret == True:

            # Display the resulting frame
            cv2.imshow('Frame', frame)

            
            
            if ui.button2.isChecked():
                stop_song()
                end_of_process()
                break
            
            # Press Q on keyboard to exit
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        # Break the loop
        else:
            break
    # When everything is done, release the video capture object
    cap.release()
    # Closes all the frames
    cv2.destroyAllWindows()
    stop_song()
    end_of_process()

def end_of_process():
    # ui.label2.setHidden(False)
    ui.setLabel('Say Something')
    ui.label1.setHidden(False)
    ui.button1.setEnabled(True)
    ui.button2.setCheckable(False)
    ui.button2.setEnabled(False)
    
       

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    style = """
        QWidget{
            background: #000000;
        }
        QLabel{
            color: #fff;
        }
        QPushButton{
            color: white;
            background: #9a05a8;
            border: 1px #DADADA solid;
            padding: 5px 10px;
            border-radius: 2px;
            font-weight: bold;
            font-size: 9pt;
            outline: none;
        }
    """
    app.setStyleSheet(style)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
