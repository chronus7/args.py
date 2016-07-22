#!/bin/env python3
# -*- coding:utf-8 -*-
"""Test usage of args.py
"""


def testfunc():
    """empty"""
    print("---")


def equal(a, b):
    """Tests both items on equality"""
    print(a == b)


def join(c: str, *a):
    """Joins the arguments with the first one"""
    print(c.join(a))


def add(*i: lambda x: list(map(float, x))):
    """Adds the given numbers"""
    from functools import reduce
    print(reduce(float.__add__, i, 0.0))


def echo(i: str):
    """echoes the given string
    :param i: the string to print
    """
    print(i)

if __name__ == '__main__':
    import args
    args.args()
