#0.0.1
from ap import AP
from skills import factory

class Time_skill ():

    def commands(self, command:str):
        return ['dime la hora', 'qué hora es', 'hora']

    def handle_command(self, command:str, pa:AP):
        Functions = functions = pa.functions
        datetime = functions.import_lib('datetime')
        now = datetime.datetime.now()
        t_string = now.strftime("%H:%M")
        pa.say(f"Son las {t_string.replace(':', ' y ')}")
        
        

def initialize():
    factory.register("time_skill", Time_skill)
        