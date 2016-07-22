#!/bin/env python3
# -*- coding:utf-8 -*-
"""Inplace argument-parsers/executor

Currently only works for positional arguments. Other
types than strings should be annotated correctly (callable).

- Dave J (https://github.com/chronus7)
"""
from sys import argv
from shlex import split as _split
from inspect import isfunction as _isfunction
from inspect import getfullargspec as _getargs
from inspect import stack as _getstack
from inspect import getmodule as _getmodule


__all__ = ["args"]


def _get_calling_module():
    # TODO test/check whether this always works!
    return _getmodule(_getstack()[-1][0])


def commands(*, globalvars=globals()):
    """Lists all possible commands. Useful for bash-completion."""
    for i in sorted(globalvars):
        print(i)
    exit(0)


def usage(*, globalvars=globals()):
    """Prints this usage message and exits"""
    print("Usage: {} <command> [arguments]".format(argv[0]))

    doc = _get_calling_module().__doc__
    if doc:
        print(doc.strip())

    print("\nCommands:")

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


def args(arguments: _split=argv[1:]):
    """Parses the cmd-arguments to execute the requested command."""
    # getting arguments
    try:
        f, *a = arguments
    except ValueError:
        raise Exception("Requires function or --help.")

    # get caller
    module = _get_calling_module()

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
    if fspecs.varargs:
        l = len(fspecs.args)
        vals = a[l:]
        if fspecs.varargs in fspecs.annotations:
            a[l:] = fspecs.annotations[fspecs.varargs](vals)

    # executing
    if ff in {usage, commands}:
        ff(globalvars=funcs)
    else:
        return ff(*a)

if __name__ == '__main__':
    args()
