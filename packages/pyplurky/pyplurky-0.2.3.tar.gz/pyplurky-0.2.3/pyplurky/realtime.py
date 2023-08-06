from .user import USEROBJECT
from .plurk import PLURKOBJECT
from .util import encode36
class REALTIMEOBJECT():
    def __init__(self,data):
        self.__has_data=False
        if 'data' in data:
            self.__data=[REALTIME_DATA_OBJECT(i) for i in data['data']]
            self.__has_data=True
        self.__new_offset=data['new_offset']

    def __str__(self):
        text="<pyplurky realtime object | NewOffset: {}>".format(self.__new_offset)
        if self.__has_data:
            for i in self.__data:
                text+="\n |-"+str(i)
        return text

    def __len__(self):
        return len(self.__data)

    def __getitem__(self,idx):
        return self.__data[idx]

    @property
    def data(self):
        if self.__has_data:
            return self.__data
        else:
            return []

    @property
    def new_offset(self):
        return self.__new_offset

    @property
    def has_data(self):
        return self.__has_data

class REALTIME_DATA_OBJECT():
    def __init__(self,data):
        self.__data=data
        self.__type=data['type']

        if self.__type=="new_response":
            self.__plurk_id=data['plurk_id']
            self.__response_count=data['response_count']
            self.__response=data['response']
            self.__user=[USEROBJECT(data['user'][i]) for i in data['user']]
            self.__user_list=[*data['user']]
            self.__plurk=PLURKOBJECT(data['plurk'])

        elif self.__type=="new_plurk":
            self.__plurk_id=data['plurk_id']
            self.__response_count=data['response_count']
            self.__plurk=PLURKOBJECT(data)

        elif self.__type=="update_notification":
            pass


    def __str__(self):
        if self.__type=="update_notification":
            text="<pyplurky realtime data object | Type: {}>".format(self.__type)
        else:
            text="<pyplurky realtime data object | Type: {}, ID: {} - {}>".format(self.__type,self.__plurk_id,encode36(self.__plurk_id))
        return text

    @property
    def data(self):
        return self.__data

    @property
    def type(self):
        return self.__type

    @property
    def plurk_id(self):
        if self.__type=="new_plurk" or self.__type=="new_response":
            return self.__plurk_id
        else:
            return None

    @property
    def plurk(self):
        if self.__type=="new_plurk" or self.__type=="new_response":
            return self.__plurk
        else:
            return None


    @property
    def response(self):
        if self.__type=="new_response":
            return self.__response
        else:
            return None
