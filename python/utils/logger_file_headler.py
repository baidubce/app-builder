# Copyright (c) 2024 Baidu, Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os
import time
import glob
import logging
from datetime import datetime, timedelta

class SizeAndTimeRotatingFileHandler(logging.Handler):
    def __init__(self, 
                 file_name, 
                 rotate_frequency='MIDNIGHT', 
                 rotate_interval=1, 
                 max_file_size=0, 
                 max_log_files=0, 
                 total_log_size=0
                 ):
        super().__init__()
        self.file_name = file_name
        self.rotate_frequency = rotate_frequency.upper()
        self.rotate_interval = rotate_interval
        self.max_file_size = max_file_size
        self.max_log_files = max_log_files
        self.total_log_size = total_log_size
        self.current_time = datetime.now()
        self.current_file = self.file_name
        self.stream = open(self.current_file, 'a')
        self.last_rollover = time.time()

    def _get_new_filename(self):
        suffix = self.current_time.strftime("%Y-%m-%d_%H-%M-%S")
        return f"{self.file_name}.{suffix}"

    def emit(self, record):
        if self.shouldRollover(record):
            self.doRollover()
        self.stream.write(self.format(record) + '\n')
        self.stream.flush()

    def shouldRollover(self, record):
        current_time = time.time()
        current_size = os.path.getsize(self.current_file)

        time_rollover = False
        if self.rotate_frequency == 'S':
            time_rollover = current_time >= self.last_rollover + self.rotate_interval
        elif self.rotate_frequency == 'M':
            time_rollover = current_time >= self.last_rollover + self.rotate_interval * 60
        elif self.rotate_frequency == 'H':
            time_rollover = current_time >= self.last_rollover + self.rotate_interval * 3600
        elif self.rotate_frequency == 'D':
            time_rollover = current_time >= self.last_rollover + self.rotate_interval * 86400
        elif self.rotate_frequency == 'MIDNIGHT':
            time_rollover = datetime.fromtimestamp(current_time).date() != datetime.fromtimestamp(self.last_rollover).date()

        size_rollover = current_size >= self.max_file_size if self.max_file_size > 0 else False

        return time_rollover or size_rollover

    def doRollover(self):
        self.stream.close()
        self.current_time = datetime.now()
        new_filename = self._get_new_filename()
        os.rename(self.current_file, new_filename)  # Rename current file to new name
        self.current_file = self.file_name
        self.stream = open(self.current_file, 'a')
        self.last_rollover = time.time()
        self.manage_log_files()

    def manage_log_files(self):
        log_files = sorted(glob.glob(f"{self.file_name}.*"), key=os.path.getmtime)

        while len(log_files) > self.max_log_files:
            oldest_log = log_files.pop(0)
            os.remove(oldest_log)

        while self._total_size(log_files) > self.total_log_size:
            if log_files:
                oldest_log = log_files.pop(0)
                os.remove(oldest_log)

    def _total_size(self, files):
        return sum(os.path.getsize(f) for f in files if os.path.exists(f))

    def close(self):
        self.stream.close()
        super().close()