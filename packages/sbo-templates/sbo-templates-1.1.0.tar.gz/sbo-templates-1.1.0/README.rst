.. contents:: Table of Contents:


.. code-block:: bash

         _                 _                       _       _            
     ___| |__   ___       | |_ ___ _ __ ___  _ __ | | __ _| |_ ___  ___ 
    / __| '_ \ / _ \ _____| __/ _ \ '_ ` _ \| '_ \| |/ _` | __/ _ \/ __|
    \__ \ |_) | (_) |_____| ||  __/ | | | | | |_) | | (_| | ||  __/\__ \
    |___/_.__/ \___/       \__\___|_| |_| |_| .__/|_|\__,_|\__\___||___/
                                            |_|                         


About
-----

sbo-templates creates easy, fast and safe SlackBuilds scripts

Features
--------

- Create fast and safe templates.
- Reading existing files templates for editing.
- Repairs wrong templates.
- Select editor for working (dafault is 'vim').
- Auto-import data from .info file 
  (such as maintainer name, appllication name, version etc.)
- Autocorrect the quotation mark in the .info file
- Warning for failed checksum.
- Auto-update the source checksum

Install
-------

.. code-block:: bash

    $ tar xvf sbo-templates-<version>.tar.gz
    $ cd sbo-templates-<version>
    $ ./install.sh

    or
    
    $ pip install sbo-templates --upgrade
    
    or

    $ pip install sbo-templates-<version>.tar.gz


Requirements
------------

- Requires Python 2.7+. It has been tested with Python 2.7.14

- python2-pythondialog >= 3.4.0


Usage
-----

.. code-block:: bash

    Usage: sbotmp <application>

    Optional arguments:
      -h, --help           display this help and exit
      -v, --version        print version and exit


For a new project, you create at first a new folder with the same name with the project,
for an existing project, come into the folder and start to edit. Enjoy!

Screenshots
-----------

.. image:: https://gitlab.com/dslackw/images/raw/master/sbo-templates/sbo-templates-1.png
    :target: https://gitlab.com/dslackw/sbo-templates


.. image:: https://gitlab.com/dslackw/images/raw/master/sbo-templates/sbo-templates-2.png
    :target: https://gitlab.com/dslackw/sbo-templates


.. image:: https://gitlab.com/dslackw/images/raw/master/sbo-templates/sbo-templates-3.png
    :target: https://gitlab.com/dslackw/sbo-templates


.. image:: https://gitlab.com/dslackw/images/raw/master/sbo-templates/sbo-templates-4.png
    :target: https://gitlab.com/dslackw/sbo-templates

 
.. image:: https://gitlab.com/dslackw/images/raw/master/sbo-templates/sbo-templates-5.png
    :target: https://gitlab.com/dslackw/sbo-templates


Copyright 
---------

- Copyright © Dimitris Zlatanidis
- Slackware® is a Registered Trademark of Patrick Volkerding.
- Linux is a Registered Trademark of Linus Torvalds.
