import base64
import hashlib
import time
from urllib.parse import urlparse


def md5_encrypt(strings):
    """
    使用md5加密字符串
    :param strings: 需要加密的字符串
    :return: md5值
    """
    m = hashlib.md5()
    m.update(bytes(strings, encoding='utf-8'))
    return m.hexdigest()


def base64_encrypt(strings):
    """
    使用base64加密字符串
    :param strings: 需要加密的字符串
    :return: 加密之后的字符串
    """
    data = bytes(strings, encoding="utf-8")
    return str(base64.b64encode(data), encoding='utf8')


def base64_decrypt(strings):
    """
    解密base64加密串
    :param strings: 需要解密的字符串
    :return: 解密之后的字符串
    """
    return base64.b64decode(strings).decode("utf-8")


def get_uri(url):
    """
    返回url地址的path路径
    :param url: url 地址
    :return: path 路径
    """
    return urlparse(url).path


def get_http_headers(var, api):
    """
    生成opsMgr认证的头信息
    :param var: 全局变量
    :param api: api 地址
    :return: header
    """
    time_now = int(time.time())

    sign = md5_encrypt(strings="{id}{token}{uri}{time}".format(
        id=var.ID,
        token=var.TOKEN,
        uri=get_uri(api),
        time=time_now
    ))

    header = {
        "Authorization": base64_encrypt(strings="{time},{sign}".format(time=time_now, sign=sign)),
        "ID": var.ID
    }

    return header
