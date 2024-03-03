import os
from datetime import datetime

class Logger():
    def __init__(self):
        if os.path.exists("log.txt"):
            os.remove("log.txt")
        self.file = open("log.txt", 'x')
        self.__now = datetime.now()
        self.__now = self.__now.strftime("%H:%M:%S")
        self.file.write(f"Log\n \nCreated: {self.__now}\n------------------\n")

    def log(self, log: str):
        self.file.write(f"\n  {log}")

    def exit(self):
        self.file.close()
