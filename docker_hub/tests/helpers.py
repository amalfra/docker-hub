# -*- encoding: utf-8 -*-
"""
Test helper methods
"""
from ..libs.utils import readable_memory_format


def generate_results(count=1):
    """ This generates fake API results """
    resp = []

    for itr in range(0, count):
        output = {
            'last_updated': '2018-12-12 14:40',
            'name': f'1.4.2-alpine-{itr + 1}',
            'full_size': 15820065 + itr
        }
        resp.append(output)

    return resp


def convert_key_to_result_format(result_arr=None, result_key_map=None):
    """ This converted response to correct display format """
    resp = []

    for itr in result_arr:
        output = {}
        for k in itr:
            if k == 'full_size':
                # Convert full_size in bytes to KB
                size_in_kb = itr[k] / 1024
                itr[k] = readable_memory_format(size_in_kb)
            if result_key_map[k]:
                output[result_key_map[k]] = itr[k]
            else:
                output[k] = itr[k]
        resp.append(output)

    return resp
