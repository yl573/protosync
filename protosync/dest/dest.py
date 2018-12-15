import pyrsync2
import os
from datetime import datetime
from protosync.common import *


def time_str():
    return datetime.now().strftime('%H:%M:%S')


@time_function('hashes')
def compute_dest_hashes(dst_root, structure):
    structured_hashes = {}
    for path in structure:
        file_path = os.path.join(dst_root, path)
        dir_path = os.path.dirname(file_path)

        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                pass

        with open(file_path, 'rb') as f:
            hashes = pyrsync2.blockchecksums(f)
            structured_hashes[path] = [x for x in hashes]
    return structured_hashes


@time_function('update')
def update_dst(dst_root, structured_deltas):
    structured_deltas = gen_dict_to_list_dict(structured_deltas)
    for path, delta in structured_deltas.items():
        if len(delta) > 0 and delta != [0]:
            file_path = os.path.join(dst_root, path)
            with open(file_path, 'rb') as unpatched:
                unpatched.seek(0)
                with open(file_path, 'wb') as save_to:
                    pyrsync2.patchstream(unpatched, save_to, delta)


def dest_fetch_structure(pin):
    structure = fetch_temp_and_load('/dest/fetch/structure', pin)
    return structure


def dest_push_hashes(pin, hashes):
    hashes = gen_dict_to_list_dict(hashes)
    save_temp_and_push(hashes, '/dest/push/hashes', pin)


def dest_fetch_deltas(pin):
    deltas = fetch_temp_and_load('/dest/fetch/deltas', pin)
    deltas = list_dict_to_gen_dict(deltas)
    return deltas


def dest_send_acknowledge(pin):
    send_pin_data(pin, '/dest/send/acknowledge')


def start_dest_sync(dest_root, debug=False):
    if debug:
        pin = GLOBALS.TEST_PIN
    else:
        pin = Fernet.generate_key()
        pin = pin.decode()

    print('Protosync started')
    print('To sync, run in local directory:')
    print('\nprotosync source {}'.format(pin))
    while True:
        structure = dest_fetch_structure(pin)
        dest_send_acknowledge(pin)
        hashes = compute_dest_hashes(dest_root, structure)
        dest_push_hashes(pin, hashes)
        deltas = dest_fetch_deltas(pin)
        update_dst(dest_root, deltas)
        dest_send_acknowledge(pin)
        time.sleep(0.5)
