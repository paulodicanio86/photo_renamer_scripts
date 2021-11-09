#! /usr/bin/env python3

import os
import argparse
import sys
from datetime import datetime
from PIL import Image
from PIL.ExifTags import TAGS


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


def get_exif_value(fn, field):
    ret = {}
    i = Image.open(fn)
    info = i._getexif()
    if info is not None:
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            ret[decoded] = value
        # uncomment to show all available EXIF fields
        #print(ret)
        if field in ret:
            return ret[field]
    return None


def get_DateTimeOriginal(fn):
    dto_str = get_exif_value(fn, "DateTimeOriginal")
    if dto_str is not None:
        dto_obj = datetime.strptime(dto_str, '%Y:%m:%d %H:%M:%S')
        time_tag = dto_obj.strftime('%Y%m%d-%H%M%S')
        return time_tag
    # if EXIF information does not exist use the file creation date:
    else:
        return get_CreationDate(fn)


def get_CreationDate(path):
    ctime = os.stat(path).st_mtime
    return datetime.fromtimestamp(ctime).strftime('%Y%m%d-%H%M%S')


def rename_photos(_dir, name_tag):
    # consider only image and movie files
    image_extensions = ['jpg', 'jpeg']
    video_extensions = ['mov', 'mp4']
    extensions = image_extensions + video_extensions
    file_list = []
    
    time_tag_list = []
    counter = 2  # for the rare case when 2 or more photos have the same timestamp (see below)
    for fn in os.listdir(_dir):
        if any(fn.lower().endswith(ext) for ext in extensions):
            file_list.append(fn)

    for fn in file_list:
        oldpath = os.path.join(_dir, fn)
        ext = fn.lower().split('.')[-1]
        
        # Videos: use OS creation time stamp
        if ext in video_extensions:
            time_tag = get_CreationDate(oldpath)
        # Images: use EXIF time stamp
        elif ext in image_extensions:
            time_tag = get_DateTimeOriginal(oldpath)
            
        # check the rare case when we have duplicate time tag and if so, append counter to name
        if time_tag in time_tag_list:
            name_tag_new = name_tag + '-' + str(counter)
            counter += 1
        else:
            name_tag_new = name_tag
            time_tag_list.append(time_tag)
            # reset
            counter = 2

        # rename
        newpath = os.path.join(_dir, '{}-{}.{}'.format(time_tag, name_tag_new, ext))
        print('---------\nOLD:\t{}\nNEW:\t{}'.format(oldpath, newpath))
        os.rename(oldpath, newpath)
    pass


def print_giraffe():
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


if __name__ == "__main__":
    _dir, name_tag = validate_user_inputs()
    rename_photos(_dir, name_tag)
    print_giraffe()
    
    pass

# ---------------------------
# NOTES
# ---------------------------

# though note below doesn't get all the mac related attributes
# info = os.stat(oldpath)
# instead using xattr module (installed via pip) - this doesn't get the created and modified times,
# it's for other attributes, see https://stackoverflow.com/questions/33181948/how-to-get-extended-macos-attributes-of-a-file-using-python
# info = xattr.xattr(_path + '/' + fn)

# Get created time
# WARNING: https://docs.python.org/2/library/stat.html#stat.ST_CTIME
# On some systems (like Unix) is the time of the last metadata change, and, on others (like Windows), is the creation time
# In this mac it seems to be also the first case
# ctime = os.path.getctime(oldpath)
# time_tag = datetime.datetime.fromtimestamp(ctime).strftime('%Y%m%d-%H%M%S')
