from urllib import request
from urllib import error
import json
import pdb


class JsonDecoder:
    def __init__(self, url):
        assert type(url) != None
        self.__url = url

    def get_content_from_url(self, curr, symbol):
        """ This method gets json from URL and convert it into python object(dictionary/list) """
        try:
            response = request.urlopen(self.__url)
            self.data = json.loads(response.read())
            coin_data = self.data["data"]
            for i in coin_data:
                if i["symbol"] == symbol:
                    print("Name:", i["name"])
                    print("Symbol:", i["symbol"])
                    print(i["quote"][curr])
        except error.HTTPError as e:
            if hasattr(e, 'code'):
                print(e.code)
            if hasattr(e, 'reason'):
                print(e.reason)
        # print(coin_data[0]["quote"])
