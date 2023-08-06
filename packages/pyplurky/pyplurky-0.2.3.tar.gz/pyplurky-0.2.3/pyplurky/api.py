# coding=utf-8
################################################
# Make plurk api better to use for python user
# Produced by Dephilia
################################################
from . import util
from .plurk import PLURKOBJECT
from .user import USEROBJECT
from .error import PlurkyError
from .karma import KARMAOBJECT
from .profile import PROFILEOBJECT
from .realtime import REALTIMEOBJECT
from plurk_oauth import PlurkAPI
from urllib.parse import urlparse,urlencode,parse_qs
import requests
import sys
import json
import time
from datetime import datetime

class PLURK(PlurkAPI):

    def __init__(self,key=None, secret=None,
                 access_token=None, access_secret=None):

        super().__init__(key, secret,access_token, access_secret)

        self.users=USERS(self.callAPI,self.error)
        self.profiles=PROFILES(self.callAPI,self.error)
        self.realtime=REALTIME(self.callAPI,self.error)
        self.polling=POLLING(self.callAPI,self.error)
        self.timeline=TIMELINE(self.callAPI,self.error)
        self.responses=RESPONSES(self.callAPI,self.error)
        self.friendsfans=FRIENDSFANS(self.callAPI,self.error)
        self.alerts=ALERTS(self.callAPI,self.error)
        self.search=SEARCH(self.callAPI,self.error)
        self.emoticons=EMOTICONS(self.callAPI,self.error)
        self.blocks=BLOCKS(self.callAPI,self.error)
        self.cliques=CLIQUES(self.callAPI,self.error)
        self.oauth=OAUTH(self.callAPI,self.error)

        if self._authorized:
            try:
                self.oauth.checkToken()
            except:
                raise PlurkyError("Plurk API initial failed. Is network OK?")
            if not self.error()['code']==200:
                self._authorized=False
                raise PlurkyError("Access Token failed. Is the token out of time?")

        try:
            self.oauth.echo("key check")
        except:
            raise PlurkyError("Plurk API initial failed. Is network OK?")
        if self.error()['code']==200:
            self.__keyvalid=True
        else:
            self.__keyvalid=False
            raise PlurkyError("Consumer key failed. Please check it at Plurk App page.")

    def get_verifier_url(self):
        """Just return autho URL"""
        self._oauth.get_request_token()
        return self._oauth.get_verifier_url()

    def get_access_token(self, verifier):
        self._oauth.get_access_token(verifier.strip())
        self._authorized = True
        return {
            'key': self._oauth.oauth_token['oauth_token'],
            'secret': self._oauth.oauth_token['oauth_token_secret'],
        }

    @property
    def authorized(self):
        return self._authorized

    @property
    def keyvalid(self):
        return self.__keyvalid

class API():
    def __init__(self,callAPI,error):
        self.callAPI=callAPI
        self.error=error
        self._channel=None

class USERS(API):
    # --Users
    def me(self):
        """
        Return user data.
        """
        response = self.callAPI('/APP/Users/me')
        if self.error()['code']!=200:
            raise PlurkyError(self.error()['reason']+": "+self.error()['content']['error_text'])

        return USEROBJECT(response)

    def update(self,full_name=None,email=None,display_name=None,privacy=None,date_of_birth=None):
        """
        !!!only verified third party app can update user info
        full_name: Change full name.
        email: Change email.
        display_name: User's display name, can be empty and full unicode. Must be shorter than 15 characters.
        privacy: User's privacy settings. The option can be world (whole world can view the profile) or only_friends (only friends can view the profile).
        date_of_birth: Should be YYYY-MM-DD, example 1985-05-13.
        """
        options={}
        util.opt_para(full_name,"full_name",options)
        util.opt_para(email,"email",options)
        util.opt_para(display_name,"display_name",options)
        util.opt_para(privacy,"privacy",options)
        util.opt_para(date_of_birth,"date_of_birth",options)
        response = self.callAPI('/APP/Users/update',options=options)
        if self.error()['code']!=200:
            raise PlurkyError(self.error()['reason']+": "+self.error()['content']['error_text'])
        return response
    def updateAvatar(self,profile_image):
        files={
        "profile_image": profile_image
        }
        response = self.callAPI('/APP/Users/updateAvatar',files=files)
        if self.error()['code']!=200:
            raise PlurkyError(self.error()['reason']+": "+self.error()['content']['error_text'])
        return USEROBJECT(response)
    def getKarmaStats(self):
        response = self.callAPI('/APP/Users/getKarmaStats')
        if self.error()['code']!=200:
            raise PlurkyError(self.error()['reason']+": "+self.error()['content']['error_text'])
        return KARMAOBJECT(response)


