#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
author: Aleksey Demidov
email: al.kashtan.ex@gmail.com
"""

import kibana_transfer as transferer
import sys
import os

git_repo = os.environ.get('GIT_REPO')
kibana_url = os.environ.get('KIBANA_URL')
if os.environ.get('KIBANA_BACKUP_PREFIX'):
    prefix = os.environ.get('KIBANA_BACKUP_PREFIX')
else:
    prefix = ''

types = ['search', 'dashboard', 'visualization']


def main(method):
    local_path = '/tmp/kibana'
    transferer.common.mkdir(local_path)

    repo = transferer.git.Git(local_path, git_repo)
    repo.gitrepo()
    repo.git_pull()

    if method == 'backup':
        kibana = transferer.kibana.Kibana(kibana_url)

        for object_type in types:
            objects = kibana.find_templates(object_type)
            if objects:
                for obj in objects:
                    if prefix in obj['attributes']['title']:
                        obj_data = kibana.convert_body(obj['attributes'])
                        backup_body = '{"attributes":' + obj_data + '}'
                        transferer.common.save_to_file(local_path, obj['id'], backup_body, object_type)
                        print('{} {} with id {} - saved to local file'.format(object_type, obj['attributes']['title'], obj['id']))
            else:
                print('No {} to backup'.format(object_type))

        git_changed = repo.git_status()

        if git_changed:
            repo.git_add()
            repo.git_commit('autobackup')
            repo.git_push()
        else:
            print('Nothing to backup')
    elif method == 'restore':
        kibana = transferer.kibana.Kibana(kibana_url)

        for object_type in types:
            if os.path.isdir('{}/{}'.format(local_path, object_type)):
                objects = transferer.common.list_dir('{}/{}'.format(local_path, object_type))
                for obj in objects:
                    data = transferer.common.read_from_file(local_path, obj, object_type)
                    kibana.put_template(object_type, obj, data)
                    print('{} with id {} - restored.'.format(object_type, obj))
            else:
                print('No {} to restore'.format(object_type))

if __name__ == '__main__':
    main(sys.argv[1])
