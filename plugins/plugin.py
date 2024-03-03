from typing import Protocol
from ap import AP

class Plugin(Protocol):
    
    def handle_command(self, command:str, ap:AP):
        """ Handle a command """
        pass

    def register(self):
        ...