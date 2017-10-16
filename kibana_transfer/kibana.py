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


def to_plaintext(func):

    """ convert responce content to raw text """

    def wrapper(self, *args, **kwargs):
        """ some replacements to hold elasticsearch format """
        source = func(self, *args, **kwargs).text
        result = source.replace('{"_source":', '')[:-1].replace('\\\\', '\\')
        return result
    return wrapper


def to_list(func):

    """ convert responce content (/_search/) to list of names """

    def wrapper(self, *args, **kwargs):
        source = func(self, *args, **kwargs)['hits']['hits']
        result = []
        for i in source:
            result.append(i['_id'])
        return result
    return wrapper


class Kibana(object):

    def __init__(self, url, **kwargs):
        self.__url = url
        if not kwargs:
            self.__usr = ''
            self.__pwd = ''
        else:
            self.__usr = kwargs['user']
            self.__pwd = kwargs['password']

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
    def __put_request(url, data):
    
        """ http put request """
    
        result = ''
        try:
            result = requests.put(url, data=data, headers={'Content-Type': 'application/json'})
        except Exception as e:
            print(e)
            quit(2)
        return result

    @to_list
    @to_json
    def search_s_template(self):

        """ find search templates """

        s_template_url = self.__url + '/.kibana/search/_search?pretty&filter_path=hits.hits._id'
        return self.__get_request(s_template_url)

    @to_list
    @to_json
    def search_dashboards(self):

        """ find dashboards """

        dashboards_url = self.__url + '/.kibana/dashboard/_search?pretty&filter_path=hits.hits._id'
        return self.__get_request(dashboards_url)

    @to_plaintext
    def get_dashboard_body(self, dashboard_name):

        """ get dashboard body """

        dashboard_url = self.__url + '/.kibana/dashboard/' + dashboard_name + '?filter_path=_source'
        return self.__get_request(dashboard_url)

    @to_plaintext
    def get_s_template_body(self, template_name):

        """ get search template body """

        template_url = self.__url + '/.kibana/search/' + template_name + '?filter_path=_source'
        return self.__get_request(template_url)

    @to_json
    def put_dashboard(self, dashboard_name, dashboard_body):

        """ put dashboard body """

        dashboards_url = self.__url + '/.kibana/dashboard/' + dashboard_name
        return self.__put_request(dashboards_url, dashboard_body)

    @to_json
    def put_s_template(self, template_name, template_body):

        """ put search template body """

        template_url = self.__url + '/.kibana/search/' + template_name
        return self.__put_request(template_url, template_body)
