+++
title = "Commandline"
+++

This document describes the **Houdini-manage** command-line interface.

## `library`

```
houdini-manage library [OPTIONS] [HOU]
```

Install, manage and remove [Houdini Libraries](library.md).


### `--install`

*LIBRARY_PATH* is the path to the Houdini library. It must contain a valid
`houdini-library.json` file.

If specified, the *HOUDINI* argument must be either the path to a Houdini
environment file (`houdini.env`) or the name of the Houdini configuration
directory that contains such a file. The default value for this argument
is defined in the **Houdini-manage** configuration file in your user home
directory (`~/.houdini-manage.ini`) and defaults to "houdini16.0".

### `--remove`

Removes the Houdini library with the specified *LIBRARY_NAME*.

### `--version-of`

Prints the version of the library specified with *LIBRARY_NAME*. If the
library is not installed, an error will be printed to stderr and the exit
code will be 1.

### `--list`

List all installed libraries.
