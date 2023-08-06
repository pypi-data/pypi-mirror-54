import datetime
import json
import os
import re
from jsonpath import jsonpath

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class mobanParse(object):

    def __init__(self,parse_info):
        self.dict_json = parse_info

    def xpathrun(self, response):
        dict_info = {}
        responseurl = response.url.split("?")[0] if "?" in response.url else response.url
        guize = {"$response.url": responseurl, "$Datetime": str(datetime.datetime.now()).split(".")[0],
                 }

        for dic in self.dict_json:
            xpath = dic.get("xpath")
            name = dic.get("name")
            regex = dic.get("regex")
            if xpath:
                if xpath[0] == "$":  # 当目标xpath语句为内设时
                    info = guize[xpath]
                    if regex:
                        info = re.search(regex, info)
                        info = info.group(1) if info else None
                else:
                    info = response.xpath("string(" + xpath + ")").get()  # 不为内置便直接执行xapth语句
                    if regex and info:
                        info = re.search(regex, info)
                        info = info.group(1) if info else None
                    if info:
                        info = re.sub("\t|\r|\n| ", "", info)
                if info:
                    if len(info) > 0:
                        dict_info[dic["name"]] = info
        return dict_info

    def jsonpathrun(self,reponse):
        dict_info = {}
        responseurl = response.url.split("?")[0] if "?" in response.url else response.url
        guize = {"$response.url": responseurl, "$Datetime": str(datetime.datetime.now()).split(".")[0],
                 }

        for dic in self.dict_json:
            xpath = dic.get("xpath")
            name = dic.get("name")
            regex = dic.get("regex")
            if xpath:
                if xpath[0] == "$":  # 当目标xpath语句为内设时
                    info = guize[xpath]
                    if regex:
                        info = re.search(regex, info)
                        info = info.group(1) if info else None
                else:
                    info = jsonpath(json.loads(response.text)) # 不为内置便直接执行xapth语句
                    if regex and info:
                        info = re.search(regex, info)
                        info = info.group(1) if info else None
                    if info:
                        info = re.sub("\t|\r|\n| ", "", info)
                if info:
                    if len(info) > 0:
                        dict_info[dic["name"]] = info
        return dict_info




def phone_format(tel):
    ret = re.match(r"^1\d{10}$", tel)
    if ret:
        return ret





