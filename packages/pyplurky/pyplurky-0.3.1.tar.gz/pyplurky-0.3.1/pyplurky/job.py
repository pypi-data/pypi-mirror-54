import schedule
import threading



class jobs():
    def __init__(self):
        self.__s=schedule
        self.__state=1
        self.__history=[]
        #self.__s.every(2).seconds.do(hey)

    def __str__(self):
        pass

    @property
    def job(self):
        return self.__s

    def run(self):
        while self.__state:
            self.__s.run_pending()

    def stop(self):
        self.__state=0

    def idle(self):
        threading.Thread(target=self.run).start()