class PROFILES(API):
    # --Profile
    def getOwnProfile(self):
        """
        Returns a JSON object with a lot of information that can be used to construct a user's own profile and timeline.
        """
        response = self.callAPI('/APP/Profile/getOwnProfile')
        if self.error()['code']!=200:
            raise PlurkyError(self.error()['reason']+": "+self.error()['content']['error_text'])
        return PROFILEOBJECT(response)

    def getPublicProfile(self,user_id):
        options={
            'user_id':user_id
        }
        response = self.callAPI('/APP/Profile/getPublicProfile',options=options)
        if self.error()['code']!=200:
            raise PlurkyError(self.error()['reason']+": "+self.error()['content']['error_text'])
        return PROFILEOBJECT(response)


class REALTIME(API):
    # --Real time notifications
    def getUserChannel(self):
        response = self.callAPI('/APP/Realtime/getUserChannel')
        if self.error()['code']!=200:
            raise PlurkyError(self.error()['reason']+": "+self.error()['content']['error_text'])

        channel_name = response['channel_name']
        pr=urlparse(response['comet_server'])
        server_loc = pr.netloc
        base_url="https://"+server_loc+"/comet"
        offset=parse_qs(pr.query)['offset'][0]

        if response:
            return base_url,channel_name,offset


    def listenNotification(self,base_url,channel,offset=None):
        options={
        'channel':channel,
        'js_callback':'CometChannel.scriptCallback'
        }
        if offset:options['offset']=offset
        url=base_url+"/%i/"%int(time.time())+'?'+urlencode(options)

        try:
            r = requests.get(url,timeout=60)

        except requests.RequestException as ex:
            print(ex, file=sys.stderr)
            sys.exit(1)
        except Exception as ex:
            print(ex, file=sys.stderr)
            sys.exit(1)

        d = json.loads(r.text[28:-2])
        return r.status_code, d, r.reason

    def ping(self):
        response = self.callAPI('/_comet/ping')
        print(self.error())

        return response

    def get(self,offset=0):
        """Directly get url from getUserChannel function and give paremeters to listenNotification"""


        if not self._channel:
            #response = self.callAPI('/APP/Realtime/getUserChannel')
            #print("Get channel:",response['comet_server'])
            #self._channel=response['comet_server']
            #r = requests.get(response['comet_server'])
            self._channel=self.getUserChannel()
            print("Get channel:",self._channel[0])
            print("Get comet name:",self._channel[1])
            status_code, d, reason=self.listenNotification(self._channel[0],self._channel[1],self._channel[2])
        else:
            #r = requests.get(self._channel)
            status_code, d, reason=self.listenNotification(self._channel[0],self._channel[1],offset=offset)
        if status_code!=200:
            raise PlurkyError(reason)

        return REALTIMEOBJECT(d)

    def reset_channel(self):
        self._channel=None

