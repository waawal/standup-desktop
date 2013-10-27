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

import Skype4Py


logger = logging.getLogger(__name__)


class SkypeCaller(object):

    def __init__(self, desktop):
        self.desktop = desktop
        super(SkypeCaller, self).__init__()
        self.run()

    def run(self):
        self.skype = Skype4Py.Skype()
        self.skype.Attach()

    def finish_call(self):
        for c in self.skype.ActiveCalls:
            try:
                c.Finish()
            except Skype4Py.SkypeError as e:
                # already finished?
                logger.error('FINISH ERROR {}'.format(e))

    def place_call(self, contacts):
        logger.info('calling {}'.format(contacts))
        self.finish_call()
        if contacts:
            try:
                self.skype.PlaceCall(*contacts)
            except Skype4Py.SkypeError as e:
                logger.error('PLACE CALL ERROR {}'.format(e))
