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


def rename_photos(_dir, name_tag):
    #  filter only image files 
    extenstions = ['jpg', 'jpeg']
    # file_names = [fn for fn in os.listdir(_dir) if any(fn.lower().endswith(ext) for ext in extenstions)]

    time_tags = []

    for fn in os.listdir(_dir):
        # Check if files is an image
        if any(fn.lower().endswith(ext) for ext in extenstions):
            ext = fn.lower().split('.')[-1]
            oldpath = os.path.join(_dir, fn)
            # Get created time
            try:
                dt_str = Image.open(oldpath)._getexif()[36867]
                #dt = datetime.datetime.strptime(dt_str, '%Y:%m:%d %H:%M:%S')                                                                                                              
                time_tag = dt_str.replace(':', '').replace(' ', '-')
            except (KeyError, TypeError) as e:
                mctime = os.path.getctime(oldpath) # last meta data change time stamp
                ctime = os.stat(oldpath).st_birthtime # creation date time stamp
                dt = datetime.datetime.fromtimestamp(ctime)
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
                                ,"     ## /
                              ,"   ##    /
                        """)
    print('-> INFO: FINISHED!')
    pass


if __name__ == "__main__":

    _dir, name_tag = validate_user_inputs()
    rename_photos(_dir, name_tag)

    pass

# ---------------------------
# APPENDIX
# ---------------------------

# though note below doesn't get all the mac related attributes
# info = os.stat(oldpath)
# instead using xattr module (installed via pip) - this doesn't get the created and modified times, it's
# for other attributes, see https://stackoverflow.com/questions/33181948/how-to-get-extended-macos-attributes-of-a-file-using-python
# info = xattr.xattr(_path + '/' + fn)

# Get created time
# WARNING: https://docs.python.org/2/library/stat.html#stat.ST_CTIME
# On some systems (like Unix) is the time of the last metadata change, and, on others (like Windows), is the creation time
# In this mac it seems to be also the first case
# ctime = os.path.getctime(oldpath)
# time_tag = datetime.datetime.fromtimestamp(ctime).strftime('%Y%m%d-%H%M%S')
