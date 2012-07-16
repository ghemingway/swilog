Swift-based Log Uploader
==================

This package tries to solve a simple problem.  In large deployments you want
to maintain your log files for a while, so you need a persistant, centralized
location to keep them.  A [Swift](https://github.com/openstack/swift "Swift")
object store is an ideal location.  Swilog is a very lightweight python-based
method for specifying multiple log files to be uploaded to a Swift store.  Swilog
is heavily influenced by [Slogging](https://github.com/notmyname/slogging "slogging"),
and a good deal of code was adapted from there.

How to Deploy
=============

1. Configure swilog.conf
2. Configure log files to rotate appropriately
3. Setup cron schedule


How to Build to Debian Packages
===============================

Dependencies:

    sudo apt-get install apt-file
    sudo apt-get install debhelper
    sudo apt-get install python-support
    sudo easy_install stdeb

Clone the version you want and build the package with [stdeb](https://github.com/astraw/stdeb "stdeb"):

    git clone http://github.com/ghemingway/swilog.git swilog_1.0.0
    cd swilog_1.0.0
    python setup.py --command-packages=stdeb.command bdist_deb
    dpkg -i deb_dist/swilow_0.0.5-1_all.deb
