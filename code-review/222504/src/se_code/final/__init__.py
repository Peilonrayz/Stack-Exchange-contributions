#!/usr/bin/python3

import sys
import zlib
import os
import hashlib
import imghdr
import pathlib

'''
1. Make file things
2. Build cross-reference tables.
3. Take all the matching hashes from the source and target.
    if hashes match, check if hardlink between source and target
    if not hardlink, make hardlink


TODO?: Can use WSL/bash to do a reliable file type check - using the file command.
'''

source_dir = r'C:\!The Gallery'
target_dir = r'C:\Games\PnP DnD'
only_these_extensions = {'.jpg', '.png', '.gif', '.jpeg', '.bmp', '.tif', '.tiff', '.webp'}


def get_dir_contents(path, extensions, followlinks=True):
    for dir_path, _, file_names in os.walk(path, followlinks=followlinks):
        dir_path = pathlib.Path(dir_path)
        for file_name in file_names:
            full_path = dir_path / file_name
            if full_path.suffix in extensions:
                yield full_path

map()
# Define a main() function that prints a little greeting.
def main():

    print('Finding files: ', end='')
    source_files = list(get_dir_contents(source_dir, only_these_extensions))
    target_files = list(get_dir_contents(target_dir, only_these_extensions))
    print('Done')
    print('Collected ' + str(len(target_files) + len(source_files)) + ' files.')

    file_things = make_file_things(target_files + source_files)

    (hash_table, node_table, name_table) = build_tables(file_things)
    print(len(hash_table))
    print(len(node_table))
    print(len(name_table))

    # Hardlink from target to source
    for thing in file_things:
        # Take all the target files
        if os.path.commonpath([target_dir, os.path.split(thing.fpath)[0]]) != '':
            target_thing = thing
            if len(hash_table[thing.fhash]) > 1:
                # Get all hash matches that matched more than one file.
                for hash_matched_thing in hash_table[thing.fhash]:
                    # Get any matches in the source dir.
                    if os.path.commonpath([source_dir, os.path.split(hash_matched_thing.fpath)[0]]) != '':
                        source_thing = hash_matched_thing
                        # Unlink target and link from source
                        os.unlink(target_thing.fpath)
                        os.link(source_thing.fpath, target_thing.fpath)


def make_file_things(file_paths):
    file_things = []
    for file_path in file_paths:
        progress('Reading files', len(file_things), len(file_paths), 1)
        with open(file_path, "rb") as file:
            content = file.read()
            digest = crc32(content)
            file_things.append(file_thing(file_path, os.stat(file_path), digest))
    return file_things


def build_tables(files):
    hash_table = {}
    node_table = {}
    name_table = {}

    print('Building reference tables:', end='')
    for file in files:
        hashy = file.fhash
        inode = file.fstat.st_ino
        name = os.path.split(file.fpath)[1]

        if hashy in hash_table:
            hash_table[hashy] = file
        else:
            hash_table[hashy] = [file]

        if inode in node_table:
            node_table[inode] = file
        else:
            node_table[inode] = [file]

        if name in name_table:
            name_table[name] = file
        else:
            name_table[name] = [file]

    print(' Done!')
    return (hash_table, node_table, name_table)



#################################################
# Helpers
#################################################
class file_thing:
    fpath = ''
    fstat = 0
    fhash = 0

    def __init__(self, fpath, fstat, fhash):
        self.fstat = fstat
        self.fpath = fpath
        self.fhash = fhash

    def __str__(self):
        return str([self.fpath, self.fhash, self.fstat])

    def __repr__(self):
        return str([self.fpath, self.fhash, self.fstat])


def enum_hardlinks(dupe_files):
    # Expects all files given to be duplicates
    hardlink_sets = {}
    for dupe in dupe_files:
        # Inode on unix, file index on windows.
        file_index = os.stat(dupe).st_ino
        if file_index in hardlink_sets:
            hardlink_sets[file_index].append(dupe)
        else:
            hardlink_sets[file_index] = [dupe]
    return hardlink_sets


