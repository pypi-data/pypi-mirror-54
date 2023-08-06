from .util import encode36
class PLURKOBJECT():
    def __init__(self,data):
        self.__data=data
        self.__plurk_id=data['plurk_id']
        self.__user_id=data['user_id']
        self.__content=data['content']

        self.__index=[*data]


    def __str__(self):
        text="<pyplurky plurk object | ID: {} - {}>".format(self.__plurk_id,encode36(self.__plurk_id))
        return text

    def __getitem__(self,idx):
        return self.__data[idx]

    @property
    def data(self):
        return self.__data

    @property
    def index(self):
        return self.__index
    @property
    def plurk_id(self):
        return self.__plurk_id

    @property
    def user_id(self):
        return self.__user_id

    @property
    def content(self):
        return self.__content
