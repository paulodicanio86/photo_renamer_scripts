# Various scripts to help rename photos
For photos ending in ```.jpg``` or ```.jpeg``` taken with a phone or camera with Exif date and time stamps.
Set up a virtual environment with the ```requirements.txt``` file. 

### photo_renamer.py
A script to rename photos according to their capture date and name defined by the user. Run like:

```
python photo_renamer.py /some/path/to/folder name
```
The outcome for a single jpg file could be:
```
20200228-160309-London.jpg
```

### photo_renamer_date_shift.py
Like the ```photo_renamer.py```	but for	photo files wrong Exif data (but whose timestamps are correct relative to each other). The user will input the year, month and day of the earliest photo taken in time, and then calculate the time delta of every other photo to this, and thus shift to the correct date and time.  

```
python photo_renamer_date_shift.py /some/path/to/folder name
```
The outcome for a single jpg file could be:
```
20200228-160309-New_York.jpg

### photo_renamer_set_date_and_counter.py
Like the ```photo_renamer.py``` but for photo files with no or wrong Exif data. You will be prompted to enter a year, month and day. It will then give each photo that date and simply append an integer counter to the end of the new filename.

```
python photo_renamer_set_date_and_counter.py /some/path/to/folder name
```
The outcome for a single jpg file could be:
```
20200228-160309-Tokyo_1.jpg
```
