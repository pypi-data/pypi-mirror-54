#!/usr/bin/env python3

import requests
import git
import getpass
import random
import string
import sys


class AutoGit(object):
    ''' Automate git for csv editing, must use a fork of upstream'''

    def __init__(self, repo_path, file_name):

        repo = git.Repo(repo_path)
        self.repo = repo
        self.file_name = file_name

        try:
            branches = repo.git.branch()
            tree_clean = repo.git.status()
            assert('* master' in branches)
            assert(tree_clean.endswith('nothing to commit, working tree'
                   ' clean'))
        except AssertionError:

            print()
            print('  !!!Bro you have to be on your master branch and your'
                  ' working tree clean!!!'.upper())
            sys.exit()

        try:
            requests.get('http://www.google.com', timeout=3)  # test internet
            print("I'm pulling from your upstream and pushing to your fork,"
                  " might take a minute...")
            repo.git.pull('upstream', 'master')
            repo.git.push()

        except requests.ConnectionError:
            print("seems you don't have internet, will work with the out of"
                  " date repo\n")

        finally:
            username = getpass.getuser()
            rand_sequence = ''.join(random.choices(string.ascii_letters
                                    + string.digits, k=6))
            branch_string = f'{username}_{file_name}_{rand_sequence}'
            repo.git.checkout('origin/master', b=branch_string)
            print(f'New branch {branch_string} created and checked out')
            self.branch_string = branch_string

    def commit_push(self):

        repo = self.repo
        repo.git.add(self.file_name)
        repo.git.commit(m=self.branch_string)
        try:
            requests.get('http://www.google.com', timeout=3)  # test internet
            repo.git.push('origin', 'HEAD')
            print('  committed and pushed to your fork!\n')

        except requests.ConnectionError:
            print("Seems you don't have internet, you will have to push this"
                  " branch manually later.")

        repo.git.checkout('master')
        print("  I've checked out master for you.\n")
        #  Maybe delete branch after checking out master.

    def wait_here(self):
        input('waiting for you to press enter:>\n')


if __name__ == '__main__':

    auto_git = AutoGit('/home/miles/github/sit', 'test_file')
    # Give you a chance to create test_file.
    auto_git.wait_here()
    auto_git.commit_push()
