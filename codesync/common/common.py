
BASE_URL = 'http://ec2-18-130-174-127.eu-west-2.compute.amazonaws.com'


def gen_dict_to_list_dict(gen_dict):
    for key, val in gen_dict.items():
        gen_dict[key] = [x for x in val]
    return gen_dict

def list_dict_to_gen_dict(gen_dict):
    for key, val in gen_dict.items():
        gen_dict[key] = (x for x in val)
    return gen_dict