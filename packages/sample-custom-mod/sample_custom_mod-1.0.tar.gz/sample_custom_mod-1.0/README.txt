How to make and install python modules


1. For making python module,

$ python3 setup.py sdist
running sdist
running check
warning: check: missing required meta-data: url

warning: sdist: manifest template 'MANIFEST.in' does not exist (using default file list)

warning: sdist: standard file not found: should have one of README, README.txt

writing manifest file 'MANIFEST'
creating flem_custom_mod-1.0
making hard links in flem_custom_mod-1.0...
hard linking flem_custom_mod.py -> flem_custom_mod-1.0
hard linking setup.py -> flem_custom_mod-1.0
creating dist
Creating tar archive
removing 'flem_custom_mod-1.0' (and everything under it)



2. For installing the python module,

$ sudo python3 setup.py install
running install
running build
running build_py
running install_lib
copying build/lib/flem_custom_mod.py -> /usr/local/lib/python3.6/dist-packages
byte-compiling /usr/local/lib/python3.6/dist-packages/flem_custom_mod.py to flem_custom_mod.cpython-36.pyc
running install_egg_info
Writing /usr/local/lib/python3.6/dist-packages/flem_custom_mod-1.0.egg-info


3. TWINE:
Twine is a utility for uploading python modules to PyPi.

For installing the twine,
$ sudo pip install twine

For uploading the module,
$ twine upload dist/*

For installing the uploaded module,
$ sudo pip install flem-custom-mod