class POLLING(API):
    # --Polling
    def getPlurks(self,offset,limit=None,favorers_detail=None,limited_detail=None,
                    replurkers_detail=None):
        """
        offset: type<datetime>
        """
        if not isinstance(offset, datetime):
            raise TypeError('Offset must be an datetime.datetime object.')
        options={'offset':util.dt2pt(offset)}
        util.opt_para(limit,"limit",options)
        util.opt_para(favorers_detail,"favorers_detail",options)
        util.opt_para(limited_detail,"limited_detail",options)
        util.opt_para(replurkers_detail,"replurkers_detail",options)

        response = self.callAPI('/APP/Polling/getPlurks',options=options)
        if self.error()['code']!=200:
            raise PlurkyError(self.error()['reason']+": "+self.error()['content']['error_text'])

        result={
        'plurk_users':{},
        'plurks':[]
        }

        for u in response['plurk_users']:
            result['plurk_users'][str(u)]=USEROBJECT(response['plurk_users'][str(u)])
        for p in response['plurks']:
            result['plurks'].append(PLURKOBJECT(p))
        return result

    def getUnreadCount(self):
        response = self.callAPI('/APP/Polling/getUnreadCount')
        if response:
            return response
        else:
            return self.error()

class TIMELINE(API):

    # --Timeline
    def getPlurk(self,plurk_id,favorers_detail=None,limited_detail=None,replurkers_detail=None):
        options={
            'plurk_id':plurk_id
        }
        util.opt_para(favorers_detail,"favorers_detail",options)
        util.opt_para(limited_detail,"limited_detail",options)
        util.opt_para(replurkers_detail,"replurkers_detail",options)

        response = self.callAPI('/APP/Timeline/getPlurk',options=options)

        result={
        "user":USEROBJECT(response['user']),
        "plurk":PLURKOBJECT(response['plurk'])
        }

        if response:
            return result
        else:
            return self.error()

    def getPlurk36(self,plurk_id,favorers_detail=None,limited_detail=None,replurkers_detail=None):
        options={
            'plurk_id':util.decode36(plurk_id)
        }
        util.opt_para(favorers_detail,"favorers_detail",options)
        util.opt_para(limited_detail,"limited_detail",options)
        util.opt_para(replurkers_detail,"replurkers_detail",options)

        response = self.callAPI('/APP/Timeline/getPlurk',options=options)

        if response:
            return {
            "user":USEROBJECT(response['user']),
            "plurk":PLURKOBJECT(response['plurk'])
            }
        else:
            return self.error()

    def getPlurks(self,offset=None,limit=None,filter=None,favorers_detail=None,limited_detail=None,
                    replurkers_detail=None):
        """
        response return 'plurk_users', 'plurks'
        plurk_users<dict>
        plurks<list>
        """
        options={}
        if offset:options['offset']=util.dt2pt(offset)
        util.opt_para(limit,"limit",options)
        util.opt_para(filter,"filter",options)
        util.opt_para(favorers_detail,"favorers_detail",options)
        util.opt_para(limited_detail,"limited_detail",options)
        util.opt_para(replurkers_detail,"replurkers_detail",options)
        response = self.callAPI('/APP/Timeline/getPlurks',options=options)
        if response:
            for p in response['plurks']:
                yield {
                "user":USEROBJECT(response['plurk_users'][str(p['owner_id'])]),
                "plurk":PLURKOBJECT(p)
                }




    def getUnreadPlurks(self,offset=None,limit=None,filter=None,favorers_detail=None,limited_detail=None,
                    replurkers_detail=None):
        options={}
        if offset:options['offset']=util.dt2pt(offset)
        util.opt_para(limit,"limit",options)
        util.opt_para(filter,"filter",options)
        util.opt_para(favorers_detail,"favorers_detail",options)
        util.opt_para(limited_detail,"limited_detail",options)
        util.opt_para(replurkers_detail,"replurkers_detail",options)
        response = self.callAPI('/APP/Timeline/getUnreadPlurks',options=options)
        if response:
            for p in response['plurks']:
                yield {
                "user":USEROBJECT(response['plurk_users'][str(p['owner_id'])]),
                "plurk":PLURKOBJECT(p)
                }


    def getPublicPlurks(self,user_id,offset=None,limit=None,filter=None,favorers_detail=None,limited_detail=None,
                    replurkers_detail=None):
        options={
            'user_id':user_id
        }
        if offset:options['offset']=util.dt2pt(offset)
        util.opt_para(limit,"limit",options)
        util.opt_para(favorers_detail,"favorers_detail",options)
        util.opt_para(limited_detail,"limited_detail",options)
        util.opt_para(replurkers_detail,"replurkers_detail",options)
        response = self.callAPI('/APP/Timeline/getPublicPlurks',options=options)
        if response:
            for p in response['plurks']:
                yield {
                "user":USEROBJECT(response['plurk_users'][str(p['owner_id'])]),
                "plurk":PLURKOBJECT(p)
                }

    def plurkAdd(self,content,qualifier=':',limited_to=None,no_comments=None,lang=None):
        options={
            'content':content,
            'qualifier':qualifier
        }
        util.opt_para(limited_to,"limited_to",options)
        util.opt_para(no_comments,"no_comments",options)
        util.opt_para(lang,"lang",options)
        response = self.callAPI('/APP/Timeline/plurkAdd',options=options)
        if response:
            return PLURKOBJECT(response)

    def plurkDelete(self,plurk_id):
        """
        timeline.plurkDelete
        [Input]
        <Necessary>
        plurk_id: Should be base10 integer.

        <Optional>
        None

        [Output]
        A boolen.
        """
        options={
            'plurk_id':plurk_id
        }

        response = self.callAPI('/APP/Timeline/plurkDelete',options=options)
        if response:
            s=response['success_text']=='ok'
            if s:
                return True
            else:
                return False


    def plurkEdit(self,plurk_id,content):
        options={
            'plurk_id':plurk_id,
            'content':content,
        }

        response = self.callAPI('/APP/Timeline/plurkEdit',options=options)
        if response:
            return PLURKOBJECT(response)
    def toggleComments(self,plurk_id,no_comments):
        options={
            'plurk_id':plurk_id,
            'no_comments':no_comments,
        }

        response = self.callAPI('/APP/Timeline/toggleComments',options=options)
        if response:
            return response["no_comments"]


    def mutePlurks(self,ids):
        if not isinstance(ids, list):
            raise TypeError('ids should be a list.')
        options={
            'ids':ids,
        }
        response = self.callAPI('/APP/Timeline/mutePlurks',options=options)
        if response:
            s=response['success_text']=='ok'
            if s:
                return True
            else:
                return False

    def mutePlurk(self,id):
        options={
            'ids':[id],
        }
        response = self.callAPI('/APP/Timeline/mutePlurks',options=options)
        if response:
            s=response['success_text']=='ok'
            if s:
                return True
            else:
                return False

    def unmutePlurks(self,ids):
        if not isinstance(ids, list):
            raise TypeError('ids should be a list.')
        options={
            'ids':ids,
        }
        response = self.callAPI('/APP/Timeline/unmutePlurks',options=options)
        if response:
            s=response['success_text']=='ok'
            if s:
                return True
            else:
                return False

    def unmutePlurk(self,id):
        options={
            'ids':[id],
        }
        response = self.callAPI('/APP/Timeline/unmutePlurks',options=options)
        if response:
            s=response['success_text']=='ok'
            if s:
                return True
            else:
                return False

    def favoritePlurks(self,ids):
        if not isinstance(ids, list):
            raise TypeError('ids should be a list.')
        options={
            'ids':ids,
        }
        response = self.callAPI('/APP/Timeline/favoritePlurks',options=options)
        if response:
            s=response['success_text']=='ok'
            if s:
                return True
            else:
                return False

    def favoritePlurk(self,id):
        options={
            'ids':[id],
        }
        response = self.callAPI('/APP/Timeline/favoritePlurks',options=options)
        if response:
            s=response['success_text']=='ok'
            if s:
                return True
            else:
                return False

    def unfavoritePlurks(self,ids):
        if not isinstance(ids, list):
            raise TypeError('ids should be a list.')
        options={
            'ids':ids,
        }
        response = self.callAPI('/APP/Timeline/unfavoritePlurks',options=options)
        if response:
            s=response['success_text']=='ok'
            if s:
                return True
            else:
                return False
    def unfavoritePlurk(self,id):
        options={
            'ids':[id],
        }
        response = self.callAPI('/APP/Timeline/unfavoritePlurks',options=options)
        if response:
            s=response['success_text']=='ok'
            if s:
                return True
            else:
                return False
    def replurk(self,ids):
        if not isinstance(ids, list):
            raise TypeError('ids should be a list.')
        options={
            'ids':ids,
        }
        response = self.callAPI('/APP/Timeline/replurk',options=options)
        if response:
            return response
        else:
            return self.error()

    def replurk_one(self,id):
        options={
            'ids':[id],
        }
        response = self.callAPI('/APP/Timeline/replurk',options=options)
        if response:
            return response
        else:
            return self.error()
    def unreplurk(self,ids):
        if not isinstance(ids, list):
            raise TypeError('ids should be a list.')
        options={
            'ids':ids,
        }
        response = self.callAPI('/APP/Timeline/unreplurk',options=options)
        if response:
            return response
        else:
            return self.error()

    def unreplurk_one(self,id):
        options={
            'ids':[id],
        }
        response = self.callAPI('/APP/Timeline/unreplurk',options=options)
        if response:
            return response
        else:
            return self.error()

    def markAsRead(self,ids,note_position=None):
        if not isinstance(ids, list):
            raise TypeError('ids should be a list.')
        options={'ids':ids}
        util.opt_para(note_position,"note_position",options)

        response = self.callAPI('/APP/Timeline/markAsRead',options=options)
        if response:
            return response
        else:
            return self.error()

    def markAsRead_one(self,id,note_position=None):
        """Accept one id version"""
        options={'ids':[str(id)]}
        util.opt_para(note_position,"note_position",options)

        response = self.callAPI('/APP/Timeline/markAsRead',options=options)
        if response:
            return response
        else:
            return self.error()

    def uploadPicture(self,image):
        files={
        "image": image
        }
        response = self.callAPI('/APP/Users/uploadPicture',files=files)
        if response:
            return response
        else:
            return self.error()

    def reportAbuse(self,plurk_id,categoty):
        options={
        'plurk_id':plurk_id,
        'categoty':categoty
        }

        response = self.callAPI('/APP/Timeline/reportAbuse',options=options)
        if response:
            return response
        else:
            return self.error()

