# -*- encoding: utf-8 -*-
"""
Helper methods
"""
import argparse
import getpass
import json
import math
import sys
from tabulate import tabulate

from ..consts import PER_PAGE
from ..libs.config import Config


#pylint: disable=broad-except
def user_input(text='', hide_input=False):
    """ Nice little function to read text inputs from stdin """
    try:
        if hide_input:
            inp = getpass.getpass(text)
        else:
            inp = input(text)
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception:
        inp = None
    return inp


def print_header(text=''):
    """ Pretty print header text """
    print('#' * (len(text) + 3))
    print(f' {text}')
    print('#' * (len(text) + 3))


def print_table(header=None, rows=None):
    """ Print tables in commandline """
    print(tabulate(rows, headers=header, tablefmt='grid'))


#pylint: disable=too-many-arguments
def print_result(fmt, rows=None, header=None, count=0, page=1, heading=False,
                 zero_result_msg='No results found for your query.'):
    """ Print result in format specified by user """
    if not fmt:
        fmt = 'table'
    if rows is None:
        rows = []
    if header is None:
        header = []

    if fmt == 'table':
        if count == 0:
            print(zero_result_msg)
        else:
            total_pages = int(((count - 1)/PER_PAGE) + 1)
            if heading:
                print_header(heading)
            else:
                print_header(f'Found {count} results. On page {page} of {total_pages}')
            print_table(header, rows)
    else:
        json_result = json.dumps([dict(zip(header, row)) for row in rows],
                                 indent=2, sort_keys=True)
        print(json_result)


def readable_memory_format(size):
    """ Converts int memory to formatted value """
    if size == 0:
        return '0B'
    size_name = ("KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size, 1024)))
    power = math.pow(1024, i)
    formatted_size = round(size/power, 2)
    return f'{formatted_size} {size_name[i]}'


#pylint: disable=too-few-public-methods
class CondAction(argparse.Action):
    """ A custom argparse action to support required arguments """
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        arg = kwargs.pop('to_be_required', [])
        super().__init__(option_strings, dest, **kwargs)
        self.make_required = arg

    #pylint: disable=inconsistent-return-statements
    def __call__(self, parser, namespace, values, option_string=None):
        if values in self.make_required:
            config = Config()
            options_required = self.make_required[values]
            for opt in options_required:
                if not config.get(opt.dest):
                    opt.required = True
        try:
            setattr(namespace, self.dest, values)
            return super().__call__(parser, namespace, values,
                                                    option_string)
        except NotImplementedError:
            pass
