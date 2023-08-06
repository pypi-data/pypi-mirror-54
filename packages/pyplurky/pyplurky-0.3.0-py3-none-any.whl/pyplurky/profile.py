from .user import USEROBJECT
from .plurk import PLURKOBJECT
class PROFILEOBJECT():
    def __init__(self,data):
        self.__data=data
        self.__user_info=USEROBJECT(data['user_info'])
        self.__plurks=iter([PLURKOBJECT(i) for i in data['plurks']])
        self.__index=[*data]

    def __str__(self):
        text="<pyplurky profile object | Name: {}, ID: {}>".format(self.__user_info.display_name,self.__user_info.id)
        return text

    def __getitem__(self,idx):
        return self.__data[idx]

    @property
    def user_info(self):
        return self.__user_info

    @property
    def plurks(self):
        return self.__plurks

    @property
    def data(self):
        return self.__data

    @property
    def index(self):
        return self.__index

    def showPlurks(self):
        for p in self.__plurks:
            print("="*40)
            print(p)
            print(p.content)
            print("\n")
        return True
