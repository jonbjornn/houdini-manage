+++
title = "Installation"
ordering-priority = 5
+++

[Node.py]: https://nodepy.org/

1. Install Python 2.7 or 3.3+ from [Python.org](https://python.org/)

2. Install Pip by running [get-pip.py](https://bootstrap.pypa.io/get-pip.py)
   *(Python 2.7 only)*

        > python C:\Users\niklas\Downloads\get-pip.py     # (Windows)
        $ python /Users/niklas/Downloads/get-pip.py     # (macOS)

3. Install [Node.py] with Pip

        $ pip install node.py

4. Install **Houdini-manage** by running

        $ nppm install git+https://github.com/NiklasRosenstein/houdini-manage.git

5. Check if it worked

        $ houdini-manage --version
        0.0.1

> **macOS**: It is very likely that you need to use `sudo <command>`.  
> **Windows**: Depending on where you chose to install Python, you might need
> an Administrator console on Windows.
