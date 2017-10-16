# -*- coding: utf-8 -*-

"""
author: Aleksey Demidov
email: al.kashtan.ex@gmail.com
"""

import configparser
import os
import sys


def conf():

    """ read configuration from transfer.conf """

    config = configparser.ConfigParser()
    config.read(sys.path[0] + '/transfer.conf')
    elastic_url = config.get('elasticsearch', 'url')
    elastic_usr = config.get('elasticsearch', 'user')
    elastic_pwd = config.get('elasticsearch', 'password')
    elastic_r_url = config.get('elasticsearch', 'url_remote')
    elastic_r_usr = config.get('elasticsearch', 'user_remote')
    elastic_r_pwd = config.get('elasticsearch', 'password_remote')
    gitlab_token = config.get('git', 'token')
    gitlab_repo = config.get('git', 'repository')
    local_path = config.get('local', 'directory')
    return elastic_url, elastic_r_url, gitlab_token, gitlab_repo, local_path


def mkdir(path):

    """ make directory """

    os.makedirs(path, exist_ok=True)


def list_dir(path):

    """ list directory """

    directories = os.listdir(str(path))
    return directories


def save_to_file(local_path, filename, data, datatype):

    """ save data to local file """

    path = local_path
    if datatype == 'dashboard':
        path += '/dashboards'
    elif datatype == 'search':
        path += '/searches'
    filepath = path + '/' + filename
    mkdir(path)
    with open(filepath, 'w') as f:
        f.write(data)


def read_from_file(local_path, filename, datatype):

    """ read data from local file """

    path = local_path + '/' + datatype + '/' + filename
    with open(path, 'r') as f:
        filedata = f.read()
    return filedata
