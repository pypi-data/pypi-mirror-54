from .api import PLURK
from .handler import handle_plurk,handle_response
from .job import jobs
import time
import json
import sys
from datetime import datetime,timedelta
from functools import wraps
import asyncio
try:
    import readline
except ImportError:
    print("readline module import failed. This may cause some input problem.")

class pyplurky():
    def __init__(self,mode,key="API.keys",debug=False):
        self.__mode=mode # "REPL","BOT"
        self.__key=key
        self.plurk = PLURK.fromfile(key)
        self.__error=""
        self.status = 0
        self.__offset=0
        self.__response_handler={}
        self.__plurk_handler={}
        self.__repeat_handler=[]
        self.__debug=debug
        self.__job=jobs()

        if not self.plurk.keyvalid:
            self.status = 2

    # def addPlurkHandler(self,keyword,replyword,*args):
    #     self.__plurk_handler[keyword]=replyword
    #
    # def addResponseHandler(self,keyword,replyword,*args):
    #     self.__response_handler[keyword]=replyword

    def addPlurkHandler(self,keyword,func,*args):
        self.__plurk_handler[keyword]=func
        return True

    def addResponseHandler(self,keyword,func,*args):
        self.__response_handler[keyword]=func
        return True


    def addRepeatHandler(self,func,*args):
        self.__repeat_handler.append(func)
        return True

    def JobStart(self):
        self.__job.idle()

    def addJob(self):
        pass


    def init_main(self):
        #print("Pass in init.")
        if not self.plurk.is_authorized():
            try:
                print("打開網址以取得驗證碼:\n",self.plurk.get_verifier_url())
                akey=self.plurk.get_access_token(input("驗證碼: "))
                with open(self.__key, 'r') as f:
                    d = json.load(f)
                d["ACCESS_TOKEN"]=akey['key']
                d["ACCESS_TOKEN_SECRET"]=akey['secret']
                with open(self.__key, 'w') as f:
                    json.dump(d, f, indent=4)

                if self.plurk.keyvalid and self.plurk.authorized:
                    m=self.plurk.users.me()
                    self.plurk.timeline.getPlurks(0,limit=1)
                    print("\033[0;33m<Access User:{} | ID:{} | Nickname:{}>\033[0m".format(m.display_name,m.id,m.nick_name))

                print("<Initial Complete>")
                return 1
            except KeyboardInterrupt:
                return 2
            except:
                return 99
        else:
            if self.plurk.keyvalid and self.plurk.authorized:
                m=self.plurk.users.me()
                self.plurk.timeline.getPlurks(0,limit=1)
                print("\033[0;33m<Access User:{} | ID:{} | Nickname:{}>\033[0m".format(m.display_name,m.id,m.nick_name))

            print("<Initial Complete>")
            return 1



    def idle_main(self):
        if not self.plurk.is_authorized():
            return 0
        #print("Pass in idle.")
        if self.__debug:
            cmd=input("\033[0;33m[pyplurky]❯ \033[0m")
            if cmd=="exit":
                return 2
            p=self.plurk
            print(eval(cmd))
            return 1
        else:
            try:
                cmd=input("\033[0;33m[pyplurky]❯ \033[0m")
                if cmd=="exit":
                    return 2
                elif cmd=="":
                    return 1
                p=self.plurk
                print(eval(cmd))
                return 1
            except KeyboardInterrupt:
                print("\nInput <exit> to leave.")
                return 1
            except Exception as e:
                self.__error=e
                return 99

    def listening(self):
        """Main program"""
        if self.__debug:
            print(self.__repeat_handler)
            for f in self.__repeat_handler:
                print("Doing",f)
                f(self.plurk)
            #print("Listening")
            comet_data=self.plurk.realtime.get(self.__offset)
            print(comet_data)
            self.__offset=comet_data.new_offset
            for d in comet_data.data:
                if d.type=="new_response":
                    for f in self.__response_handler:
                        print("Checking",f)
                        handle_response(d,self.plurk,f,self.__response_handler[f])
                elif d.type=="new_plurk":
                    for f in self.__plurk_handler:
                        print("Checking",f)
                        handle_plurk(d,self.plurk,f,self.__plurk_handler[f])
            return 1
        else:
            try:
                for f in self.__repeat_handler:
                    f(self.plurk)
                comet_data=self.plurk.realtime.get(self.__offset)
                print(comet_data)
                self.__offset=comet_data.new_offset
                for d in comet_data.data:
                    if d.type=="new_response":
                        for f in self.__response_handler:
                            handle_response(d,self.plurk,f,self.__response_handler[f])
                    elif d.type=="new_plurk":
                        for f in self.__plurk_handler:
                            handle_response(d,self.plurk,f,self.__plurk_handler[f])
            except Exception as e:
                self.__error=e
                return 99

        return 1


    def error(self):
        #print(plurk.error())
        t=type(self.__error).__name__+": "+str(self.__error)+"\n"
        sys.stderr.write(t)

        self.__error=""
        return 1


    def state_handler(self,status):
        if self.status==0:
            return self.init_main()
        elif self.status==1:
            if self.__mode=="REPL":
                return self.idle_main()
            elif self.__mode=="BOT":
                return self.listening()
        elif self.status==99:
            return self.error()
        elif self.status==2:
            self.exit()
            return -1

    def exit(self):
        self.__job.stop()


    def main(self):
        try:
            """Main program"""
            while 1:
                self.status=self.state_handler(self.status)
                if self.status==-1:
                    #self.__job.stop()
                    break
        except KeyboardInterrupt:
            self.exit()
            print("\rSee you again.")
