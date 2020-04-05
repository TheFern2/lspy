#!/usr/bin/python3

import os
import argparse

def remove_dot_files(list_files):
    non_dot_list = []
    for file in list_files:
        if not file.startswith('.'):
            non_dot_list.append(file)
    return non_dot_list


# 0, list multiple columns
# 1, list in one column
def default_listing(listing_mode=0):
    dir_list = os.listdir()
    if listing_mode == 0:
        dir_list = remove_dot_files(dir_list)
        print(" ".join(dir_list))
    if listing_mode == 1:
        dir_list = remove_dot_files(dir_list)
        for file in dir_list:
            print(file)
    if listing_mode == 2:
        for file in dir_list:
            print(file)
    if listing_mode == 3:
        for file in dir_list:
            print(file)
    
  
def main():
        parser = argparse.ArgumentParser()
        parser.add_argument('-l', '--list', dest='list_files', help='list files', action='store_true')
        parser.add_argument('-a', '--all', dest='list_hidden_files', help='list hidden files', action='store_true')
        parser.set_defaults(list_files=False, list_hidden_files=False)
        args = parser.parse_args()
  
        # if -l is given print in one column
        if args.list_files:
            default_listing(1)
        if args.list_files and args.list_hidden_files:
            default_listing(3)
        if args.list_hidden_files:
            default_listing(2)
        else:
            # list files in multiple columns
            default_listing(0)
 
 
if __name__ == '__main__':
          main()