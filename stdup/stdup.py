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

from collections import OrderedDict
import json
import logging
import pprint
import sys


logger = logging.getLogger(__name__)


class StdupDesktop(object):

    def __init__(self, conn, room, name):
        self.conn = conn
        self.room = room
        self.name = name
        self.participants = OrderedDict()
        self._opened()
        logger.info('Connection established.')

    def _opened(self):
        self._send_msg('join', room=self.room, name=self.name)

    def received_message(self, msg):
        try:
            data = json.loads(msg.data)
        except Exception as e:
            logger.error('Message JSON parse error: {}'.format(msg))
            return

        try:
            handler_fn = 'on_' + data['msg']
        except KeyError as e:
            logger.error('Message structure error: {}'.format(msg))
            return

        try:
            handler = getattr(self, handler_fn, None)
            if handler:
                handler(msg, data)
            else:
                self.default_handler(msg, data)
        except Exception as e:
            logger.exception('Message handler error: {}'.format(msg))

    def closed(self, code, reason=None):
        pass

    def _send_msg(self, msg, **data):
        data['msg'] = msg
        self.conn.send(json.dumps(data))

    # ===== Message Handlers ===== #

    def default_handler(self, msg, data):
        logger.error('unhandled message: {}'.format(msg))

    def on_join(self, msg, data):
        logger.info('join: {}'.format(msg))
        self._send_msg('welcome', name=self.name)
        self._add_participant(msg, data)

    def on_welcome(self, msg, data):
        logger.info('welcome: {}'.format(data.get('name')))
        self._add_participant(msg, data)

    def on_keepalive(self, msg, data):
        logger.info('keepalive')
        self._send_msg('alive', name=self.name)

    def on_alive(self, msg, data):
        logger.info('alive: {}'.format(data.get('name')))
        self._add_participant(msg, data)

    def on_set(self, msg, data):
        logger.info('set: {}'.format(data))

    # ===== Participants ===== #

    def _add_participant(self, msg, data):
        name = data['name']
        participant = {
            'name': name,
            'contact': data.get('contact', None),
        }
        self.participants[name] = participant
        parts = pprint.pformat(self.participants)
        logger.info('* current participants: \n{}'.format(parts))
