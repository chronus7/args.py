#!/bin/env python3
# -*- coding:utf-8 -*-
"""Inplace argument-parsers/executor

Currently only works for positional arguments. Other
types than strings should be annotated correctly (callable).

- Dave J (https://github.com/chronus7)
"""
from sys import argv
from inspect import isfunction as _isfunction
from inspect import getfullargspec as _getargs
from inspect import stack as _getstack
from inspect import getmodule as _getmodule


__all__ = ["args"]


def commands(*, globalvars=globals()):
    """Lists all possible commands. Useful for bash-completion."""
    for i in sorted(globalvars):
        print(i)
    exit(0)


def usage(*, globalvars=globals()):
    """Prints this usage message and exits"""
    print("Usage: {} ...".format(argv[0]))

    if __doc__:
        print(__doc__.strip())

    print()

    fs = {}
    for k, v in globalvars.items():
        l = fs.setdefault(v, [])
        l.append(k)
        l.sort()    # TODO hmm...

    for func, cmds in sorted(fs.items(), key=lambda tpl: tpl[1][0]):
        specs = _getargs(func)
        variables = []
        for v in specs.args:
            vv = v
            if v in specs.annotations:
                vv += ":" + specs.annotations[v].__name__
            # TODO missing kw[only]args
            variables.append(vv)
        print(' | '.join(sorted(cmds)), ' '.join(variables))
        docs = func.__doc__
        if docs:
            docs = docs.strip()
        print("   ", docs)
    exit(0)


def args():
    """Parses the cmd-arguments to execute the requested command."""
    # getting arguments
    try:
        _, f, *a = argv
    except ValueError:
        raise Exception("Requires function or --help.")

    # get caller
    frame = _getstack()[1]
    module = _getmodule(frame[0])

    # getting functions
    funcs = {k: v for k, v in vars(module).items()
             if not k.startswith('_') and _isfunction(v)}
    funcs['--help'] = funcs['-h'] = funcs['help'] = usage
    funcs['--list-commands'] = commands
    if f not in funcs:
        raise Exception("Invalid function '{}'.".format(f))

    # getting this function
    ff = funcs[f]

    # converting arguments
    fspecs = _getargs(ff)
    for i, (val, name) in enumerate(zip(a, fspecs.args)):
        if name in fspecs.annotations:
            a[i] = fspecs.annotations[name](val)

    # executing
    if ff in {usage, commands}:
        ff(globalvars=funcs)
    else:
        ff(*a)

if __name__ == '__main__':
    args()