# The old version, before I knew about st_ino
def enum_hardlinks2(dupe_files):  # Expects all files given to be duplicates
    hardlink_sets = []
    for dupe in dupe_files:
        done = False
        hardlink_num = os.stat(dupe).st_nlink
        if (hardlink_num > 1):
            for hl_set in hardlink_sets:
                if (os.path.samefile(hl_set[0], dupe)):
                    hl_set.append(dupe)
                    done = True
                    break
        if (not done):
            hardlink_sets.append([dupe])
    return hardlink_sets


def enum_extensions(files, exclude_extensions=None):
    ext_set = set()
    for file in files:
        ext = get_ext(file)
        if (exclude_extensions is None or ext not in exclude_extensions):
            ext_set.add(ext)
    return ext_set


def group_by_extension(files, exclude_extensions=None):
    ext_dict = {}
    for file in files:
        ext = get_ext(file)
        if (exclude_extensions is None or ext not in exclude_extensions):
            if (ext in ext_dict):
                ext_dict[ext].append(file)
            else:
                ext_dict[ext] = [file]
    return ext_dict


# Fails in ~8% of cases. Meh.
def unreliable_filetype_check(files):
    type_dict = {}
    mismatches = []
    for file in files:
        ext = get_ext(file)
        img_type = imghdr.what(file)
        if (ext == 'jpg'):
            ext = 'jpeg'
        if (ext == 'tif'):
            ext = 'tiff'

        if (img_type is not None and ext != img_type):
            mismatches.append(file)
            print(ext + ' vs ' + img_type)
        if (img_type in type_dict):
            type_dict[img_type].append(file)
        else:
            type_dict[img_type] = [file]
    print(str(len(type_dict[None])) + ' images whose type could not be determined.')
    print(type_dict[None])
    return mismatches


def crc32(data):
    return hex(zlib.crc32(data) & 0xffffffff)


def sha265(data):
    return hashlib.sha256(data).hexdigest()


def get_ext(file):
    return os.path.splitext(file)[1][1:].lower()


def progress(prefix, current, total, step=1):
    '''
    The point is to only print when we are very close to a value we want. But we can't guarantee equality,
    so we have to use some kind of range around which we trigger the print. The upper bound for this range
    is 1/total, half below and half above our real value. There's edge cases where we end up with 2
    consecutive values within our range, but those are rare. Basically on odd numbered items, around 50%,
    when we have enough precision to accurately represent both ends of the range.
    '''
    temp = current / total * (100/step)
    delta = 1 / total * (50/step)  # Half above and below each target value, for a total range of 1/total
    if abs(temp - round(temp)) > delta and current != total-1:
        return
    temp = temp*step  # Mult by step again to get back to a scale of 100
    # Random edge case where both the nearest below and above values end up in our target range
    if (round(temp) == 50 and temp - round(temp) < 0):
        return
    if env == 'sub':
        if current == 0:
            print(prefix + ': ' + '{:2.0f}'.format(temp) + '%', end='')
        elif current == (total-1):
            print(' ' + '{:2.0f}'.format(temp) + '%')
        else:
            print(' ' + '{:2.0f}'.format(temp) + '%', end='')
        sys.stdout.flush()
    elif env == 'cli':
        if round(temp) > progress:
            print('Processing: ' + '{:2.0f}'.format(temp) + '%', end='\r')
            progress = round(temp)


# This is the standard boilerplate that calls the main() function.
env = ''
if __name__ == '__main__':
  if (sys.version_info[0] < 3):
    raise Exception('Your frickin python version is so very WROOOOOOOONG')
  try:
    os.environ['PYTHONSUBLIMEBUILDSYSTEM'] #If this exists, we're in our custom build sublime environment. Plz don't try to ask for input here.
    env = 'sub'
  except:
    env = 'cli'
  main()