class RESPONSES(API):
    # --Responses
    def get(self,plurk_id,from_response=None,minimal_data=None,count=None):
        options={
            'plurk_id':plurk_id
        }

        util.opt_para(from_response,"from_response",options)
        util.opt_para(minimal_data,"minimal_data",options)
        util.opt_para(count,"count",options)

        response = self.callAPI('/APP/Responses/get',options=options)
        if self.error()['code']!=200:
            raise PlurkyError(self.error()['reason']+": "+self.error()['content']['error_text'])
        return response
    def responseAdd(self,plurk_id,content,qualifier=':'):
        """
        Note: Repeating send something will cause failure
        """
        options={
            'plurk_id':plurk_id,
            'content':content,
            'qualifier':qualifier
        }

        response = self.callAPI('/APP/Responses/responseAdd',options=options)
        if self.error()['code']!=200:
            raise PlurkyError(self.error()['reason']+": "+self.error()['content']['error_text'])
        return response

    def responseDelete(self,response_id,plurk_id):
        options={
            'plurk_id':plurk_id,
            'response_id':response_id,
        }

        response = self.callAPI('/APP/Responses/responseDelete',options=options)
        if self.error()['code']!=200:
            raise PlurkyError(self.error()['reason']+": "+self.error()['content']['error_text'])
        return response

