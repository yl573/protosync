import pyrsync2
import os
from termcolor import colored
from protosync.common import list_dict_to_gen_dict, save_temp_and_push, fetch_temp_and_load, gen_dict_to_list_dict
import fnmatch
import time


def get_ignore_filters(src_root):
    ignore_file = os.path.join(src_root, '.gitignore')
    if os.path.isfile(ignore_file):
        with open(ignore_file, 'r') as f:
            text = f.read()
        ignore_filters = text.split('\n')
    for i, filter in enumerate(ignore_filters):
        if len(filter) > 0 and filter[-1] == '/':
            ignore_filters[i] = filter + '*'
    ignore_filters.append('.git/*')
    return ignore_filters


def get_src_structure(src_root):
    structure = {}
    for path, subdirs, files in os.walk(src_root):
        for name in files:
            _, file_extension = os.path.splitext(name)

            file_path = os.path.join(path, name)
            sub_path = file_path[len(src_root) + 1:]
            structure[sub_path] = 0

    ignore_filters = get_ignore_filters(src_root)
    tracked_files = list(structure.keys())

    for ignore in ignore_filters:
        tracked_files = [f for f in tracked_files if not fnmatch.fnmatch(f, ignore)]

    structure = {file: structure[file] for file in tracked_files}
    return structure


def compute_source_deltas(src_root, structured_hashes):
    structured_deltas = {}
    for path, hashes in structured_hashes.items():
        file_path = os.path.join(src_root, path)
        try:
            with open(file_path, 'rb') as patchedfile:
                delta = pyrsync2.rsyncdelta(patchedfile, hashes)
                structured_deltas[path] = [x for x in delta if isinstance(x, (bytes, bytearray))]
        except FileNotFoundError:
            pass
    return structured_deltas


def source_push_structure(pin, structure):
    save_temp_and_push(structure, '/source/push/structure', pin)


def source_fetch_hashes(pin):
    hashes = fetch_temp_and_load('/source/fetch/hashes', pin, timeout=True)
    if hashes is None:
        print('\nOops, Protosync can\'t find the remote server')
        print('Make sure you are running "protosync dest" on the remote server\n')
        exit()
    hashes = list_dict_to_gen_dict(hashes)
    return hashes


def source_push_deltas(pin, deltas):
    save_temp_and_push(deltas, '/source/push/deltas', pin)


def start_source_sync(src_root, pin):
    structure = get_src_structure(src_root)
    source_push_structure(pin, structure)
    hashes = source_fetch_hashes(pin)
    deltas = compute_source_deltas(src_root, hashes)
    source_push_deltas(pin, deltas)
    print('Code synced to remote directory')
