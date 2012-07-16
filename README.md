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

1. Configure swilog.conf (see below)
2. Configure log files to rotate appropriately
3. Setup cron schedule


Swilog Configuration
====================

Customize the Swilog configuration to suit your individual machine's logging
needs.  The default behavior is for swilog to look for a configuration file
at /etc/swilog/swilog.conf.  A sample conf is included in the source etc/
directory.  Customize this one or write your own.  Is is a very simlpe yaml
schema described below:

Global Options:

    Global:

    swift_auth: Something like "https://swift.isis.vanderbilt.edu/auth/v1.0".  No default.  Required.
    swift_user: Something like "swift_tenant:account".  No default.  Required.
    swift_password: "supersecretpassword".  No default.  Required.
    hostname: Something like "myserver".  Hostname the logs are recorded as coming from.  Defaults to /etc/hostname.
    compress: true/false.  Should all logs be gzipped.  Defaults to true.
    remove: true/false.  Should logs be deleted once they are uploaded.  Defaults to true.
    create_container: true/false.  Should the swift container be created if not already present.  Defaults to true.
    container: Something like "logs_raw".  The name of the container into which all logs are written.  Defaults to "logs_raw".
    format: See discussion below.  Defaults to ['date','host','label'].
    lookback_hrs: Integer.  How many hours must have passed since the file was last written to.  Defaults to 1.
    expire_days: Integer.  Mark after how many days the uploaded file will be purged from Swift.  Defaults to infinity.

Per Log Options:

Each log is defined separately, but all are encapsulated within one section, such as:

    Logfiles: [
        { label: Foo, directory: /var/log/, file_name: foo },
        { label: Barr, directory: /var/log/bar/, filen_name: bar }
    ]

Here are the options that can be set for each individual log:

    label: Something like "my_syslog".  No default.  Mandatory.
    directory: Something like "/var/log/".  No default.  Mandatory.
    file_name: Something like "syslog".  No default.  Mandatory.
    compress = See above.  Defaults to global value.
    remove = See above.  Defaults to global value.
    lookback_hrs = See above.  Defaults to global value.
    expire_days = See above.  Defaults to global value.


Swift Object Key Format
=======================

The name that is given to each uploaded log file is very configurable.

MORE HERE...


How to Setup Logs for Hourly Collection
=======================================

Here are a couple of examples how this could be used.

*auth.log*

Let'say you want to collect the auth log from your machines every hour.  On Ubuntu by default auth events go through
rsyslog, so configuring this is pretty easy.  Modify the rsyslog configuration to use an hourly template.  With
a bit of permissioning you can get it going.

1. Modify /etc/rsyslog.d/50-default.conf

  $template HourlyAuthLog,"/var/log/auth/hourly/%$YEAR%%$MONTH%%$DAY%%$HOUR%"
  auth,authpriv.*			?HourlyAuthLog
  auth,authpriv.*			/var/log/auth.log

2. mkdir -p /var/log/auth/hourly
3. chown -R syslog.adm /var/log/auth
4. chmod 775 /var/log/auth /var/log/auth/hourly
5. service rsyslog restart


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
    sudo dpkg -i deb_dist/python-swilog_1.0.0-1_all.deb
