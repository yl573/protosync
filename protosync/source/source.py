import pyrsync2
import os
from protosync.common import *
from gitignore_parser import parse_gitignore
from queue import Queue

MAX_FILE_SIZE_MB = 5
WARNING_SIZE_MB = 3


def get_src_structure(src_root):
    ignore_file = os.path.join(src_root, '.gitignore')
    if not os.path.isfile(ignore_file):
        ignore = None
    else:
        ignore = parse_gitignore(ignore_file)

    structure = {}
    directories = Queue()
    directories.put(src_root)
    while not directories.empty():
        dir_path = directories.get()
        items = os.listdir(dir_path)
        for item in items:
            full_path = os.path.join(dir_path, item)
            rel_path = os.path.relpath(full_path, src_root)

            # check if item in .gitignore
            if ignore and ignore(full_path):
                continue

            # check if item is directory
            if os.path.isdir(full_path):
                directories.put(full_path)
                continue

            # check if file is too big
            file_size = os.path.getsize(full_path) / (1024 ** 2)
            if file_size > MAX_FILE_SIZE_MB:
                print('Ignoring file: {}, file exceeding {} Mb'.format(rel_path, MAX_FILE_SIZE_MB))
                continue

            else:
                structure[rel_path] = 0

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
        print('Try re-running "protosync dest" on the remote server\n')
        exit()


def print_report(deltas):
    count = 0
    for file, delta in deltas.items():
        if len(delta) > 0 and delta != [0]:
            print('File synced: {}'.format(file))
            count += 1
    print('Total synced: {} files'.format(count))


def start_source_sync(src_root, pin, debug=False):
    if debug:
        pin = TEST_PIN
    structure = get_src_structure(src_root)
    source_push_structure(pin, structure)
    source_check_acknowledge(pin)
    hashes = source_fetch_hashes(pin)
    deltas = compute_source_deltas(src_root, hashes)
    source_push_deltas(pin, deltas)
    print_report(deltas)
