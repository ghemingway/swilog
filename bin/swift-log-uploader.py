#!/usr/bin/python
# Copyright (c) 2012 G. Hemingway
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from swiftclient import Connection, ClientException
from optparse import OptionParser
import socket
import sys
import yaml
import time
from swilog.log_processor import LogProcessor
import logging
import logging.handlers

logger = logging.getLogger('swilog')
logger.setLevel(logging.DEBUG)
if sys.platform == "darwin":
    address = '/var/run/syslog'
else:
    address = '/dev/log'
handler = logging.handlers.SysLogHandler(address)
formatter = logging.Formatter('Swilog: %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def read_configuration(filename):
    try:
        with open(filename) as f:
            conf = yaml.load(f)
            f.close()
            global_conf = conf['Global']
        if 'hostname' not in global_conf:
            global_conf['hostname'] = socket.gethostname()
        if 'create_container' not in global_conf:
            global_conf['create_container'] = True
        if 'container' not in global_conf:
            global_conf['container'] = 'logs_raw'
        if 'format' not in global_conf:
            global_conf['format'] = ['date','host','label']
        if 'compress' not in global_conf:
            global_conf['compress'] = True
        if 'remove' not in global_conf:
            global_conf['remove'] = True
        if 'lookback_hrs' not in global_conf:
            global_conf['lookback_hrs'] = 1
        return (global_conf, conf['Logfiles'])
    except IOError as e:
        logger.fatal('Configuration file %s could not be opened.  Exiting' % filename)
        sys.exit(-1)


def build_log_config(config, logfile):
    log_config = dict(config.items() + logfile.items())
    del log_config['swift_auth']
    del log_config['swift_password']
    del log_config['swift_user']
    return log_config


if __name__ == '__main__':
    parser = OptionParser(version='%prog 1.0', usage='Usage: %prog -c CONFIG_FILE')
    parser.add_option('-c', '--config', dest='config', default='/etc/swilog/swilog.conf', help='Configuration file')
    (options, args) = parser.parse_args(sys.argv[1:])
    (config, logfiles) = read_configuration(options.config)
    # Star the clock here
    start_time = time.time()
    logger.warn('Initiating log processing.')
    conn = Connection(config['swift_auth'], config['swift_user'], config['swift_password'])
    cont_name = config['container']
    try:
        container = conn.head_container(cont_name)
    except ClientException as e:
        if config['create_container']:
            logger.warn('No container by that name - Creating %s.' % cont_name)
            container = conn.put_container(cont_name)
        else:
            logger.fatal('Container %s does not exist.  Exiting.' % cont_name)
            sys.exit(-1)

    # Loop through each declared log file and process
    for logfile in logfiles:
        log_conf = build_log_config(config, logfile)
        processor = LogProcessor(logger, log_conf)
        processor.process(conn)

    elapsed_time = time.time() - start_time
    logger.warn('Processing complete.  Total execution %f seconds.' % elapsed_time)
