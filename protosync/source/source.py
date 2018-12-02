import pyrsync2
import os
from termcolor import colored
import uuid
from protosync.common import list_dict_to_gen_dict, save_temp_and_push, fetch_temp_and_load, gen_dict_to_list_dict


def get_src_structure(src_root):
    structure = {}
    for path, subdirs, files in os.walk(src_root):
        for name in files:
            file_path = os.path.join(path, name)
            sub_path = file_path[len(src_root) + 1:]

            structure[sub_path] = 0
    return structure


def compute_source_deltas(src_root, structured_hashes):
    structured_deltas = {}
    for path, hashes in structured_hashes.items():
        file_path = os.path.join(src_root, path)
        with open(file_path, 'rb') as patchedfile:
            delta = pyrsync2.rsyncdelta(patchedfile, hashes)
        structured_deltas[path] = delta
    return structured_deltas


def source_push_structure(pin, structure):
    save_temp_and_push(structure, '/source/push/structure', pin)


def source_fetch_hashes(pin):
    hashes = fetch_temp_and_load('/source/fetch/hashes', pin)
    hashes = list_dict_to_gen_dict(hashes)
    return hashes


def source_push_deltas(pin, deltas):
    deltas = gen_dict_to_list_dict(deltas)
    save_temp_and_push(deltas, '/source/push/deltas', pin)


def start_source_sync(src_root, pin):
    if len(pin) == 0:
        pin = uuid.uuid4().hex
    print('\n\tRun in remote repository:')
    print('\t' + colored('protosync dest {}'.format(pin, src_root), 'yellow'))
    while True:
        structure = get_src_structure(src_root)
        source_push_structure(pin, structure)
        hashes = source_fetch_hashes(pin)
        deltas = compute_source_deltas(src_root, hashes)
        source_push_deltas(pin, deltas)
