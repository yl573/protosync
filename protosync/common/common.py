import tempfile
import dill
import requests
import time

BASE_URL = 'http://ec2-18-130-174-127.eu-west-2.compute.amazonaws.com'
FETCH_TIMEOUT = 3

# BASE_URL = 'http://0.0.0.0:5000'


def gen_dict_to_list_dict(gen_dict):
    for key, val in gen_dict.items():
        gen_dict[key] = [x for x in val]
    return gen_dict


def list_dict_to_gen_dict(list_dict):
    for key, val in list_dict.items():
        list_dict[key] = (x for x in val)
    return list_dict


def save_temp_and_push(data, endpoint, pin):
    with tempfile.TemporaryFile() as fp:
        dill.dump(data, fp)
        fp.seek(0)
        files = {'file': fp}
        url = BASE_URL + endpoint
        data = dict(pin=pin)
        requests.post(url, files=files, data=data)


def fetch_temp_and_load(endpoint, pin, timeout=False):
    has_response = False
    t0 = time.time()
    while not has_response:
        url = BASE_URL + endpoint
        data = dict(pin=str(pin))
        res = requests.post(url, data=data)
        has_response = res.status_code == 200
        time.sleep(0.1)
        if timeout and time.time() - t0 > FETCH_TIMEOUT:
            return None

    with tempfile.TemporaryFile() as fp:

        fp.write(res.content)
        can_read = False
        while not can_read:
            try:
                fp.seek(0)
                data = dill.load(fp)
                can_read = True
            except Exception as e:
                print(e)
                can_read = False
    return data
