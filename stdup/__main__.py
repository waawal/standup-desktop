# -*- coding: utf-8 -*-

# Copyright 2013 Jacek Mitręga

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import unicode_literals

import logging
import sys

from tornado import ioloop
from ws4py.client.tornadoclient import TornadoWebSocketClient

from stdup import StdupDesktop


log_formatter = logging.Formatter('%(levelname)-8s | %(name)-8s :: %(message)s')
console_handler = logging.StreamHandler()
console_handler.setFormatter(log_formatter)
root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)
root_logger.addHandler(console_handler)

logger = logging.getLogger(__name__)


server = sys.argv[1]
room = sys.argv[2]
name = sys.argv[3]
video = bool(sys.argv[4])


class StdupClient(TornadoWebSocketClient):

    def __init__(self, *args, **kwargs):
        super(StdupClient, self).__init__(*args, **kwargs)
        self.stdup = None

    def opened(self):
        logger.debug('opened')
        try:
            self.stdup = StdupDesktop(self, room, name, video)
        except Exception as e:
            logger.exception('opened exception')

    def received_message(self, msg):
        logger.debug('received_message: {}'.format(msg))
        try:
            self.stdup.received_message(msg)
        except Exception as e:
            logger.exception('received_message exception')

    def closed(self, code, reason=None):
        logger.debug('closed: code={code} reason={reason}'
                     .format(code=code, reason=reason))
        try:
            self.stdup.closed(code, reason)
            self.stdup = None
            ioloop.IOLoop.instance().stop()
        except Exception as e:
            logger.exception('closed exception')

    def _cleanup(self):
        try:
            logger.debug('_cleanup')
        except Exception as e:
            logger.exception('_cleanup exception')


ws = StdupClient('ws://{server}/sock/websocket'.format(server=server),
                 protocols=['http-only', 'chat'])
ws.connect()

ioloop.IOLoop.instance().start()
