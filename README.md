# `args.py`

A small in-place argument-parser. Call it in your python file to easily provide
a commandline-interface to your functions.

## Features:

- easy usage: `import args; args.args()`
- cmd-interface to all functions of that module
    - no class support (for now)
- automatic usage-generation (`test.py -h`)
- parsing of arguments into the respective type (if annotated)
- `--list-commands` to retrieve a machine-readable list of all possible commands
- ignoring functions, starting with `_`

Check out `test.py` for examples and usage of this module.

----

> Dave J (https://github.com/chronus7)

<!--
vim: ft=markdown:tw=80
-->
