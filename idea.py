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


def microphone_input():
    # Obtain audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say Something!")
        audio = r.listen(source)

    try:
        sentence = r.recognize_google(audio).lower()
        process_text_tokenize(sentence)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

# This method filters the incoming sentence to get rid of stop words
def process_text_tokenize(processed_text):
    stop_words = set(stopwords.words('english'))

    word_tokens = word_tokenize(processed_text)
    # Empty list
    filtered_sentence = []
    for w in word_tokens:
        if w not in stop_words:
            filtered_sentence.append(w)
    # print(filtered_sentence)
    process_text(filtered_sentence)

def process_text(text):
    if 'romantic' in text:
        threading.Thread(target=play_video, args=('fireplace',)).start()
        threading.Thread(target=start_playback_song, args=('coffee',)).start()
        # play_video()
       # start_playback_song()       
    elif 'daddy' in text:
        tts = gTTS('You are my daddy, seddy and you are so fucking sexy', lang='en')
        tts.save('hey.mp3')
        playsound('hey.mp3')
        os.remove('hey.mp3')
    elif 'spotify' in text:
        subprocess.Popen('C:\\Users\\serdr\\AppData\\Roaming\\Spotify\\Spotify.exe')
    elif 'sad' in text:
        threading.Thread(target=play_video, args=('sad_song',)).start()
        threading.Thread(target=start_playback_song, args=('505',)).start()
    else:
        print(text)

def start_playback_song(name_of_song):
    playsound(f'songs/{name_of_song}.mp3')

def play_video(name_of_video):
    # Create a VideoCapture object and read from input file
    cap = cv2.VideoCapture(f"{name_of_video}.mp4")

    # Check if camera opened successfully
    if (cap.isOpened()== False):
        print("Error opening video file")

    cv2.namedWindow('Window', cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty('Window', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    
    # Read until the video is completed
    while(cap.isOpened()):

        # Capture frame by frame
        ret, frame = cap.read()
        if ret == True:

            # Display the resulting frame
            cv2.imshow('Frame', frame)

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

microphone_input()


    


