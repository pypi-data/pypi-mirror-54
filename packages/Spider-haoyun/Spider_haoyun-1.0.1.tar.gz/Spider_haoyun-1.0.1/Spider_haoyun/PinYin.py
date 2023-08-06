
import pypinyin
import re

def PinYin_edit(info):

    ProjectName = info
    if ProjectName and type(ProjectName) == str:
        ressult = "".join(
            list(map(lambda x: x[0], pypinyin.pinyin(ProjectName, style=pypinyin.Style.FIRST_LETTER))))
        return re.sub("[^a-zA-Z0-9]", "", ressult)
    else:
        return None

def QuanPin_edit(info):

    ProjectName = info
    if ProjectName:
        ressult = "".join(pypinyin.lazy_pinyin(ProjectName))
        return re.sub("[^a-zA-Z0-9]", "", ressult)
    else:
        return None