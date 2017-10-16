#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
author: Aleksey Demidov
email: al.kashtan.ex@gmail.com
"""

import kibana_transfer as transferer
import sys


def main(method):
    elastic_url, elastic_r_url, gitlab_token, gitlab_repo, local_path = transferer.common.conf()

    transferer.common.mkdir(local_path)

    repo = transferer.git.Git(local_path, gitlab_repo, gitlab_token, ssl_verify=False)
    repo.gitrepo()
    repo.git_pull()

    if method == 'backup':
        kibana = transferer.kibana.Kibana(elastic_url)

        templates = kibana.search_s_template()
        if templates:
            for template in templates:
                template_data = kibana.get_s_template_body(template)
                transferer.common.save_to_file(local_path, template, template_data, 'search')

        dashes = kibana.search_dashboards()
        if dashes:
            for dashboard in dashes:
                dashboard_data = kibana.get_dashboard_body(dashboard)
                transferer.common.save_to_file(local_path, dashboard, dashboard_data, 'dashboard')

        git_changed = repo.git_status()

        if git_changed:
            repo.git_add()
            repo.git_commit('backuped')
            repo.git_push()
        else:
            print('Nothing to backup')
    elif method == 'restore':
        kibana = transferer.kibana.Kibana(elastic_r_url)

        templates = transferer.common.list_dir(local_path + '/' + 'searches')
        for tmplt in templates:
            data = transferer.common.read_from_file(local_path, tmplt, 'searches')
            kibana.put_s_template(tmplt, data)

        dashboards = transferer.common.list_dir(local_path + '/' + 'dashboards')
        for dshbrd in dashboards:
            data = transferer.common.read_from_file(local_path, dshbrd, 'dashboards')
            kibana.put_dashboard(dshbrd, data)

if __name__ == '__main__':
    main(sys.argv[1])
