## houdini-manage

![MIT licensed](https://img.shields.io/badge/License-MIT-yellow.svg)

Houdini-Manage is a PyQt5 application that allows you to install libraries of
Houdini digital assets, native plugins, toolbars, python modules and VEX
headers by linking them into your Houdini environment.

![](https://i.imgur.com/jKjXCdB.png)

### Features

* Keep your Houdini preferences directory clean, Hoduini-Manage will only
  modify your `houdini.env` file
* Automatically builds DSOs when installing a library

### Library Structure

A Houdini library is a directory with several subdirectories that Houdini uses
as search paths for different components. Examples of these subdirectories are
`icons/`, `otls/`, `python/`, `toolbar/`, `vex/include/` and `dso/`.

In order to be installable by Houdini-Manager, you need to create a
`houdini-library.json` file that specifies at least a `"libraryName"` and
`"libraryVersion"`. Additional supported fields are listed below.

```json
{
  "libraryName": "NR_HOUDINI_LIBRARY",
  "libraryVersion": "1.0.0",
  "environment": [
    "SOME_ENVIRONMENT_VARIABLE=value"
  ],
  "dsoDebug": true
}
```

Available configuration values:

* **libraryName**: The name of the library. Must be unique. (required)
* **libraryVersion**: The version of the library. (required)
* **environment**: A list of environment variables that are added to your
  `houdini.env` file when the library is installed. (optional)
* **dsoDebug**: Set to `true` to build DSOs of your library in debug mode.
* **dsoInclude**:
* **dsoLibdir**:
* **dsoLibs**:
* **dsoSource**: The directory where the DSO source files are searched for.
  Defaults to `dso_source/`.

### Installation

  [get-pip.py]: https://bootstrap.pypa.io/get-pip.py

Make sure you have Python 3.3+ and Pip installed on your system. If you don't
have Pip installed (try `pip` in the terminal), you can use the [get-pip.py]
script to install it. Then you can install *houdini-manage* from the GitHub
repository.

    $ python get-pip.py
    $ pip install git+https://github.com/NiklasRosenstein/houdini-manage.git
    $ houdini-manage --version
    0.0.3
    $ houdini-manage --gui

> **macOS**: If you did not install Python via Homebrew, you need to add
> use `sudo <command>`.  
> **Windows**: Depending on where you chose to install Python, you might need
> an Administrator console on Windows.
