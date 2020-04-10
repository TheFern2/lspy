#!/usr/bin/python3

import os
import argparse
from pwd import getpwuid
from grp import getgrgid
import datetime

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
def get_file_stats(file):
    cwd = os.getcwd()
    stats = os.stat(cwd + "/" + file)
    numeric_chmod = oct(stats[0])[-3:]
    number_of_links = stats[3]
    user = find_owner(stats[4])
    group = find_group(stats[5])
    size = stats[6]
    mod_timestamp = datetime.datetime.fromtimestamp(stats[8])

    # print(numeric_chmod, number_of_links, user, group, size, mod_timestamp, file)
    print("{} {} {:10} {:10} {:8} {} {}".format(numeric_chmod, number_of_links, user, group, size, mod_timestamp, file))


def show_files_one_column(files):
    for file in files:
        #print(file)
        get_file_stats(file)


def default_listing(show_dot_files=False, list_files=False):
    dir_list = os.listdir()
    dir_list.sort(key=str.lower)

    if not show_dot_files:
        dir_list = remove_dot_files(dir_list)

    if list_files:
        show_files_one_column(dir_list)
    else:
        print("  ".join(dir_list))
    
  
def main():
        parser = argparse.ArgumentParser()
        parser.add_argument('-l', '--list', dest='list_files', help='list files', action='store_true')
        parser.add_argument('-a', '--all', dest='list_hidden_files', help='list hidden files', action='store_true')
        parser.set_defaults(list_files=False, list_hidden_files=False)
        args = parser.parse_args()
  
        default_listing(args.list_hidden_files, args.list_files)
 
 
if __name__ == '__main__':
          main()