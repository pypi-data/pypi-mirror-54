#!/usr/bin/env python3
import configparser
from datetime import datetime


class LineBuild(object):
    """Builds a line to insert into csv file depending on user input and 
       options in an INI file."""

    def __init__(self, ini_file):

        config = configparser.ConfigParser()
        config.optionxform = str  # Don't lowercase the keys
        config.read(ini_file)

        self.config = config
        self.file = config['file_path']['fp']
        self.repo = config['repository']['repo']
        self.last_date = None
        self.delete_lines = config['functions']['delete_lines']
        self.close_date = config['functions']['close_date']

    @property
    def today(self):

        return datetime.today().strftime('%d/%m/%Y')

    def make_line(self, site_code):

        config = self.config
        options_dict = config['options']

        choice_dict = {n: k for n, k in enumerate(options_dict, 1)}

        # Make a nice menu of the devices
        keys_list = list(choice_dict.keys())
        lines = len(keys_list) // 3
        if lines % 3:
            lines += 1
        start = 0
        print()
        for row in range(1, lines + 1):
            for i in keys_list[start::lines]:
                print(f'{i:2} {choice_dict[i]:22}', end='')
            start += 1
            print()
        print()

        line_out = ''

        selection = input('Enter choice number and press enter:> ')
        if selection == '':
            return
        selection = int(selection)

        line_out = f'{site_code},{options_dict[choice_dict[selection]]}'

        for question in config['inputs']:
            if question in line_out:
                answer = input(f"{config['inputs'][question]}:> ")
                if question == 'DATE' and answer not in config['shortcuts']:
                    self.last_date = answer
                if answer in config['shortcuts']:
                    answer = config['shortcuts'][answer]
                    if answer == 'TODAY':
                        answer = self.today
                        self.last_date = self.today
                    if answer == 'LASTDATE':
                        answer = self.last_date
                line_out = line_out.replace(question, answer)
        return line_out + '\n'


if __name__ == '__main__':

    myobj = LineBuild('power.ini')
    print(myobj.file)
    print(myobj.repo)
    myline = myobj.make_line('ZZZ')
    print(myline)
