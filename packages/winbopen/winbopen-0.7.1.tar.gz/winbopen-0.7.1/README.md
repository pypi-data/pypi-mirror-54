Opens ipynb files on double-click

winbopen looks for the nearest running notebook server - if it finds one, it
opens a web browser to that notebook. If not, it starts a new notebook server
in that directory.


Installation on Windows:

    pip install winbopen --no-binary winbopen

Usage::

    double-click on ipynb

If you're not on Windows, or double-clicking does not work run:
`2
* Linux/BSD: ``python3 -m nbopen.install_xdg``
* Mac: Clone the repository and run ``./osx-install.sh``
* Windows: ``python -m nbopen.install_win``

NB --no-binary is necessary to let the installer write to windows registry.
Binary wheels do not support post-install hooks.

This is a fork of Thomas Kluyver's [nbopen](https://github.com/takluyver/nbopen) focused on Windows platform
with the following improvements:

* one-line installation
* original nbopen stops working at a certain point of time - this bug is fixed
