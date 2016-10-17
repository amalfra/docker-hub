# -*- encoding: utf-8 -*-
import sys
import argparse
import math
from tabulate import tabulate
from ..consts import PER_PAGE

try:
    input = raw_input
except NameError:
    pass


def user_input(text=''):
    """ Nice little function to read text inputs from stdin """
    try:
        inp = input(text)
    except KeyboardInterrupt:
        sys.exit(0)
    except:
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


def print_result(format, count=0, page=1, rows=[], header=[]):
    """ Print result in format specified by user """
    if not format:
        format = 'table'

    if format == 'table':
        total_pages = int(((count - 1)/PER_PAGE) + 1)
        print_header('Found %s results. On page %s of %s' %
                     (count, page, total_pages))
        print_table(header, rows)
    else:
        json_result = []
        for row in rows:
            json_dict = {}
            json_dict = dict(zip(header, row))
            json_result.append(json_dict)
        print(json_result)


class CondAction(argparse.Action):
    """ A custom argparse action to support required arguments """
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        x = kwargs.pop('to_be_required', [])
        super(CondAction, self).__init__(option_strings, dest, **kwargs)
        self.make_required = x

    def __call__(self, parser, namespace, values, option_string=None):
        for x in self.make_required:
            x.required = True
        try:
            setattr(namespace, self.dest, values)
            return super(CondAction, self).__call__(parser, namespace, values,
                                                    option_string)
        except NotImplementedError:
            pass
