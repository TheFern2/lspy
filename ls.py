#!/usr/bin/python3

import os
import argparse
from pwd import getpwuid
from grp import getgrgid
import datetime
from stat import filemode, S_ISDIR, S_ISREG, S_IEXEC
from termcolor import colored, cprint
import stat

def remove_dot_files(list_files):
    non_dot_list = []
    for file in list_files:
        if not file.startswith('.'):
            non_dot_list.append(file)
    return non_dot_list


def find_owner(uid):
    return getpwuid(uid).pw_name


def find_group(gid):
    return  getgrgid(gid).gr_name


# https://www.garron.me/en/go2linux/ls-file-permissions.html
# https://stackoverflow.com/questions/5337070/how-can-i-get-the-unix-permission-mask-from-a-file
# https://stackoverflow.com/questions/1830618/how-to-find-the-owner-of-a-file-or-directory-in-python
# https://stackoverflow.com/questions/39359245/from-stat-st-mtime-to-datetime
def get_file_stats(file, get_oct_chmod=False):
    filename = file
    cwd = os.getcwd()
    stats = os.stat(cwd + "/" + filename)
    if get_oct_chmod:
        chmod = oct(stats[0])[-3:]
    else:
        chmod = filemode(stats[0])
    #numeric_chmod = oct(stats[0])[-3:]    
    number_of_links = stats[3]
    user = find_owner(stats[4])
    group = find_group(stats[5])
    size = stats[6]
    mod_timestamp = datetime.datetime.fromtimestamp(stats[8])
    formatted_timestamp = mod_timestamp.strftime("%b %d %H:%M")

    return MyFileStat(chmod, number_of_links, user, group, size, formatted_timestamp, filename, stats)


# get terminal width size
# if files can fit do a join,
# if not builds columns vertically
def show_files_vertical_columns(files):
    rows, columns = os.popen('stty size', 'r').read().split()
    print(columns)
    files_info = []

    for file in files:
        files_info.append(get_file_stats(file))

    for file in files_info:
        print("{}".format(StringColorizer(file.filename, file.stats)), end=" ")


def show_files_one_column(files, get_oct_chmod=False):
    files_info = []

    # track our columns string size
    number_of_links_length = 0
    user_length = 0
    group_length = 0
    size_lenght = 0

    for file in files:
        files_info.append(get_file_stats(file, get_oct_chmod))

    # find longest strings for calculating padding
    for file in files_info:

        if len(str(file.number_of_links)) > number_of_links_length:
            number_of_links_length = len(str(file.number_of_links))
        
        if len(file.user) > user_length:
            user_length = len(file.user)

        if len(file.group) > group_length:
            group_length = len(file.group)

        if len(str(file.size)) > size_lenght:
            size_lenght = len(str(file.size))


    for file in files_info:
        
        # Self notes: This was by far the hardest part of this little project. :)
        # I had never worked with columns much before, once figured out it was a truly
        # tada moment.
        # Only uses empty curly braces for items that do not take any parametrized values
        # All key=value need to go at the end.
        # Parametrized format in the string goes inside another set of curly braces
        # "{} {:{first_parameter}{second_parameter}} {:{first_parameter}}"
        # https://pyformat.info/
        print("{} {:{links_padding}} {:{user_padding}} {:{group_padding}} {:{align}{size_padding}} {} {}".format(
            file.chmod,
            file.number_of_links,
            file.user,
            file.group,
            file.size,
            file.mod_timestamp,
            StringColorizer(file.filename, file.stats),
            links_padding=str(number_of_links_length),
            user_padding=str(user_length),
            group_padding=str(group_length),
            size_padding=str(size_lenght),
            align='>'   
            ))

def default_listing(show_dot_files=False, list_files=False, get_oct_chmod=False):
    dir_list = os.listdir()
    dir_list.sort(key=str.lower)

    if not show_dot_files:
        dir_list = remove_dot_files(dir_list)

    if list_files:
        show_files_one_column(dir_list, get_oct_chmod)
    else:
        #print("  ".join(dir_list)) # initial print
        show_files_vertical_columns(dir_list)

# chmod, number_of_links, user, group, size, mod_timestamp, file
class MyFileStat:
    def __init__(self, chmod, number_of_links, user, group, size, mod_timestamp, filename, stats):
        self.chmod = chmod
        self.number_of_links = number_of_links
        self.user = user
        self.group = group
        self.size = size
        self.mod_timestamp = mod_timestamp
        self.filename = filename
        self.stats = stats


class StringColorizer:
    def __init__(self, string_to_print, stats):
        self.string_to_print = string_to_print
        self.stats = stats

    def __format__(self, format):
        default_color = 'white'
        image_extensions = ['.png', '.jpg','.jpeg', '.tif', '.tiff', '.bmp', '.gif', '.png', '.raw']

        for ext in image_extensions:
            if self.string_to_print.endswith(ext):
                return colored(self.string_to_print, 'magenta', attrs=['bold'])

        if stat.S_ISDIR(self.stats[0]):
            return colored(self.string_to_print, 'blue', attrs=['bold'])
        
        if stat.S_IXUSR & self.stats[0]:
            return colored(self.string_to_print, 'green', attrs=['bold'])

        if stat.S_ISREG(self.stats[0]):
            return colored(self.string_to_print, 'white')

        return colored(self.string_to_print, default_color)
  
def main():
        parser = argparse.ArgumentParser()
        parser.add_argument('-l', '--list', dest='list_files', help='list files', action='store_true')
        parser.add_argument('-a', '--all', dest='list_hidden_files', help='list hidden files', action='store_true')
        parser.add_argument('-n', '--numeric-chmod',  dest='numeric_chmod',help='chmod as octal numeric', action='store_true')
        parser.set_defaults(list_files=False, list_hidden_files=False, numeric_chmod=False)
        args = parser.parse_args()
  
        default_listing(args.list_hidden_files, args.list_files, args.numeric_chmod)
 
 
if __name__ == '__main__':
          main()
