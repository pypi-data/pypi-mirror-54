import schedule
import threading

def hey():
    print("hey")

class jobs():
    def __init__(self):
        self.__s=schedule
        self.__state=1
        #self.__s.every(2).seconds.do(hey)

    def run(self):
        while self.__state:
            self.__s.run_pending()

    def stop(self):
        self.__state=0

    def idle(self):
        threading.Thread(target=self.run).start()
