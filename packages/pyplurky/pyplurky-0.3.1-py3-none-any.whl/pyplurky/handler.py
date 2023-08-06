
"""
NOTE

Notice anti-flood-same-content
"""
from .error import PlurkyError
def handle_plurk(data,plurk_object,keyword,func):
    #print(data)
    content=data.data["content"]
    if keyword in content:
            func(plurk_object,data)

def handle_response(data,plurk_object,keyword,func):
    #print(data.data)
    content=data.response["content"]
    if keyword in content:
            func(plurk_object,data)
