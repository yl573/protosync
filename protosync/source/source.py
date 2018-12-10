import pyrsync2
import os
from protosync.common import *
import fnmatch

MAX_FILE_SIZE_MB = 10
WARNING_SIZE_MB = 5


def get_ignore_filters(src_root):
    ignore_file = os.path.join(src_root, '.gitignore')
    if not os.path.isfile(ignore_file):
        return []

    with open(ignore_file, 'r') as f:
        text = f.read()
    ignore_filters = text.split('\n')
    for i, filter in enumerate(ignore_filters):
        if len(filter) > 0 and filter[-1] == '/':
            ignore_filters[i] = filter + '*'
    ignore_filters.append('.git/*')
    return ignore_filters


def filter_gitignore(tracked_files, src_root):
    ignore_filters = get_ignore_filters(src_root)
    for ignore in ignore_filters:
        tracked_files = [f for f in tracked_files if not fnmatch.fnmatch(f, ignore)]
    return tracked_files


def filter_large_files(tracked_files, src_root):
    filtered_files = []
    for sub_path in tracked_files:
        full_path = os.path.join(src_root, sub_path)
        file_size = os.path.getsize(full_path) / (1024 ** 2)
        if file_size > MAX_FILE_SIZE_MB:
            print('Ignoring file: {}, file exceeding {} Mb'.format(sub_path, MAX_FILE_SIZE_MB))
        else:
            filtered_files.append(sub_path)
    return filtered_files


def get_src_structure(src_root):
    structure = {}
    for path, subdirs, files in os.walk(src_root):
        for name in files:
            _, file_extension = os.path.splitext(name)
            file_path = os.path.join(path, name)
            sub_path = os.path.relpath(file_path, src_root)
            structure[sub_path] = 0

    tracked_files = list(structure.keys())
    tracked_files = filter_gitignore(tracked_files, src_root)
    tracked_files = filter_large_files(tracked_files, src_root)

    structure = {file: structure[file] for file in tracked_files}
    return structure


def compute_source_deltas(src_root, structured_hashes):
    structured_deltas = {}
    for path, hashes in structured_hashes.items():
        file_path = os.path.join(src_root, path)
        try:
            size = os.path.getsize(file_path) / (1024 ** 2)
            if size > WARNING_SIZE_MB:
                print('Large file: {} is {:.2f} Mb, this might take a while'.format(path, size))
            with open(file_path, 'rb') as patchedfile:
                delta = pyrsync2.rsyncdelta(patchedfile, hashes)
                structured_deltas[path] = [x for x in delta if isinstance(x, (bytes, bytearray))]
        except FileNotFoundError:
            pass
    return structured_deltas


def source_push_structure(pin, structure):
    save_temp_and_push(structure, '/source/push/structure', pin)


def source_fetch_hashes(pin):
    hashes = fetch_temp_and_load('/source/fetch/hashes', pin)
    hashes = list_dict_to_gen_dict(hashes)
    return hashes


def source_push_deltas(pin, deltas):
    save_temp_and_push(deltas, '/source/push/deltas', pin)


def source_check_acknowledge(pin):
    acknowledged = wait_pin_data(pin, '/source/wait/acknowledge')
    if not acknowledged:
        print('\nOops, Protosync can\'t find the remote server')
        print('Make sure you are running "protosync dest" on the remote server\n')
        exit()


def start_source_sync(src_root, pin, debug=False):
    if debug:
        pin = TEST_PIN
    structure = get_src_structure(src_root)
    source_push_structure(pin, structure)
    source_check_acknowledge(pin)
    hashes = source_fetch_hashes(pin)
    deltas = compute_source_deltas(src_root, hashes)
    source_push_deltas(pin, deltas)
    print('Code synced to remote directory')
