from ap import AP
from skills import factory, loader
from plugins import plugin_loader, plugin_factory
import json
from eventhook import Event_hook

class MainAP():

    def __init__(self):
        self.ap = AP()

        self.ap.start = Event_hook()
        self.ap.stop = Event_hook()

        self.command = ""

        with open("./skills/skills.json") as f:
            data = json.load(f)

            loader.load_skills(data["lib"])

        self.skills = [factory.create(item) for item in data["skills"]]
        print(f'skills: {self.skills}')

        with open("./plugins/plugins.json") as f:
            plugin_data = json.load(f)
            print(f'plugins: {plugin_data["plugins"]}')
            plugin_loader.load_plugins(plugin_data["plugins"])

        self.plugins = [plugin_factory.create(item) for item in plugin_data["items"]]

        for item in self.plugins:
            item.register(self.ap)

    def main(self):
        self.ap.start.trigger()
        self.ap.say("Hola")
        while True and self.command not in ["adiós", 'hasta luego', 'quitar', 'salir','hasta otra', 'la salida', 'salida']:
            self.command = ""
            self.command = self.ap.listen()
            if self.command:
                self.command = self.command.lower()
                print(f'command heard: {self.command}') 
                for skill in self.skills:
                    if self.command in skill.commands(self.command):
                        try:
                            skill.handle_command(self.command, self.ap)
                        except Exception as e:
                            print(f"Error: {e}")
            if self.ap.engine.isBusy() == False:
                self.ap.engine.endLoop()

        self.ap.say("Adiós!")

        print('telling triggers to stop')
        self.ap.stop.trigger()
        print('telling ai to stop')
        self.ap.stop_ap()
        print('deleting ai')
        del(self.ap)
        print('done')