class FRIENDSFANS(API):
    # --Friends and fans
    def getFriendsByOffset(self,user_id,offset=None,limit=None):
        options={
            'user_id':user_id
        }
        util.opt_para(offset,"offset",options)
        util.opt_para(limit,"limit",options)

        response = self.callAPI('/APP/FriendsFans/getFriendsByOffset',options=options)
        if response:
            return response
        else:
            return self.error()

    def getFansByOffset(self,user_id,offset=None,limit=None):
        options={
            'user_id':user_id
        }
        util.opt_para(offset,"offset",options)
        util.opt_para(limit,"limit",options)

        response = self.callAPI('/APP/FriendsFans/getFansByOffset',options=options)
        if response:
            return response
        else:
            return self.error()

    def getFollowingByOffset(self,offset=None,limit=None):
        util.opt_para(offset,"offset",options)
        util.opt_para(limit,"limit",options)

        response = self.callAPI('/APP/FriendsFans/getFollowingByOffset',options=options)
        if response:
            return response
        else:
            return self.error()

    def becomeFriend(self,friend_id):
        options={
            'friend_id':friend_id
        }
        response = self.callAPI('/APP/FriendsFans/becomeFriend',options=options)
        if response:
            return response
        else:
            return self.error()


    def removeAsFriend(self,friend_id):
        options={
            'friend_id':friend_id
        }
        response = self.callAPI('/APP/FriendsFans/removeAsFriend',options=options)
        if response:
            return response
        else:
            return self.error()
    def becomeFan(self,fan_id):
        options={
            'fan_id':fan_id
        }
        response = self.callAPI('/APP/FriendsFans/becomeFan',options=options)
        if response:
            return response
        else:
            return self.error()
    def setFollowing(self,fan_id,follow):
        options={
            'fan_id':fan_id,
            'follow':follow
        }
        response = self.callAPI('/APP/FriendsFans/setFollowing',options=options)
        if response:
            return response
        else:
            return self.error()
    def getCompletion(self):
        response = self.callAPI('/APP/FriendsFans/getCompletion')
        if response:
            return response
        else:
            return self.error()

