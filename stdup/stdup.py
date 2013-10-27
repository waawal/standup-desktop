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

from collections import OrderedDict
import json
import pprint
import sys


class StdupDesktop(object):

    def __init__(self, conn, room, name):
        self.conn = conn
        self.room = room
        self.name = name
        self.participants = OrderedDict()
        self._opened()
        print('Connection established.')

    def _opened(self):
        self._send_msg('join', room=self.room, name=self.name)

    def received_message(self, msg):
        try:
            data = json.loads(msg.data)
        except Exception as e:
            print('msg parse error:', e.__class__, e, file=sys.stderr)
            return

        try:
            handler_fn = 'on_' + data['msg']
        except KeyError as e:
            print('msg error: {}'.format(msg), file=sys.stderr)
            return

        try:
            handler = getattr(self, handler_fn, None)
            if handler:
                handler(msg, data)
            else:
                self.default_handler(msg, data)
        except Exception as e:
            print('msg handler error:', e.__class__, e, file=sys.stderr)

    def closed(self, code, reason=None):
        print('closed')

    def _send_msg(self, msg, **data):
        data['msg'] = msg
        self.conn.send(json.dumps(data))

    # ===== Message Handlers ===== #

    def default_handler(self, msg, data):
        print('unhandled message:', msg, file=sys.stderr)

    def on_join(self, msg, data):
        print('join:', msg)
        self._send_msg('welcome', name=self.name)
        self._add_participant(msg, data)

    def on_welcome(self, msg, data):
        print('{name} welcomes you.'.format(name=data.get('name')))
        self._add_participant(msg, data)

    def on_set(self, msg, data):
        print('set:', msg.data)

    # ===== Participants ===== #

    def _add_participant(self, msg, data):
        name = data['name']
        participant = {
            'name': name,
            'contact': data.get('contact', None),
        }
        self.participants[name] = participant
        print(' * current participants:')
        pprint.pprint(self.participants)
