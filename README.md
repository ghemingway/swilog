Swift-based Log Uploader
==================

This package tries to solve a simple problem.  In large deployments you want
to maintain your log files for a while, so why not upload them to your
swift-based cloud storage system.  Swilog is a very lightweight python-based
method for specifying multiple log files to be uploaded.  Triggered either
manually or via a cron job it is easy to maintain all of your important logging
information.  This writeup really is lame.  I should improve this soon.

How to Build to Debian Packages
===============================

    python setup.py --command-packages=stdeb.command bdist_deb
