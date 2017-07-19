+++
title = "Home"
render-title = false
ordering-priority = 10
+++

# HoudiniLibrary

<a href="https://opensource.org/licenses/MIT">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" align="right">
</a>
&mdash; Install & manage external Houdini libraries, and keep them external.

HoudiniLibrary is a command-line tool to install [Houdini libraries][1] simply by
managing your Houdini environment file. Example:

    $ houdini-manage library --list
    * NR_HOULIB v1.0.0 (C:\Users\niklas\repos\houdini-library)
    $ houdini-manage library --remove NR_HOULIB
    library "NR_HOULIB" removed
    $ houdini-manage library --install ../houdini-library/
    library "NR_HOULIB" installed
    $ houdini-manage library --install ../houdini-library/
    error: previous installation found. pass --overwrite to proceed
    $ houdini-manage library --version-of NR_HOULIB
    1.0.0

[1]: library/
