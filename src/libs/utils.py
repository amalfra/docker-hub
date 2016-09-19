# -*- encoding: utf-8 -*-
import sys
from tabulate import tabulate


def user_input(text=''):
    try:
        inp = raw_input(text)
    except KeyboardInterrupt:
        sys.exit(0)
    except:
        inp = None
    return inp


def print_header(text=''):
    print '#' * (len(text) + 3)
    print ' %s' % text
    print '#' * (len(text) + 3)


def print_table(header=[], rows=[]):
    print tabulate(rows, headers=header, tablefmt='grid')
