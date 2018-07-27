+++
title = 'Changelog'
ordering = 4
+++

## v1.0.0 (2018-07-27)

- Show information dialog after DSOs have been rebuilt.
- Distributions now provide a `houdini-manage-gui` entrypoint that hides the
  console and `houdini-manage` doesn't.
- Fix "Remove" button
- Update documentation

## v0.0.3

- Remove `houdini-manage gui` subcommand, add it as `--gui` option instead
- Buildable with [nr.pybundle](https://gitlab.niklasrosenstein.com/NiklasRosenstein/python/nr.pybundle)
- Add automatic building of DSO source files in libraries
- Add 'Houdini Application Directory' parameter to dialog (required for
  DSO building if the path could not be automatically determined)
- Always adds the `python/` folder of a library to the `PYTHONPATH` in your
  Houdini environment file, even if the directory doesn't exist at install
  time (thus updating the library does not necessarily require a reinstall
  when the directory is added in the update)

## v0.0.2

- Fix `NameError: name 'parser' is not defined` when `~/.houdini-manage.ini`
  file did not exist

## v0.0.1

- Initial version with a simple GUI
