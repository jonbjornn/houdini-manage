+++
title = 'Commandline'
ordering = 2
+++

> `houdini-manage [options] [hou]`

This document describes the **Houdini-manage** command-line interface.

It allows you to install, manage and remove [Houdini Libraries](library.md).
The *HOU* parameter will default to "houdini16.0", unless otherwise configured
in `~/.houdini-manage.ini`. If the argument is specified, it must be the name
of the Houdini user preferences folder or a full path to a Houdini environment
file.

### `--gui`

Start the Houdini Manage GUI.

### `--install`

*LIBRARY_PATH* is the path to the Houdini library. It must contain a valid
`houdini-library.json` file.

If specified, the *HOUDINI* argument must be either the path to a Houdini
environment file (`houdini.env`) or the name of the Houdini configuration
directory that contains such a file.

### `--remove`

Removes the Houdini library with the specified *LIBRARY_NAME*.

### `--version-of`

Prints the version of the library specified with *LIBRARY_NAME*. If the
library is not installed, an error will be printed to stderr and the exit
code will be 1.

### `--path-of`

Prints the path to the library specified with *LIBRARY_NAME*. If the library
is not installed, an error will be printed to stderr and the exit code will
be 1.

### `--list`

List all installed libraries.
