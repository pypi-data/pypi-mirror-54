`membernator` is a tool that can be used to scan membership cards and establish if
they're valid or not against a CSV database.

# Dependencies

This program is written in Python 3. You will need to install these dependencies
to run `membernator` properly:

* python3
* pygame
* docopt

# Installation

## Debian

`membernator` is packaged in Debian! You can install it using:

    $ sudo apt install membernator

## With setup.py

You can install `membernator` like any other python program with the help of
`setuptools`:

    $ python3 setup.py install

## With pip

You can install `membernator` by downloading it from PyPi:

  $ pip3 install membernator

# Internationalisation

Membernator supports internationalisation. If you wish to add new locales, you
can use the files in the `locales` directory.

Current locales supported are:

* English (default)
* French

Note that internationalisation is only supported if you install the Debian
package.

# Usage

    Usage:
        membernator [options] --database FILE
        membernator (-h | --help)
        membernator --version

    Options:
        -h  --help       Shows the help screen
        --version        Outputs version information
        --database FILE  Path to the CSV database
        --id_col ID      "id" column in the CSV database. [default: ID]
        --name_col NAME  "name" column in the CSV database. [default: NAME]
        --time SEC       Delay in secs between scans. [default: 2.5]
        --width WIDTH    Width in pixels. Use 0 for fullscreen. [default: 800]
        --height HEIGHT  Height in pixels. Use 0 for fullscreen. [default: 480]
        --logfile LOG    Path to the logfile
