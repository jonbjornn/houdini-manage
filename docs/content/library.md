+++
title = "Houdini Libraries"
ordering-priority = 5
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

    {
      "libraryName": "MY_LIBRARY_NAME",
      "libraryVersion": "1.6.0",
      "environment": [
        "# This line will be inserted into the Houdini environment file."
      ]
    }

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
