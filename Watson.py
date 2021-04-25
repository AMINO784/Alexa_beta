import random
import webbrowser

import wikipedia as wikipedia

voice = "de-DE_BirgitV3Voice"
#de-DE_BirgitV3Voice
#de-DE_ErikaV3Voice
#de-DE_DieterV3Voice
user = "Felipe"

from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from playsound import playsound
import speech_recognition as sr
import pyaudio
import warnings
import datetime
import os
from time import sleep
import time
import pyfirmata
import requests
import requests
import wikipedia

einkaufsliste = [""]

wikipedia.set_lang("de")
#board = pyfirmata.Arduino('COM3')
warnings.filterwarnings('ignore')

#get token and URl from IBM Cloud
url = "YOUR_URL"
api = IAMAuthenticator("YOUR_TOKEN")


txt2sp = TextToSpeechV1(authenticator=api)
txt2sp.set_service_url(url)
r = sr.Recognizer()

seconds = 0
# say audio
def say(audio):
    with open("speech1.mp3", "wb") as audiofile:
        audiofile.write(
            txt2sp.synthesize(audio,
                              accept="audio/mp3",
                              voice=voice,
                              ).get_result().content
        )
    os.system("start speech1.mp3")
    sleep(3)


def rec_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening....")
        audio = r.listen(source)
    data = ''
    try:
        data = r.recognize_google(audio, language="de_DE")

        print(data)

    except sr.UnknownValueError:
        print('ein Fehler ist aufgetreten ')
    except sr.RequestError as e:
        print('ein Fehler ist aufgetreten ')
    return data
    sleep(2)


def wakeWord(text):
    WAKE_WORDS = ['Alexa']
    for phrase in WAKE_WORDS:
        if phrase in text:
            return True

    return False

def greet():
    h = datetime.datetime.now().hour
    if h >=0 and h <12:
        sp = datetime.datetime.now().strftime("Guten Morgen Amino es ist Momentan %H Uhr %M wie kann ich dir helfen?")
    elif h>= 12 and h<18:
        sp = datetime.datetime.now().strftime("Guten Mittag Amino es ist Momentan %H Uhr %M wie kann ich dir helfen?")
    else:
        sp = datetime.datetime.now().strftime("Guten Abend Amino es ist Momentan %H Uhr %M wie kann ich dir helfen?")
    say(sp)

def Witz():
    Witze = ["Was ist lustiger als ein totes Kind?      Ein Totes Kind im Clownskostüm",
             "Wie tötet eine Blondiene einen Vogel?       Sie schmeißt ihn aus dem Fenster",
             "Wenn Stiftung Warentest Vibratoren testet,              ist befriedigend dann besser als gut?   ",
             "Geht ein Cowboy zum Friseur. Als er wieder rauskommt, ist sein Pony weg.",
             "Was macht ein Pirat am Computer? Er drückt die Enter-Taste.",
             "Wie nennt man einen dicken Vegetarier?  Biotonne",
             "Hast du ein Bad genommen?        Warum,     fehlt eins?",
             "welche sind die teuersten Tomaten?          Die Geldautomaten.",
                "Was ist grün und steht vor der Tür?– Ein Klopfsalat",
             "Was kommt nach Elch? Zwölch. ",
             "Was fliegt durch die Luft und macht Mus Mus? Eine Biene im Rückwärtsgang! ",
             "Gute Nachricht: Ich bekomme endlich den obersten Knopf meiner superengen Jeans zu. Schlechte Nachricht: Habe sie leider nicht an. ",
             "Ein Mathematiker springt aus dem Fenster und fliegt nach oben? Was ist passiert? Vorzeichenfehler.",
             "Geht ein Cowboy zum Coiffeur. Als er wieder rauskommt, ist sein Pony weg."
             ]

    return random.choice(Witze)

def light_on():
    #board.digital[12].write(1)
    say("licht eins Wurde eingeschalten")


def light_off():
    #board.digital[12].write(0)
    say("licht eins wurde ausgeschalten")

def Uhrzeit(text):
    time = datetime.datetime.now().strftime("%H Uhr %M")
    say("es ist " + time)




while True:
    text = rec_audio()
    response = ""

    if (wakeWord(text) == True):

        data = text.split(" ")
        for i, s in enumerate(data):
            if s == 'Alexa':
                text = [x for x in data if data.index(x) >= i]
                break
        print(text)

        if "wie viel" and "Uhr" in text:
            Uhrzeit(text)

        elif ("Guten") and ("Mittag") in text:
            say("Guten Mittag")

        elif ("Witz") and ("erzähl mir") in text:
            say("okay lass mich überlegen")
            sleep(2)
            say(Witz())

        elif ("wo ist") in text:
            text = text.split(" ")
            location = text[3]
            say("Eine Sekunde ich werde dir zeigen wo " + location + " ist")
            os.system("MicrosoftEdge https://www.google.nl/maps/place/" + location)

        elif ("Einkaufsliste") and ("setze") in text:
            text = text.split(" ")
            item = text[2]
            say(f'ich habe {item} auf deine Einkaufsliste gesetzt')
            einkaufsliste.append(item)


        elif ("Einkaufsliste") and ("ist in") in text:
            say("momentan befindet sich " + str(einkaufsliste) + " in deiner Einkaufsliste")

        elif("aus meiner Einkaufsliste") and ("entferne" or "lösche") in text:
            text = text.split(" ")
            item = text[2]
            try:
                einkaufsliste.remove(item)
                say(f'{item} wurde aus deiner Einkaufsliste entfernt')
            except:
                say(f'{item} befindet sich nicht in deiner Einkaufsliste')


        #elif ("schalte Licht 1" or "schalte Licht eins") and "ein" in text:
           #light_on()

        #elif ("schalte Licht 1" or "schalte Licht eins") and "aus" in text:
            #light_off()

        elif ("Wetter in") in text:
           try:
            city = text.split("in").pop()
            api_key = "e1b8c7307dc5d97e97471350f44f8ab7"
            url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
            data = requests.get(url).json()
            temp = data['main']['temp']
            humidity = data['main']['humidity']

            say(f'In {city} beträgt die Temperatur {temp} Grad. Die Luftfeuchtigkeit beträgt {humidity}')

           except:
               say("Ich konnte den ort leider nicht finden")

        elif ("ist das") and ("Wetter") in text:
            city = "Brackenheim"
            api_key = "e1b8c7307dc5d97e97471350f44f8ab7"
            url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
            data = requests.get(url).json()
            temp = data['main']['temp']
            humidity = data['main']['humidity']

            say(f'In {city} beträgt die Temperatur {temp} Grad. Die Luftfeuchtigkeit beträgt {humidity}')

        elif ("was" and "ist") in text:
            person = text.split("ist")
            person = person.pop()
            say(f'eine Sekunde ich suche im internet nach {person}')
            say(wikipedia.summary(str(person), sentences=1))

        elif "wer" and "ist" in text:
            person = text.split("ist")
            person = person.pop()
            say(f'ich such im internet nach {person}')
            say(wikipedia.summary(str(person), sentences=1))

        elif "stop" in text:
            say("okay")




