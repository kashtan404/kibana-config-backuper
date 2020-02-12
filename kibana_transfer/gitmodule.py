# -*- coding: utf-8 -*-

"""
author: Aleksey Demidov
email: al.kashtan.ex@gmail.com
"""

import subprocess


class Git(object):

    def __init__(self, repo_path, repo_url):
        self.__repo_path = repo_path
        self.__repo_url = repo_url

    @staticmethod
    def __execute(cmd, repodir):

        """ run a shell command """

        pipe = subprocess.Popen(cmd, shell=True, cwd=repodir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (out, error) = pipe.communicate()
        pipe.wait()
        return out, error

    def gitrepo(self):

        """ init and fetch repo """

        self.__git_init()
        self.__git_add_origin()
        self.__git_fetch()

    def __git_init(self):

        """ 'git init' command """

        cmd = 'git init'
        self.__execute(cmd, self.__repo_path)
        return self

    def __git_add_origin(self):

        """ 'git remote add origin <http_url>' command """

        cmd = 'git remote add origin ' + self.__repo_url
        self.__execute(cmd, self.__repo_path)
        return self

    def __git_fetch(self):

        """ 'git fetch' command """

        cmd = 'git fetch'
        self.__execute(cmd, self.__repo_path)
        return self

    def git_add(self):

        """ 'git add -A' command
            add all to solve our work """

        cmd = 'git add -A'
        self.__execute(cmd, self.__repo_path)
        return self

    def git_commit(self, commitmessage):

        """ 'git commit -am "<comment>"' command """

        cmd = 'git commit -am "%s"' % commitmessage
        self.__execute(cmd, self.__repo_path)
        return self

    def git_push(self):

        """ 'git push origin refs/heads/master:refs/heads/master' command
            i use master branch for this, but you can change for what you want """

        cmd = 'git push origin refs/heads/master:refs/heads/master'
        self.__execute(cmd, self.__repo_path)
        return self

    def git_pull(self):

        """ 'git pull origin master' command
            same as git_push() """

        cmd = 'git pull origin master'
        self.__execute(cmd, self.__repo_path)
        return self

    def git_status(self):

        """ 'git status' command
            return only 'false' (no changes) or 'true' (have changes) """

        cmd = 'git status'
        out, err = self.__execute(cmd, self.__repo_path)
        if 'nothing to commit' in str(out):
            return False
        return True
