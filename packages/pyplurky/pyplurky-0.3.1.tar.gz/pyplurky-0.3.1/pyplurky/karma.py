from .util import timestamp2datetime
class KARMAOBJECT():
    def __init__(self,data):
        self.__data=data
        self.__karma_fall_reason=data['karma_fall_reason']
        self.__current_karma=data['current_karma']
        self.__karma_graph=data['karma_graph']
        self.__karma_trend=data['karma_trend']


    def __str__(self):
        text="<pyplurky karma object | Now: {}>".format(self.__current_karma)
        return text

    def __getitem__(self,idx):
        return self.__data[idx]

    @property
    def now(self):
        return self.__current_karma

    @property
    def trend(self):
        for t in self.__karma_trend:
            x=t.split("-")
            yield (timestamp2datetime(int(x[0])),float(x[1]))
