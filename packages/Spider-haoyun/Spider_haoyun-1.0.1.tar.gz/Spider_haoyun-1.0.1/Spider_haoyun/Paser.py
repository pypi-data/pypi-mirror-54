import datetime
import json
import os
import re
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class mobanParse(object):

    def __init__(self, file_path="moban"):
        with open(os.path.join(os.getcwd(),"json",file_path), "r", encoding="utf-8")as f:
            self.dict_json = json.loads(f.read())
    def run(self,response):
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
                    info = response.xpath("string(" + xpath + ")").get()#不为内置便直接执行xapth语句
                    if regex and info:
                        info = re.search(regex, info)
                        info = info.group(1) if info else None
                    if info:
                        info = re.sub("\t+|\r+|\n+|\s+", "╪", info.strip())
                        info = re.sub("╪+", "╪", info.strip())
                if info:
                    if len(info) > 0:
                        dict_info[dic["name"]] = info
        return dict_info



