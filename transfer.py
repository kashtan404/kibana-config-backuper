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
elastic_url = os.environ.get('ELASTICSEARCH_URL')


def main(method):
    local_path = '/tmp/kibana'
    transferer.common.mkdir(local_path)

    repo = transferer.git.Git(local_path, git_repo)
    repo.gitrepo()
    repo.git_pull()

    if method == 'backup':
        kibana = transferer.kibana.Kibana(elastic_url)

        templates = kibana.search_s_template()
        if templates:
            for template in templates:
                template_data = kibana.get_s_template_body(template)
                transferer.common.save_to_file(local_path, template, template_data, 'searches')
        else:
            print('No searches to backup')

        dashes = kibana.search_dashboards()
        if dashes:
            for dashboard in dashes:
                dashboard_data = kibana.get_dashboard_body(dashboard)
                transferer.common.save_to_file(local_path, dashboard, dashboard_data, 'dashboards')
        else:
            print('No dashboards to backup')

        git_changed = repo.git_status()

        if git_changed:
            repo.git_add()
            repo.git_commit('autobackup')
            repo.git_push()
        else:
            print('Nothing to backup')
    elif method == 'restore':
        kibana = transferer.kibana.Kibana(elastic_url)

        if os.path.isdir('{}/searches'.format(local_path)):
            templates = transferer.common.list_dir('{}/searches'.format(local_path))
            for tmplt in templates:
                data = transferer.common.read_from_file(local_path, tmplt, 'searches')
                kibana.put_s_template(tmplt, data)
        else:
            print('No searches to restore')

        if os.path.isdir('{}/dashboards'.format(local_path)):
            dashboards = transferer.common.list_dir('{}/dashboards'.format(local_path))
            for dshbrd in dashboards:
                data = transferer.common.read_from_file(local_path, dshbrd, 'dashboards')
                kibana.put_dashboard(dshbrd, data)
        else:
            print('No dashboards to restore')

if __name__ == '__main__':
    main(sys.argv[1])
