# -*- coding: utf-8 -*-

"""
author: Aleksey Demidov
email: al.kashtan.ex@gmail.com
"""

import os
import sys


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
