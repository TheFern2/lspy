#!/usr/bin/python3

import os
import argparse

def remove_dot_files(list_files):
    non_dot_list = []
    for file in list_files:
        if not file.startswith('.'):
            non_dot_list.append(file)
    return non_dot_list


def show_files_one_column(files):
    for file in files:
        print(file)


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