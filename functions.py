import importlib
import sys
import subprocess
import time

class Functions():

    def __init__(self):
        pass

    def import_module(self, module:str):
        return self._tryimport(module)
    
    def import_lib(self, lib:str):
        return self._tryimport(lib)
    
    def _tryimport(self, m:str, _maxforce: int = 30, _sleep: int = 100):
        try:
            return importlib.import_module(m)
        except:
            try:
                i = self.__installpipmodule(m)
                if i:
                    for i in range(_maxforce):
                        _fi = self.__forceimport(m)
                        if _fi:
                            return _fi
                        time.sleep(_sleep/1000)
                    pass
                else:
                    pass
            except:
                pass
    
    def __installpipmodule(self, m:str) -> bool:
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', m])
            return True
        except:
            return False
    
    def __forceimport(self, m: str):
        try:
            return importlib.import_module(m)
        except:
            return None

class PrivateFunctions():
    def install_lib(lib: str):
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', lib])
            return True
        except:
            return False