import hashlib
import datetime
import re

def get_ma5(url):
    if isinstance(url, str):
        url = url.encode("utf-8")
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()


def date_convert(value):
    try:
        create_time = datetime.datetime.strptime(value, "%Y/%m/%d").date()
    except Exception as e:
        create_time = datetime.datetime.now().date()
    return create_time


def remove_comment_tags(value):
    #去掉tag中提取的评论
    if "评论" in value:
        return ""
    else:
        return value


def deal_with_time(value):
    creat_time = value[0].strip().replace("·", "").strip()
    return creat_time


def return_value(value):
    return value


def remove_splash(value):
        # 去掉斜杠
    return value.replace("/", "")


def remove_comment_addr(value):
    item_list = value.split("\n")
    tag_list = [item.strip() for item in item_list if item.strip() != "查看地图"]
    return "".join(tag_list)


def main():
    get_ma5()
    date_convert()
    remove_comment_tags()
    deal_with_time()
    remove_splash()
    remove_comment_addr()
    return_value()


if __name__ == '__main__':
    main()
