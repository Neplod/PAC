import codecs
import importlib
from pathlib import Path
import os
import json

class Skill():

    def __init__(self, name: str, commands: list[str] = [], code: str = """""", _ispy: bool| None = None):
        self.__name: str = name.lower().replace(' ','_').replace('.',',')
        self.__commands: list[str] = commands
        self.__code: str = code
        self.__old:str = self.__name
        if _ispy != None:
            self.__py: bool = _ispy
        else:
            self.__py: bool = False
    
    def __new__(cls, name:str, commands: list[str] = [], code: str = """""", _ispy: bool|None = None):
        instance = super().__new__(cls)
        return instance
    
    def __str__(self):
        return f"""{self.__name.capitalize()}: \n   Commands: {", ".join(self.__commands)} \n   Code:{self.__code}"""

    # Properties
    
    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__old = self.__name
        self.__name = value.lower().replace(' ','_').replace('.',',')
    
    @property
    def commands(self) -> list[str]:
        return self.__commands

    @commands.setter
    def commands(self, value: list[str]):
        self.__commands = value
    
    def commands_append(self, value: str):
        self.__commands.append(value)
    def commands_extend(self, value: str):
        self.__commands.extend(value)
    def commands_pop(self, value: int):
        self.__commands.pop(value)
    def commands_remove(self):
        self.__commands.append()

    @property
    def code(self) -> str:
        return self.__code

    @code.setter
    def code(self, value: str):
        self.__code = value

    # Funcs

    def toPy(self, only_txt: bool = False):
        try:
            os.remove(f"skills/skillset/{self.__name}.py")
        except:
            pass
        try:
            os.remove(f"skills/skillset/{self.__name}.txt")
        except:
            pass

        file = codecs.open(f'skills/skillset/{self.__name}.txt', 'x', 'UTF8')

        self.__fixcode()

        skill = f"""#0.0.1
from ap import AP
from skills import factory

class {self.__name.capitalize()}_skill ():

    def commands(self, command:str):
        return {self.__commands}

    def handle_command(self, command:str, pa:AP):
        Functions = functions = pa.functions
        {self.__code}

def initialize():
    factory.register("{self.__name}_skill", {self.__name.capitalize()}_skill)
        """
    
        file.write(skill)
        file.close()

        if not only_txt:
            path = Path(f"skills/skillset/{self.__name}.txt")

            newpath = path.with_suffix('.py')

            self._editinjson(self.__old)

            path.rename(newpath)
            self.__py = True
        else:
            self.__py = False

    def deletePy(self):
        try:
            os.remove(f"skills/skillset/{self.__name}.py")
            self._unregisterinjson()
            self.__py = False
        except:
            pass
    
    def delete(self):
        self.deletePy()
        try:
            os.remove(f"skills/skillset/{self.__name}.txt")
        except:
            pass
    
    def _registerinjson(self):
        with codecs.open('./skills/skills.json', 'r', 'UTF8') as file:
            data = json.load(file)
            data["lib"].append(f'skills.skillset.{self.__name}')
            data["skills"].append({"name":f"{self.__name}_skill"})
        self.__rewrite(data, './skills/skills.json')
    
    def _editinjson(self, old: str):
        with codecs.open('./skills/skills.json', 'r', 'UTF8') as file:
            data = json.load(file)
            if f'skills.skillset.{old}' in data['lib']:
                data["lib"][data["lib"].index(f'skills.skillset.{old}')] = f'skills.skillset.{self.__name}'
                data["skills"][data["skills"].index({"name":f"{old}_skill"})] = {"name":f"{self.__name}_skill"}
                file.close()
                self.__rewrite(data, './skills/skills.json')
            else:
                file.close()
                self._registerinjson()
    
    def _unregisterinjson(self):
        with codecs.open('./skills/skills.json', 'r', 'UTF8') as file:
            data = json.load(file)
            data["lib"].pop(data['lib'].index(f'skills.skillset.{self.__name}'))
            data["skills"].pop(data['skills'].index({"name":f"{self.__name}_skill"}))
        self.__rewrite(data, './skills/skills.json')
            
    def __rewrite(self, data: any, path:str):
        os.remove(path)
        newfile = open(path, 'x')
        newfile.write(str(data).replace("'",'"'))
        newfile.close()
    
    def __fixcode(self) -> str:
        sc: list[str] = self.__code.split('\n')
        fix: str = ""
        for i,e in enumerate(sc):
            if i != 0:
                sc[i] = f"""\n        {e}"""
            fix = fix + sc[i]
        self.__code = fix

def get_all_skills() -> list[Skill]:
    funcs: list[Skill] = []
    funcspath = os.listdir('skills/skillset/')
    for p in funcspath:
        if p != '__pycache_:__':
            with codecs.open(f'./skills/skillset/{p}', encoding='UTF8') as _file:
                _lines = _file.readlines()

            _name = _lines[-2].split('"')[1][:-6]
            _commands = eval(_lines[7].replace('        return ', '').replace('\n', ''))
            _code = _lines [11:-5]

            for i,l in enumerate(_code):
                _code[i] = l.replace('        ','')
                if i == len(_code)-1:
                    _code[i] = _code[i].replace('\n', '')
            _code = ''.join(_code)

            funcs.append(Skill(_name, _commands, f"""{_code}""", _ispy = True if p.endswith('.py') else False))
    return funcs