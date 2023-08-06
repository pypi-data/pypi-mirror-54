from oauth2 import (
    Client, Consumer, Request,
    SignatureMethod_HMAC_SHA1, Token,
)
from urllib.parse import parse_qsl
from urllib.parse import urlencode
import requests
from plurk_oauth import PlurkOAuth

class oauth_recover(PlurkOAuth):
    def request(self, url, params={}, data={}, files={}):
        """ Return: status code, json object, status reason """



        # Setup
        if self.oauth_token:
            self.token = Token(self.oauth_token['oauth_token'],
                               self.oauth_token['oauth_token_secret'])
        req = self._make_request(self.base_url + url, data)

        req_files = {}
        try:
            if files:
                for (name, fpath) in files.items():
                    req_files[name] = open(fpath, 'rb')

            r = requests.post(
                self.base_url + url,
                headers=req.to_header(),
                data=data,
                files=req_files if req_files else None
            )

        except requests.RequestException as ex:
            print >> sys.stderr, ex
            sys.exit(1)
        except:
            print >> sys.stderr
            sys.exit(1)
        finally:
            for name, ofile in req_files.items():
                 ofile.close()
        try:
            return r.status_code, r.json(), r.reason
        except:
            return r.status_code, r.text, r.reason
    def get_access_token(self, verifier):
        status, content, reason = self.request(self.access_token_url, data={
            'oauth_token_secret': self.oauth_token['oauth_token_secret'],
            'oauth_verifier': verifier,
        })
        if str(status) != '200':
            raise Exception(reason)
        self.oauth_token = dict(parse_qsl(content))
        self._dump(self.oauth_token)
