import getpass 
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
from test_joke import test_joke
from weather import find_weather
from response import father, mother

sys.setrecursionlimit(100000)

# Stores the current windows username to access files on system
user = getpass.getuser()

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
        threading.Thread(target=self.clicked).start()
    
    # Close method that kills all proccesses when user clicks red x in upper right hand corner
    def closeEvent(self):
        try:
            if p:
                stop_song()
                os._exit(0)
        except NameError:
            pass
        else:
            os._exit(0)
        
    # Speak Button Clicked method
    def clicked(self):
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
        # Ends the music process if activated since it's a background process
        try:
            if p:
                stop_song()
        except NameError:
            pass
        time.sleep(.2)
        self.setLabel(text)
        self.button2.setEnabled(False)
        self.button1.setEnabled(True)
        
def microphone_input():
    
    """ Process the Microphone input and tokenizes it"""
    # Turns speak and end button off while processing to prevent spam clicking and abnormal processes
    ui.button1.setEnabled(False)
    ui.button2.setEnabled(False)

    # Obtain audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
    try:
        sentence = r.recognize_google(audio).lower()
        process_text_tokenize(sentence)
    except sr.UnknownValueError:
        # Couldn't recognize command
        dont_recognize_command()
        time.sleep(1)
        end_of_process()
    except sr.RequestError as e:
        ui.setLabel('Error')

# this method filters the incoming sentence to get rid of stop words
def process_text_tokenize(processed_text):
    stop_words = set(stopwords.words('english'))
    words_tokens = word_tokenize(processed_text)
    # Empty list which will contain filtered tokens
    filtered_sentence = []
    for w in words_tokens:
        if w not in stop_words:
            filtered_sentence.append(w)
    process_text(filtered_sentence)
    
def process_text(text):
    """Commands go here in the if and else statements"""
    global p
    if 'romantic' in text and 'mode' in text:
        t1 = threading.Thread(target=play_video, args=('videos/fireplace_new',))
        p = Process(target=playsound, args=('songs/romantic.mp3',))
        p.start()
        t1.start()
    elif 'father' in text or 'daddy' in text or 'dad' in text or 'creator' in text:
        dad_response = father()
        tts = gTTS(dad_response, lang='en')
        tts.save('dad.mp3')
        playsound('dad.mp3')
        os.remove('dad.mp3')
        end_of_process()
    elif 'mother' in text or 'mom' in text or 'mommy' in text:
        mom_response = mother()
        tts = gTTS(mom_response, lang='en')
        tts.save('mom.mp3')
        playsound('mom.mp3')
        os.remove('mom.mp3')
        end_of_process()
    elif 'spotify' in text:
        try:
            subprocess.Popen(f'C:\\Users\\{user}\\AppData\\Roaming\\Spotify\\Spotify.exe')
            end_of_process()
        except FileNotFoundError:
            ui.setLabel('File Not Found')
            time.sleep(1)
            end_of_process()
    elif 'sad' in text:
        t1 = threading.Thread(target=play_video, args=('videos/sad_song_new',))
        p = Process(target=playsound, args=('songs/sad_song_song.mp3',))
        p.start()
        t1.start()
    elif 'joke' in text:
        # Creates instance of joke object
        random_joke = test_joke()
        tts = gTTS(random_joke, lang='en')
        tts.save('joke.mp3')
        playsound('joke.mp3')
        os.remove('joke.mp3')
        end_of_process()
    elif 'weather' in text:
        tts = gTTS(process_weather(text), lang='en')
        tts.save('weather.mp3')
        playsound('weather.mp3')
        os.remove('weather.mp3')
        end_of_process()         
    else:
        dont_recognize_command()
        time.sleep(1)
        end_of_process()
        
def dont_recognize_command():
    ui.button2.setEnabled(False)
    ui.button1.setEnabled(True)
    ui.setLabel("Couldn't recognize command")

def stop_song():
    p.terminate()

def play_video(name_of_video):
    # Create a VideoCapture object and read from imput file
    cap = cv2.VideoCapture(f"{name_of_video}.mp4")

    # Check if camera opened successfully
    if (cap.isOpened()==False):
        setLabel('Error Opening video file')
    # Read until the video is completed
    while(cap.isOpened()):
        ui.button2.setEnabled(True)
        # Wont allow button to be pressed while video is opened
        ui.button1.setEnabled(False)
        # Capture frame by frame
        ret, frame = cap.read()
        if ret == True:

            # Display the resulting frame
            cv2.imshow('Show', frame)

            if ui.button2.isChecked():
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
    if p:
        stop_song()
    end_of_process()

# method to process weather requests using openweathermap API
def process_weather(text):
    new_list = text[-2:]
    if 'weather' in new_list:
        final_list = new_list[-1:]
        string_city = final_list.pop()
        weather = find_weather(string_city)
        if weather == None:
            dont_recognize_command()
            time.sleep(1)
            end_of_process()
            sys.exit()
        formatted_weather = f"{weather} degrees fahrenheit" 
        return formatted_weather
    else:
        # pops the last 2 words out and concatenates them
        word_1 = new_list.pop(-2)
        word_2 = new_list.pop(-1)
        string_city = f"{word_1} {word_2}"
        weather = find_weather(string_city)
        if weather == None:
            dont_recognize_command()
            time.sleep(1)
            end_of_process()
            sys.exit()
        formatted_weather = f"{weather} degrees fahrenheit"
        return formatted_weather

# Method to handle end processes
def end_of_process():
    ui.setLabel('Say Something')
    ui.label1.setHidden(False)
    ui.button1.setEnabled(True)
    ui.button2.setCheckable(False)
    ui.button2.setEnabled(False)   

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    style = """
        QWidget{
            background: #000000;
        }
        QLabel{
            color: #fff;
            font-weight:bold;

        }
        QPushButton{
            color: white;
            background: #9a05a8;
            border: 1px #DADADA solid;
            padding: 5px 10px;
            border-radius: 4px;
            font-weight: bold;
            font-size: 9pt;
            outline: none;
        }
    """
    app.setStyleSheet(style)
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
