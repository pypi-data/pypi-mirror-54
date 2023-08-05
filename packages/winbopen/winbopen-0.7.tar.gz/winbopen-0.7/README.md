Opens ipynb files on double-click

winbopen looks for the nearest running notebook server - if it finds one, it
opens a web browser to that notebook. If not, it starts a new notebook server
in that directory.


Installation::

    pip install winbopen

Usage::

    double-click on ipynb

If double-clicking does not work or you're not on Windows, run:

* Linux/BSD: ``python3 -m nbopen.install_xdg``
* Windows: normally automatic; for manual installation run ``python3 -m nbopen.install_win``
* Mac: Clone the repository and run ``./osx-install.sh``

This is a fork of Thomas Kluyver's [nbopen](https://github.com/takluyver/nbopen) focused on Windows platform
with the following improvements:
  
* automatic installation with only one call to `pip install`
* original nbopen stops working at a certain point of time - this bug is fixed

