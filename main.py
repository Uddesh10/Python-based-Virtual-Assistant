import tkinter as tk # tkinter library for GUI
from tkinter import StringVar, ttk
from PIL import Image , ImageTk #PIL library to show image on window
import speech_recognition as sr # recognise speech
import playsound # to play an audio files
from gtts import gTTS # google text to speech
import random #random number generator
from time import ctime # get time details
import webbrowser # open browser
import os # to remove created audio files
import pyttsx3 #text to speech library

# create application window
window = tk.Tk()
window.title('Virtual Assistant')
window_width = 300
window_height = 400
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
center_x = int(screen_width/2 - window_width / 2)
center_y = int(screen_height/2 - window_height / 2)
window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
window.resizable(False, False)
voice_data = ''
labelText = StringVar()
labelText2 = StringVar()
labelText.set("Tap on mic to speak")
labelText2.set("")
text_label2 = ttk.Label(window,textvariable=labelText2,font=("Times", 18),wraplength=300,justify="center")
text_label2.pack(ipadx=0, ipady=11)
text_label = ttk.Label(window,textvariable=labelText,font=("Times", 18),wraplength=300,justify="center")
text_label.pack(ipadx=0, ipady=11)
mic_img = Image.open('./mic.png')
mic_lbl = tk.Label(window)
mic_lbl.place(x=98,y=290)
img = mic_img.resize((100,100))
img = ImageTk.PhotoImage(img)
mic_lbl.config(image=img)
mic_lbl.bind("<Button-1>",lambda e:start())

class User:
    name = ''
    def setName(self, name):
        self.name = name

class Asistant:
    name = ''
    def setName(self, name):
        self.name = name

def there_exists(terms):
    for term in terms:
        if term in voice_data:
            return True

#text to speech engine
def engine_speak(text):
    text = str(text)
    engine.say(text)
    engine.runAndWait()

r = sr.Recognizer() # initialise a recogniser
# listen for audio and convert it to text:
def record_audio(ask=""):
    with sr.Microphone() as source: # microphone as source
        if ask:
            engine_speak(ask)
        audio = r.listen(source, 5, 5)  # listen for the audio via source
        voice_data = ''
        try:
            labelText.set("Processing...")
            voice_data = r.recognize_google(audio)  # convert audio to text
        except sr.UnknownValueError: # error: recognizer does not understand
            labelText.set("Tap on mic to speak")
            engine_speak('I did not get that')
        except sr.RequestError:
            engine_speak('Sorry, the service is down') # error: recognizer is not connected
        return voice_data.lower()

# get string and make a audio file to be played
def engine_speak(audio_string):
    audio_string = str(audio_string)
    tts = gTTS(text=audio_string, lang='en') # text to speech(voice)
    labelText.set(asis_obj.name + ":" + audio_string) # print what app said
    r = random.randint(1,20000000)
    audio_file = 'audio' + str(r) + '.mp3'
    tts.save(audio_file) # save as mp3
    playsound.playsound(audio_file) # play the audio file
    os.remove(audio_file) # remove audio file


def respond(voice_data):
    labelText2.set("You:"+voice_data)
    # 1: greeting
    if there_exists(['hey','hi','hello','heya','hola','hai']):
        greetings = ["hey, how can I help you" + user_obj.name, "hey, what's up?" + user_obj.name, "I'm listening" + user_obj.name, "how can I help you?" + user_obj.name, "hello" + user_obj.name]
        greet = greetings[random.randint(0,len(greetings)-1)]
        engine_speak(greet)
        return

    # 2: name
    if there_exists(["what is your name","what's your name","tell me your name"]):
        if user_obj.name:
            engine_speak("My name is Virtuala")
            return
        else:
            engine_speak("My name is Virtuala. what's your name?")
            playsound.playsound("./start.mp3")
            voice_data = record_audio("")
            playsound.playsound("./stop.mp3")
            user_name = voice_data.split("is")[-1].strip()
            engine_speak("okay, i will remember that "+user_name)
            user_obj.setName(user_name) # remember name in person object
        return


    # 3: greeting
    if there_exists(["how are you","how are you doing",'whatsup',]):
        engine_speak("I'm very well, thanks for asking " + user_obj.name)
        return

    # 4: time
    if there_exists(["what's the time","tell me the time","what time is it","tell me the time","what time is it"]):
        time = ctime().split(" ")[3].split(":")[0:2]
        if time[0] == "00":
            hours = '12'
        else:
            hours = time[0]
        minutes = time[1]
        time = hours + " hours and " + minutes + "minutes"
        engine_speak(time)
        return

    # 5: search google
    if there_exists(["search for"]):
        search_term = voice_data.split("for")[-1]
        url = "https://google.com/search?q=" + search_term
        webbrowser.get().open(url)
        engine_speak("Here is what I found for" + search_term + " on google")
        return

    #6: open any site
    if there_exists(["open"]):
        search_term = voice_data.split("open")[-1].strip()
        url = "https://"+search_term.replace(" ","") +".com/"
        webbrowser.get().open(url)
        engine_speak("Opening "+search_term)
        return

    # 7: search video on youtube
    if there_exists(["search video","search youtube"]):
        engine_speak("What you want to search on youtube")
        playsound.playsound("./start.mp3") 
        voice_data = record_audio("")
        playsound.playsound("./stop.mp3") 
        search_term = voice_data.split("video")[-1]
        url = "https://www.youtube.com/results?search_query=" + search_term
        webbrowser.get().open(url)
        engine_speak("Here is what I found for " + search_term + " on youtube")
        return

    #8: play music
    if there_exists(["play"]):
        search_term= voice_data.split("play")[-1]
        url="https://open.spotify.com/search/"+search_term
        webbrowser.get().open(url)
        engine_speak("Opening "+ search_term + " on Spotify")
        return

    #9: Weather
    if there_exists(["what is today's weather","weather","today's weather"]):
        url = "https://www.accuweather.com/"
        webbrowser.get().open(url)
        engine_speak("Today's weather forecast")
        return

    #10: make a note
    if there_exists(["make a note"]):
        search_term=voice_data.split("note")[-1]
        url="https://keep.google.com/#home"
        webbrowser.get().open(url)
        engine_speak("Here you can make notes")
        return

    #11: News
    if there_exists(["show news","news"]):
        engine_speak("Which news do you want to read")
        playsound.playsound("./start.mp3") 
        voice_data = record_audio("")
        playsound.playsound("./stop.mp3")
        if voice_data=="top stories"or voice_data=="top news":
            url = "https://news.google.com/"
            webbrowser.get().open(url)
            engine_speak("Here are the top stories")
            return
        else:
            url = "https://news.google.com/search?q="+voice_data
            webbrowser.get().open(url)
            engine_speak("Opening news on "+voice_data)
            return

    #12 to search wikipedia for definition
    if there_exists(["what is"]):
        definition = voice_data.split("is")[-1]
        url='https://en.wikipedia.org/wiki/'+definition
        webbrowser.get().open(url)
        engine_speak("Here is what I found for " + definition + " on wikipedia")
        return

    #13 Exit
    if there_exists(["exit", "quit", "goodbye"]):
        engine_speak("See Yaa.......Bye!")
        exit()

user_obj = User()
asis_obj = Asistant()
asis_obj.name = 'Kim'
engine = pyttsx3.init()

def start():
  playsound.playsound("./start.mp3")   
  global voice_data
  voice_data = record_audio("") # get the voice input
  playsound.playsound("./stop.mp3")
  labelText.set("Q: "+ voice_data)
  respond(voice_data) # respond
window.mainloop()