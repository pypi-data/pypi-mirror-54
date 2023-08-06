#!/usr/bin/env python3

''' Takes an ini file as an argument to add lines in a csv file and sort.
    Then push to github.'''

import sys
from pathlib import Path
from importlib import resources

from rimteam_editor.line_builder import LineBuild
from rimteam_editor.automatic_gitting import AutoGit


def get_file(file_path):
    with open(file_path) as f:
        return f.readlines()


def save_file(file_path, contents):
    with open(file_path, 'w') as f:
        contents[1:] = sorted(contents[1:], key=str.lower)
        f.writelines(contents)


def show_code(site_code, contents):
    found = False
    for line in contents:
        if site_code in line:
            print(line, end='')
            found = True
    if found is False:
        print('No existing lines found\n')


def main():
    # sys.argv[1] is your ini file eg power.ini
    if len(sys.argv) < 2:
        print('You must start the editor with a an argument eg :~$ reditor'
              ' power (if editing power.csv)')
        sys.exit()

    # Doesn't matter if you call reditor with eg power, power.ini or power.csv.
    arg_1 = sys.argv[1].split('.')[0] + '.ini'

    with resources.path('rimteam_editor', arg_1) as p:
        ini_path = p

    line_build = LineBuild(ini_path)
    the_file = line_build.file
    rep = line_build.repo
    home = str(Path.home())
    repo_path = input(
            f'enter your repo path eg {home}/github/sit or enter if correct:> '
            )
    if '/home/' not in repo_path:
        repo_path = f'{home}/github/{rep}'
    file_path = repo_path + '/' + the_file

    autogit = AutoGit(repo_path, the_file)

    contents = get_file(file_path)

    message = 'Enter site code:> '

    while True:

        control = input(message)
        if len(control) >= 3 and control[:3].isalpha():
            site_code = control.upper()
            show_code(site_code, contents)

            message = ('Enter new site_code, press enter to use the same or c '
                       'to commit:> ')
        elif control == '':
            pass

        elif control == 'c':
            break
        elif control.split()[0] == 'rm':
            if line_build.delete_lines == 'true':
                print('removing line ', int(control.split()[1]))
                found = 0
                for line in contents:
                    if site_code in line:
                        found += 1
                        if found == int(control.split()[1]):
                            contents.remove(line)
                            show_code(site_code, contents)
                            save_file(file_path, contents)
            else:
                print(f'\nfunction not enabled for {the_file}\n')
            continue

        elif control.split()[0] == 'dt':
            if line_build.close_date == 'true':
                found = 0
                for line in contents:
                    if site_code in line:
                        found += 1
                        if found == int(control.split()[1]):
                            contents.remove(line)
                            new_date = control.split()[2]
                            if new_date == 't':
                                new_date = line_build.today
                            contents.append(line.replace('1/1/1999', new_date))
                            show_code(site_code, contents)
                            save_file(file_path, contents)
            else:
                print(f'\nfunction not enabled for {the_file}\n')
            continue

        else:
            print('Not valid input, enter something else')
            continue

        new_line = line_build.make_line(site_code)
        if new_line is not None:
            max_line = None
            for line in contents:
                if site_code in line:
                    max_line = contents.index(line)
            if max_line:
                contents.insert((max_line + 1), new_line)
            else:
                contents.append(new_line)
            save_file(file_path, contents)
        show_code(site_code, contents)
    autogit.commit_push()


if __name__ == '__main__':
    main()
