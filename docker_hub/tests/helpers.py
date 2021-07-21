from ..libs.utils import readableMemoryFormat


def generate_results(count=1):
    r = []

    for d in range(0, count):
        o = {
            'last_updated': '2018-12-12 14:40',
            'name': '1.4.2-alpine-{0}'.format(d + 1),
            'full_size': 15820065 + d
        }
        r.append(o)

    return r


def convert_key_to_result_format(result_arr=[], result_key_map={}):
    r = []

    for d in result_arr:
        o = {}
        for k in d:
            if k == 'full_size':
                # Convert full_size in bytes to KB
                size_in_kb = d[k] / 1024
                d[k] = readableMemoryFormat(size_in_kb)
            if result_key_map[k]:
                o[result_key_map[k]] = d[k]
            else:
                o[k] = d[k]
        r.append(o)

    return r
