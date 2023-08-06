class USEROBJECT():
    def __init__(self,data):
        self.__data=data
        self.__display_name=data['display_name']
        self.__id=data['id']
        self.__nick_name=data['nick_name']
        self.__index=[*data]

    def __str__(self):
        text="<pyplurky user object | Name: {}, ID: {}>".format(self.__display_name,self.__id)
        return text

    def __getitem__(self,idx):
        return self.__data[idx]

    @property
    def display_name(self):
        return self.__display_name


    @property
    def id(self):
        return self.__id


    @property
    def data(self):
        return self.__data

    @property
    def nick_name(self):
        return self.__nick_name

    @property
    def index(self):
        return self.__index
