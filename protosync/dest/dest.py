import pyrsync2
import os
import requests
import time
import dill
from datetime import datetime
from termcolor import colored
from protosync.common import BASE_URL, gen_dict_to_list_dict


def compute_dest_hashes(dst_root, structure):
    structured_hashes = {}
    for path in structure:
        file_path = os.path.join(dst_root, path)
        dir_path = os.path.dirname(file_path)

        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        if not os.path.exists(file_path):
            with open(file_path, "w") as f:
                f.write('')

        unpatched = open(file_path, 'rb')
        hashes = pyrsync2.blockchecksums(unpatched)

        structured_hashes[path] = hashes
    return structured_hashes


def update_dst(dst_root, structured_deltas):
    for path, delta in structured_deltas.items():
        if delta != [0]:
            file_path = os.path.join(dst_root, path)
            time_str = datetime.now().strftime('%H:%M:%S')
            print('{}  File changed: {}'.format(time_str, file_path))
            unpatched = open(file_path, 'rb')
            unpatched.seek(0)
            save_to = open(file_path, 'wb')
            pyrsync2.patchstream(unpatched, save_to, delta)


def dest_fetch_structure(pin):
    has_response = False
    while not has_response:
        url = BASE_URL + '/dest/fetch/structure'
        data = dict(pin=str(pin))
        res = requests.post(url, data=data)
        has_response = res.status_code == 200
        time.sleep(0.1)
    filename = 'cache/{}_structure.pkl'.format(pin)
    with open(filename, 'wb') as f:
        f.write(res.content)

    can_read = False
    while not can_read:
        try:
            with open(filename, 'rb') as f:
                structure = dill.load(f)
                can_read = True
        except:
            can_read = False

    return structure


def dest_push_hashes(pin, hashes):
    hashes = gen_dict_to_list_dict(hashes)
    filename = 'cache/{}_hashes.pkl'.format(pin)
    with open(filename, 'wb') as f:
        dill.dump(hashes, f)

    files = {'file': open(filename, 'rb')}
    url = BASE_URL + '/dest/push/hashes'
    data = dict(pin=pin)
    requests.post(url, files=files, data=data)


def dest_fetch_deltas(pin):
    has_response = False
    while not has_response:
        url = BASE_URL + '/dest/fetch/deltas'
        data = dict(pin=str(pin))
        res = requests.post(url, data=data)
        has_response = res.status_code == 200
        time.sleep(0.1)
    filename = 'cache/{}_deltas.pkl'.format(pin)
    with open(filename, 'wb') as f:
        f.write(res.content)

    can_read = False
    while not can_read:
        try:
            with open(filename, 'rb') as f:
                deltas = dill.load(f)
                can_read = True
        except:
            can_read = False

    return deltas


def start_dest_sync(dest_root, pin):
    start = True
    while True:
        structure = dest_fetch_structure(pin)
        hashes = compute_dest_hashes(dest_root, structure)
        dest_push_hashes(pin, hashes)
        deltas = dest_fetch_deltas(pin)
        update_dst(dest_root, deltas)
        if start:
            print(colored('Syncing directory to source', 'yellow'))
            start = False
