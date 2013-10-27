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

from __future__ import unicode_literals, print_function

import sys

from tornado import ioloop
from ws4py.client.tornadoclient import TornadoWebSocketClient

from stdup import StdupDesktop


server = sys.argv[1]
room = sys.argv[2]
name = 'stdup-desktop'


class StdupClient(TornadoWebSocketClient):

    def __init__(self, *args, **kwargs):
        super(StdupClient, self).__init__(*args, **kwargs)
        self.stdup = None

    def opened(self):
        self.stdup = StdupDesktop(self, room, name)

    def received_message(self, msg):
        self.stdup.received_message(msg)

    def closed(self, code, reason=None):
        self.stdup.closed(code, reason)
        self.stdup = None
        ioloop.IOLoop.instance().stop()

    def _cleanup(self):
        print('cleanup', file=sys.stderr)
        pass


ws = StdupClient('ws://{server}/sock/websocket'.format(server=server),
                 protocols=['http-only', 'chat'])
ws.connect()

ioloop.IOLoop.instance().start()
