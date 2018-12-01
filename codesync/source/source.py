import pyrsync2
import os
import dill
import requests
import time
from termcolor import colored
import uuid
from codesync.common import BASE_URL, list_dict_to_gen_dict, gen_dict_to_list_dict


def get_src_structure(src_root):
    structure = {}
    for path, subdirs, files in os.walk(src_root):
        for name in files:
            file_path = os.path.join(path, name)
            sub_path = file_path[len(src_root) + 1:]

            structure[sub_path] = None
    return structure


def compute_source_deltas(src_root, structured_hashes):
    structured_deltas = {}
    for path, hashes in structured_hashes.items():
        file_path = os.path.join(src_root, path)
        patchedfile = open(file_path, 'rb')
        delta = pyrsync2.rsyncdelta(patchedfile, hashes)
        structured_deltas[path] = delta
    return structured_deltas


def source_push_structure(pin, structure):
    filename = 'cache/{}_structure.pkl'.format(pin)
    with open(filename, 'wb') as f:
        dill.dump(structure, f)

    files = {'file': open(filename, 'rb')}
    url = BASE_URL + '/source/push/structure'
    data = dict(pin=pin)
    requests.post(url, files=files, data=data)


def source_fetch_hashes(pin):
    has_response = False
    while not has_response:
        url = BASE_URL + '/source/fetch/hashes'
        data = dict(pin=str(pin))
        res = requests.post(url, data=data)
        has_response = res.status_code == 200
        time.sleep(0.1)
    filename = 'cache/{}_hashes.pkl'.format(pin)
    with open(filename, 'wb') as f:
        f.write(res.content)

    can_read = False
    while not can_read:
        try:
            with open(filename, 'rb') as f:
                hashes = dill.load(f)
                can_read = True
        except:
            can_read = False

    hashes = list_dict_to_gen_dict(hashes)
    return hashes


def source_push_deltas(pin, deltas):
    filename = 'cache/{}_deltas.pkl'.format(pin)
    deltas = gen_dict_to_list_dict(deltas)
    with open(filename, 'wb') as f:
        dill.dump(deltas, f)

    files = {'file': open(filename, 'rb')}
    url = BASE_URL + '/source/push/deltas'
    data = dict(pin=pin)
    requests.post(url, files=files, data=data)


def start_source_sync(src_root, pin):
    if len(pin) == 0:
        pin = uuid.uuid4().hex
    print('\n\tRun in remote repository:')
    print('\t' + colored('codesync.py dest {}'.format(pin, src_root), 'yellow'))
    while True:
        structure = get_src_structure(src_root)
        source_push_structure(pin, structure)
        hashes = source_fetch_hashes(pin)
        deltas = compute_source_deltas(src_root, hashes)
        source_push_deltas(pin, deltas)
