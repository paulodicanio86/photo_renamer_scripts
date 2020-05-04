#! /usr/bin/env python3

import sys
import os
import time
import argparse
import datetime
import piexif

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


def rename_photos(_dir, name_tag, start_date):
    #  filter only image files
    extenstions = ['jpg', 'jpeg']

    counter = 1
    for fn in sorted(os.listdir(_dir)):
        # Check if files is an image
        if any(fn.lower().endswith(ext) for ext in extenstions):
            ext = fn.lower().split('.')[-1]
            oldpath = os.path.join(_dir, fn)

            #set correct meta data in exif
            try:
                exif_dic = piexif.load(oldpath)
                exif_dic['0th'][306] = start_date.strftime('%Y:%m:%d 00:00:00')
                exif_dic['Exif'][36867] = start_date.strftime('%Y:%m:%d 00:00:00')
                exif_dic['Exif'][36868] = start_date.strftime('%Y:%m:%d 00:00:00')

                exif_bytes = piexif.dump(exif_dic)
                piexif.insert(exif_bytes, oldpath)
            except:
                print("-----------> DID NOT WORK FOR:", oldpath)

            # Construct new name
            time_tag = start_date.strftime('%Y%m%d')
            name_tag_new = time_tag + '_' + name_tag + '_' + str(counter)

            counter += 1

            newpath = os.path.join(_dir, '{}.{}'.format(name_tag_new, ext))
            print('---------\nOLD:\t{}\nNEW:\t{}'.format(oldpath, newpath))
            os.rename(oldpath, newpath)

            # change the MAC OS modified (and created time)                                                                                                                                              
            os.utime(newpath, (time.mktime(start_date.utctimetuple()),)*2)

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


def get_start_date():
    year = int(input('Enter a year (YYYY): '))
    month = int(input('Enter a month (MM): '))
    day = int(input('Enter a day (DD): '))
    hour = 0 #int(input('Enter an hour (hh): '))
    minute = 0 #int(input('Enter a minute (mm): '))
    return  datetime.datetime(year, month, day, hour, minute)

if __name__ == "__main__":

    start_date = get_start_date()

    _dir, name_tag = validate_user_inputs()
    rename_photos(_dir, name_tag, start_date)

    pass
