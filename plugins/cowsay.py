from dataclasses import dataclass
from ap import AP
import plugins.plugin_factory

@dataclass
class Cowsay_plugin:
    name = 'cowsay'

    def cowsay(self, message):
        print(f"moo {message}")

    def register(self, ap:AP):
        self.ap = ap
        print("registering cowsay plugin - after speaking")
        self.ap.after_speaking.register(self.cowsay)   
        return self

def initialize():
    # register with Factory or plugin?
    plugins.plugin_factory.register('cowsay_plugin', Cowsay_plugin)
    
    print("Cow Say Plugin initialized")