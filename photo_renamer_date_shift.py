#! /usr/bin/env python3

import sys
import os
import datetime
import argparse
from PIL import Image


def validate_user_inputs():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('path', metavar='path', type=str,
                    help='path to photo directory')
    parser.add_argument('name', metavar='name', type=str,
                    help='common name to add to photo files')
    args = parser.parse_args()
    args_values = vars(args)

    name_tag = args_values['name']
    cwd = os.getcwd()
    _dir = os.path.join(cwd, args_values['path'])

    try:
        fList = os.listdir(_dir)
    except OSError:
        sys.exit("-> ERROR: That directory doesn't exist")

    return _dir, name_tag


def get_delta(_dir, start_dt):
    #  filter only image files                                                                                                                                                                      
    extenstions = ['jpg', 'jpeg']

    #x = datetime.datetime(2019, 5, 24, 9, 0)

    #find minimum time
    time_tags = []
    for fn in os.listdir(_dir):
        # Check if files is an image                                                                                                                                                                    
        if any(fn.lower().endswith(ext) for ext in extenstions):
            ext = fn.lower().split('.')[-1]
            oldpath = os.path.join(_dir, fn)
            # Get created time
            try:
                dt_str = Image.open(oldpath)._getexif()[36867]
                dt = datetime.datetime.strptime(dt_str, '%Y:%m:%d %H:%M:%S')

            except (KeyError, TypeError) as e:
                mctime = os.path.getctime(oldpath) # last meta data change time stamp                                                                                                              
                ctime = os.stat(oldpath).st_birthtime # creation date time stamp
                dt = datetime.datetime.fromtimestamp(ctime)

            time_tags.append(dt)

    dt_min = min(time_tags)
    dt_delta = start_dt - dt_min

    return dt_delta

def rename_photos(_dir, name_tag, dt_delta):
    extenstions = ['jpg', 'jpeg']
    
    time_tags = []
    for fn in os.listdir(_dir):
        # Check if files is an image
        if any(fn.lower().endswith(ext) for ext in extenstions):
            ext = fn.lower().split('.')[-1]
            oldpath = os.path.join(_dir, fn)
            # Get created time and add delta
            try:
                dt_str = Image.open(oldpath)._getexif()[36867]
                dt = datetime.datetime.strptime(dt_str, '%Y:%m:%d %H:%M:%S')                                                                                                              
                dt = dt + dt_delta
                time_tag = dt.strftime('%Y%m%d-%H%M%S')

            except (KeyError, TypeError) as e:
                mctime = os.path.getctime(oldpath) # last meta data change time stamp
                ctime = os.stat(oldpath).st_birthtime # creation date time stamp
                dt = datetime.datetime.fromtimestamp(ctime)
                dt = dt + dt_delta
                time_tag = dt.strftime('%Y%m%d-%H%M%S')

            # Check the rare case when we have duplicate time_tags and if so, append counter tag to name
            if time_tag in time_tags:
                counter = time_tags.count(time_tag) + 1
                name_tag_new = name_tag + '_' + str(counter)
            else:
                name_tag_new = name_tag
                time_tags += [time_tag]

            newpath = os.path.join(_dir, '{}-{}.{}'.format(time_tag, name_tag_new, ext))
            print('---------\nOLD:\t{}\nNEW:\t{}'.format(oldpath, newpath))
            os.rename(oldpath, newpath)
    print("""\
                                           ._ o o
                                           \_`-)|_
                                        ,""       \ 
                                      ,"  ## |   o o. 
                                    ," ##   ,-\__    `.
                                  ,"       /     `--._;)
                                ,"     ## /               ---HAHA
                              ,"   ##    /
                        """)
    print('-> INFO: FINISHED!')
    pass


def get_start_date():
    year = int(input('Enter a year (YYYY): '))
    month = int(input('Enter a month (MM): '))
    day = int(input('Enter a day (DD): '))
    hour = int(input('Enter an hour (hh): '))
    minute = int(input('Enter a minute (mm): '))
    second = int(input('Enter a second (ss): '))
    return  datetime.datetime(year, month, day, hour, minute, second)

if __name__ == "__main__":

    _dir, name_tag = validate_user_inputs()

    start_date = get_start_date()
    #start_date = datetime.datetime(2016, 6, 4, 12, 25)
    delta = get_delta(_dir, start_date)
    rename_photos(_dir, name_tag, delta)

    pass

