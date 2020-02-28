import os
import sys
import threading
import logging

LOG = logging.getLogger(__name__)

class ProgressPercentage(object):

    def __init__(self, filename):
        self._filename = filename
        self._size = float(os.path.getsize(filename))
        self._seen_so_far = 0
        self._lock = threading.Lock()

    def __call__(self, bytes_amount):
        # To simplify, assume this is hooked up to a single filename
        with self._lock:
            self._seen_so_far += bytes_amount
            percentage = (self._seen_so_far / self._size) * 100
            LOG.info("Progress: %s  %s / %s (%s)",
                     self._filename,
                     self._seen_so_far,
                     self._size,
                     percentage)

            if percentage == 100:
                LOG.info("Upload of %s is complete!", self._filename)
