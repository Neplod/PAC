from typing import Protocol
from ap import AP

class Skill(Protocol):

    def commands(self, command:str):
        """ Return a list of commands that this skill can handle """
        pass
    
    def handle_command(self, command:str, ap:AP):
        """ Handle a command """
        pass

def initialize():
    pass