class ALERTS(API):
    # --Alerts
    def getActive(self):
        response = self.callAPI('/APP/Alerts/getActive')
        if response:
            return response
        else:
            return self.error()
    def getHistory(self):
        response = self.callAPI('/APP/Alerts/getHistory')
        if response:
            return response
        else:
            return self.error()
    def addAsFan(self,user_id):
        options={
            'user_id':user_id
        }
        response = self.callAPI('/APP/Alerts/addAsFan',options=options)
        if response:
            return response
        else:
            return self.error()
    def addAllAsFan(self):
        response = self.callAPI('/APP/Alerts/addAllAsFan')
        if response:
            return response
        else:
            return self.error()
    def addAllAsFriends(self):
        response = self.callAPI('/APP/Alerts/addAllAsFriends')
        if response:
            return response
        else:
            return self.error()
    def addAsFriend(self,user_id):
        options={
            'user_id':user_id
        }
        response = self.callAPI('/APP/Alerts/addAsFriend',options=options)
        if response:
            return response
        else:
            return self.error()
    def denyFriendship(self,user_id):
        options={
            'user_id':user_id
        }
        response = self.callAPI('/APP/Alerts/denyFriendship',options=options)
        if response:
            return response
        else:
            return self.error()
    def removeNotification(self,user_id):
        options={
            'user_id':user_id
        }
        response = self.callAPI('/APP/Alerts/removeNotification',options=options)
        if response:
            return response
        else:
            return self.error()

class SEARCH(API):
    # --Search
    def PlurkSearch(self,query,offset=None):
        options={
            'query':query,
        }
        util.opt_para(offset,"offset",options)
        response = self.callAPI('/APP/PlurkSearch/search',options=options)
        if response:
            return response
        else:
            return self.error()
    def UserSearch(self,query,offset=None):
        options={
            'query':query,
        }
        util.opt_para(offset,"offset",options)
        response = self.callAPI('/APP/UserSearch/search',options=options)
        if response:
            return response
        else:
            return self.error()

class EMOTICONS(API):
    # --Emoticons
    def get(self):
        response = self.callAPI('/APP/Emoticons/get')
        if response:
            return response
        else:
            return self.error()

    def __str__(self):
        response = self.callAPI('/APP/Emoticons/get')
        text="""<pyplurky emoticons object>
*custom   :{}
*recruited:{}
*karma    :{}
*recuited :{}""".format(len(response['custom']),
                   len(response['recruited']),
                   len(response['karma']),
                   len(response['recuited']))
        return text


