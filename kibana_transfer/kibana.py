# -*- coding: UTF-8 -*-

"""
author: Aleksey Demidov
email: al.kashtan.ex@gmail.com
"""

import requests
import json


def to_json(func):

    """ convert responce content to json """

    def wrapper(self, *args, **kwargs):
        return json.loads(func(self, *args, **kwargs).content.decode("utf-8"))
    return wrapper


def to_list(func):

    """ convert responce content (/saved_objects/) to list of objects """

    def wrapper(self, *args, **kwargs):
        source = func(self, *args, **kwargs)['saved_objects']
        result = []
        for i in source:
            result.append(i)
        return result
    return wrapper


class Kibana(object):

    def __init__(self, url):
        self.__url = url

    @staticmethod
    def __get_request(url):

        """ http get request """

        result = ''
        try:
            result = requests.get(url)
        except Exception as e:
            print(e)
            quit(2)
        return result

    @staticmethod
    def __post_request(url, data):

        """ http post request """

        result = ''
        try:
            result = requests.post(url, data=data, headers={'Content-Type': 'application/json', 'kbn-xsrf': 'true'})
        except Exception as e:
            print(e)
            quit(2)
        return result

    @to_list
    @to_json
    def find_templates(self, object_type):

        """ find template """

        url = '{}/api/saved_objects/{}'.format(self.__url, object_type)
        return self.__get_request(url)

    def convert_body(self, body):

        """ convert template body """

        converted_body = str(body).replace("False", "false").replace("True", "true").replace("\"","\\\"").replace("\'", "\"")
        return converted_body

    @to_json
    def put_template(self, object_type, object_id, body):

        """ put template body """

        url = '{}/api/saved_objects/{}/{}?overwrite=true'.format(self.__url, object_type, object_id)
        return self.__post_request(url, body)
