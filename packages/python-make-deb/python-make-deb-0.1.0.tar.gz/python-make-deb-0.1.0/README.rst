Project forked from: `https://github.com/nylas/make-deb`

python-make-deb: Helper Tool for getting your python code into debian packages
=============================================

Python-make-deb is a simple tool that generates Debian configuration based on your setuptools configuration and git history. When run, it will create a Debian directory at the root of your python project with the necessary files to build your package into a Debian package using `dh-virtualenv <https://github.com/spotify/dh-virtualenv>`_

.. code-block:: bash

   $ cd /my/python/repository
   $ python-make-deb

   'debian' directory successfully placed at the root of your repository

If setuptools does not have complete information, python-make-deb will ask for additional information (for example, maintainer email). After initialization, a directory named "debian" will be reated at the root of your repo. Assuming you have dh-virtualenv installed, you should be able to simply create a .deb from your python project by running the following command at the root of your project.

.. code-block:: bash

   $ dpkg-buildpackage -us -uc -b

Installation
------------

To install python-make-deb:

.. code-block:: bash

   $ pip install python-make-deb

Documentation
-------------

Generating your Debian configuration can be run from any operating system. However, in order to build a debian package, you must be on a Debian-based operating system and have dh-virtualenv installed. In the future, we plan to support Vagrant integration to build packages from any platform.

Example run using docker:
.. code-block:: bash
    $ docker run --rm -ti -v $PWD:/app ubuntu:bionic
    $ apt-get update && apt-get install -y python3-setuptools python-setuptools git build-essential python3-pip dh-virtualenv debhelper libffi-dev
    $ pip3 install python-make-deb
    $ cp -r /app /app2
    $ cd /app2
    $ python-make-deb
    $ dpkg-buildpackage -us -uc -b
    $ cp /*.deb /app/
