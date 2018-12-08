import tempfile
import dill
import requests
import time

BASE_URL = 'http://ec2-18-130-174-127.eu-west-2.compute.amazonaws.com'
FETCH_TIMEOUT = 3


def time_function(name):
    def name_time_function(func):
        def timed_func(*args, **kwargs):
            t0 = time.time()
            result = func(*args, **kwargs)
            print('Function {} took {}'.format(name, time.time() - t0))
            return result
        return timed_func
    return name_time_function


def set_debug():
    global BASE_URL
    BASE_URL = 'http://0.0.0.0:5000'


def gen_dict_to_list_dict(gen_dict):
    for key, val in gen_dict.items():
        gen_dict[key] = [x for x in val]
    return gen_dict


def list_dict_to_gen_dict(list_dict):
    for key, val in list_dict.items():
        list_dict[key] = (x for x in val)
    return list_dict


def send_pin_data(pin, endpoint):
    url = BASE_URL + endpoint
    data = dict(pin=pin)
    requests.post(url, data=data)


def wait_pin_data(pin, endpoint):
    t0 = time.time()
    while time.time() - t0 < FETCH_TIMEOUT:
        url = BASE_URL + endpoint
        data = dict(pin=str(pin))
        res = requests.post(url, data=data)
        if res.status_code == 200:
            return True
        print(res.status_code)
        time.sleep(0.2)
    return False


def save_temp_and_push(data, endpoint, pin):
    with tempfile.TemporaryFile() as fp:
        dill.dump(data, fp)
        fp.seek(0)
        files = {'file': fp}
        url = BASE_URL + endpoint
        data = dict(pin=pin)
        requests.post(url, files=files, data=data)


def fetch_temp_and_load(endpoint, pin):
    has_response = False
    while not has_response:
        url = BASE_URL + endpoint
        data = dict(pin=str(pin))
        res = requests.post(url, data=data)
        has_response = res.status_code == 200

    with tempfile.TemporaryFile() as fp:

        fp.write(res.content)
        can_read = False
        while not can_read:
            try:
                fp.seek(0)
                data = dill.load(fp)
                can_read = True
            except Exception as e:
                can_read = False
    return data
