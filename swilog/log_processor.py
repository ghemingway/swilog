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

import os
import re
import hashlib

class LogProcessor(object):
    """
    Handle the processing of a single type of log
    """
    def __init__(self, logger, config):
        try:
            self.logger = logger
            self.label = config['label']
            self.container = config['container']
            self.hostname = config['hostname']
            self.format = config['format']
            self.directory = config['directory']
            self.file_name = config['file_name']
            self.compress = config['compress']
            self.remove = config['remove']

        except Exception as e:
            logger.fatal('Failed to initialize LogProcessor')
            exit(-1)


    def _filter_files(self):
        """
        Filter files based on regex pattern
        :param all_files: list of strs, relpath of the filenames under self.directory
        :param pattern: regex pattern to match against filenames
        :returns : dict mapping full path of file to match group dict
        """
        all_files = []
        for path, dirs, files in os.walk(self.directory):
            all_files.extend(os.path.join(path, f) for f in files)
        all_files = [os.path.relpath(f, start=self.directory) for f in all_files]
        pattern = '''^%s-(?P<year>[0-9]{4})
                         (?P<month>[0-1][0-9])
                         (?P<day>[0-3][0-9])
                         (?P<hour>[0-2][0-9]).*$''' % self.file_name
        filename2match = {}
        for filename in all_files:
            match = re.match(pattern, filename, re.VERBOSE)
            if match:
                full_path = os.path.join(self.directory, filename)
                filename2match[full_path] = match.groupdict()

        return filename2match


    def _determine_key(self, year, month, day, hour):
        """
        Build the object key name
        """
        values = []
        for pos,format in enumerate(self.format):
            if format == 'host':
                values.append(self.hostname)
            elif format == 'date':
                values += [year, month, day, hour]
            elif format == 'label':
                values.append(self.label)
        return '/'.join(values)


    def process(self, conn):
        """
        Process the uploading of one log file
        """
        file_list = self._filter_files()
        for filename, match in file_list.items():
            # Determine the key name
            key_name = self._determine_key(**match)
            if os.path.getsize(filename) != 0:
                self.logger.debug("Processing log: %s" % filename)
                hash = hashlib.md5()
                # Do we compress
                already_compressed = True if filename.endswith('.gz') else False
                if self.compress and not already_compressed:
                    source_file = gzip.open(filename, 'rb')
                    for line in source_file:
                        # filter out bad lines here?
                        hash.update(line)
                else:
                    source_file = open(filename, 'rb')
                hash = hash.hexdigest()
                # Upload the file
                self.logger.debug('Uploading %s.' % filename)
                headers = {'x-object-meta-original-name': filename, 'x-hash': hash }
                conn.put_object(self.container, key_name, source_file,
                    content_type = 'text/directory',
                    headers = headers)
                # Determine if we need to remove the file
                if self.remove:
                    self.logger.info("Deleting local copy of %s" % filename)