class BLOCKS(API):
    # --Blocks
    def get(self,offset=None):
        options={}
        util.opt_para(offset,"offset",options)
        response = self.callAPI('/APP/Blocks/get',options=options)
        if self.error()['code']!=200:
            raise PlurkyError(self.error()['reason']+": "+self.error()['content']['error_text'])
        response['users']=[USEROBJECT(i) for i in response['users']]
        return response
    def block(self,user_id):
        options={
            'user_id':user_id,
        }
        response = self.callAPI('/APP/Blocks/block',options=options)
        if self.error()['code']!=200:
            raise PlurkyError(self.error()['reason']+": "+self.error()['content']['error_text'])
        if response['success_text']=='ok':
            return True
        else:
            return False

    def unblock(self,user_id):
        options={
            'user_id':user_id,
        }
        response = self.callAPI('/APP/Blocks/unblock',options=options)
        if self.error()['code']!=200:
            raise PlurkyError(self.error()['reason']+": "+self.error()['content']['error_text'])
        if response['success_text']=='ok':
            return True
        else:
            return False

class CLIQUES(API):
    # --Cliques
    def getCliques(self):
        response = self.callAPI('/APP/Cliques/getCliques')
        if self.error()['code']!=200:
            raise PlurkyError(self.error()['reason']+": "+self.error()['content']['error_text'])
        return response
    def getClique(self,clique_name):
        options={
        'clique_name':clique_name
        }
        response = self.callAPI('/APP/Cliques/getClique',options=options)
        if self.error()['code']!=200:
            raise PlurkyError(self.error()['reason']+": "+self.error()['content']['error_text'])
        return [USEROBJECT(i) for i in response]
    def createClique(self,clique_name):
        options={
        'clique_name':clique_name
        }
        response = self.callAPI('/APP/Cliques/createClique',options=options)
        if self.error()['code']!=200:
            raise PlurkyError(self.error()['reason']+": "+self.error()['content']['error_text'])
        if response['success_text']=='ok':
            return True
        else:
            return False
    def renameClique(self,clique_name,new_name):
        options={
        'clique_name':clique_name,
        'new_name':new_name
        }
        response = self.callAPI('/APP/Cliques/renameClique',options=options)
        if self.error()['code']!=200:
            raise PlurkyError(self.error()['reason']+": "+self.error()['content']['error_text'])
        if response['success_text']=='ok':
            return True
        else:
            return False
    def add(self,clique_name,user_id):
        options={
        'clique_name':clique_name,
        'user_id':user_id
        }
        response = self.callAPI('/APP/Cliques/add',options=options)
        if self.error()['code']!=200:
            raise PlurkyError(self.error()['reason']+": "+self.error()['content']['error_text'])
        if response['success_text']=='ok':
            return True
        else:
            return False
    def remove(self,clique_name,user_id):
        options={
        'clique_name':clique_name,
        'user_id':user_id
        }
        response = self.callAPI('/APP/Cliques/remove',options=options)
        if self.error()['code']!=200:
            raise PlurkyError(self.error()['reason']+": "+self.error()['content']['error_text'])
        if response['success_text']=='ok':
            return True
        else:
            return False
class OAUTH(API):
    # --OAuth Utilities
    def checkToken(self):
        response = self.callAPI('/APP/checkToken')
        if self.error()['code']!=200:
            raise PlurkyError(self.error()['reason']+": "+self.error()['content']['error_text'])
        return response
    def expireToken(self):
        response = self.callAPI('/APP/expireToken')
        if self.error()['code']!=200:
            raise PlurkyError(self.error()['reason']+": "+self.error()['content']['error_text'])
        return response

    def checkTime(self):
        response = self.callAPI('/APP/checkTime')
        if self.error()['code']!=200:
            raise PlurkyError(self.error()['reason']+": "+self.error()['content']['error_text'])
        return response
    def echo(self,data):
        response = self.callAPI('/APP/echo',options={'data':data})
        if self.error()['code']!=200:
            raise PlurkyError(self.error()['reason']+": "+self.error()['content']['error_text'])
        return response
