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
- allowing arguments to be passed via stdin
- works even with `pdb`

Check out `test.py` for examples and usage of this module.

## Known Issues:

- `pdb` finishes with `ValueError: I/O operation on closed file.` when calling
  `-h` or `--list-commands`.
- import not working as intended in all situations (probably name clashes)
- no setup.py

----

> Dave J (https://github.com/chronus7)

<!--
vim: ft=markdown:tw=80
-->
