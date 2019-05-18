# -*- encoding: utf-8 -*-
import argparse
import getpass
import json
import math
import sys
from tabulate import tabulate

from ..consts import PER_PAGE
from ..libs.config import Config

try:
    input = raw_input
except NameError:
    pass


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
    print(' %s' % text)
    print('#' * (len(text) + 3))


def print_table(header=[], rows=[]):
    """ Print tables in commandline """
    print(tabulate(rows, headers=header, tablefmt='grid'))


def print_result(format, rows=[], header=[], count=0, page=1, heading=False,
                 zeroResultMsg='No results found for your query.'):
    """ Print result in format specified by user """
    if not format:
        format = 'table'

    if format == 'table':
        if count == 0:
            print(zeroResultMsg)
        else:
            total_pages = int(((count - 1)/PER_PAGE) + 1)
            if heading:
                print_header(heading)
            else:
                print_header('Found %s results. On page %s of %s' %
                             (count, page, total_pages))
            print_table(header, rows)
    else:
        json_result = json.dumps([dict(zip(header, row)) for row in rows],
                                 indent=2, sort_keys=True)
        print(json_result)


def readableMemoryFormat(size):
    if (size == 0):
        return '0B'
    size_name = ("KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size, 1024)))
    p = math.pow(1024, i)
    s = round(size/p, 2)
    return '%s %s' % (s, size_name[i])


class CondAction(argparse.Action):
    """ A custom argparse action to support required arguments """
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        x = kwargs.pop('to_be_required', [])
        super(CondAction, self).__init__(option_strings, dest, **kwargs)
        self.make_required = x

    def __call__(self, parser, namespace, values, option_string=None):
        if values in self.make_required:
            config = Config()
            options_required = self.make_required[values]
            for x in options_required:
                if not config.get(x.dest):
                    x.required = True
        try:
            setattr(namespace, self.dest, values)
            return super(CondAction, self).__call__(parser, namespace, values,
                                                    option_string)
        except NotImplementedError:
            pass
