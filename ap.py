import pyttsx3
from vosk import Model, KaldiRecognizer
#import speech_recognition as sr
from pyaudio import PyAudio, paInt16
import json
from eventhook import Event_hook
from threading import Thread, Lock
from log import Logger
from functions import Functions

"""
pip install vosk
download the models from https://alphacephei.com/vosk/models
"""

class AP():
    __name = ""
    __skill = []
    lock = Lock()
   
    def __init__(self, name=None):
        self.engine = pyttsx3.init()

        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice' , voices[0].id)
        name = "AP"
        print(name)

        model = Model('./model') # path to model
        self.r = KaldiRecognizer(model, 16000)

        self.m = PyAudio()

        if name is not None:
            self.__name = name 

        self.audio = self.m.open(format=paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
        self.audio.start_stream()
        
        print("Listening")
        with self.m as source: 
            self.r.adjust_for_ambient_noise(source)

        self.functions: Functions = Functions()
        self.logger: Logger = Logger()

        # Setup event hooks
        self.before_speaking = Event_hook()
        self.after_speaking = Event_hook()
        self.before_listening = Event_hook()
        self.after_listening = Event_hook()
        self.start = Event_hook()
        self.stop = Event_hook()

    @property 
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        sentence = "Hola, mi nombre es" + self.__name
        self.__name = value
        self.engine.say(sentence)
        self.engine.runAndWait()

    def _speak(self, sentence):
        
        # Lock the thread so it doesn't try to speak while it is already speaking
        self.lock.acquire()
        print(sentence)
        self.before_speaking.trigger(sentence)
        self.engine.say(sentence)
        self.engine.runAndWait()
        self.after_speaking.trigger(sentence)

        # Release the lock
        self.lock.release()


    def say(self, sentence):
        """ Launch a new thread to speak """
        if self.engine._inLoop:
            # self.engine.iterate()
            self.engine.endLoop()
        while self.lock.locked():
            pass
        t = Thread(target = self._speak, args = (sentence,))
        t.start()

    def force_speak(self, sentence):
        """ 
        Force to Speak the AP
        ------
        ! Important ! Stops Other Loops or Speaks
        """
        try:
            self.engine.endLoop()
        except:
            pass

        print(sentence)
        self.before_speaking.trigger(sentence)
        self.engine.say(sentence)
        self.engine.runAndWait()
        self.after_speaking.trigger(sentence)

        
    def listen(self, trigger: bool = True):
        phrase = ""
        if self.r.AcceptWaveform(self.audio.read(4096,exception_on_overflow = False)): 
            self.before_listening.trigger()
            phrase = self.r.Result()
            
            phrase = str(json.loads(phrase)["text"])
            if phrase:
                if trigger:
                    self.after_listening.trigger(phrase)
            return phrase
        return None
    
    def force_listen(self):
        phrase = None
        while True:
            phrase = self.listen(False)
            if phrase != None & type(phrase) == str:
                break
        self.after_listening.trigger(phrase)
        return phrase

    def log(self, txt: str):
        self.logger.log(txt)
        
    def stop_ap(self):
        self.logger.exit()
        self.engine.stop()
        print("stopped engine")