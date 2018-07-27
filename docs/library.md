+++
title = 'Library Specification'
+++

**Houdini-manage** allows you to install libraries that contain Houdini
digital assets and shelf tools simply by managing your Houdini environment
variables in a clever way.

Libraries can be installed, managed or removed from the command-line using
the [`library`](../cli/#library) command.

## Library Structure

We define a Houdini library as any directory with the appropriate structure
and a valid `houdini-library.json` configuration file. The configuration file
will be used to determine the installation parameters for the library.
Different content types must be in separate directories, as shown below.

    houdini-library.json
    vop/
    otls/
    scripts/
    desktop/
    dso/
    geo/
    python_panels/
    python/
    pic/
    toolbar/
    radialmenu/
    vex/
    glsl/
    ocl/

## Configuration

__Example__

```json
{
  "libraryName": "MY_LIBRARY_NAME",
  "libraryVersion": "1.6.0",
  "environment": [
    "SOME_ENVIRONMENT_VARIABLE=value"
  ],
  "dsoDebug": true
}
```

#### libraryName

Must be a valid environment variable identifier. This library name is used
to keep track of sections in the Houdini environment file to allow installing,
updating and uninstalling libraries. Additionally, the following environment
variables will be affected by this parameter:

* `HLIB_INSTALLED`: A list of the names of libraries that are installed.
* `HLIBPATH_$libraryName`: The path to the library. This is used mostly
  by shelf tools to reference an icon from the `icons/` directory, for example:
  `$HLIBPATH_MY_LIBRARY_NAME/icons/myshelftool.png`
* `HLIBVERSION_$libraryName`: The version of the library.

#### libraryVersion

The version number of the library.

#### environment

A list of strings that will be added to the environment file.

### dsoDebug

Set to `true` to build DSOs in debug mode when the library is installed.

### dsoInclude

A list of paths that will be added to the compiler include directories.

### dsoLibdir

A list of paths that will be added to the compiler library directories.

### dsoLibs

A list of library names that will be linked with your DSO.

### dsoSource

The directory where the DSO source files are searched for and compiled from
Defaults to `dso_source/`.
