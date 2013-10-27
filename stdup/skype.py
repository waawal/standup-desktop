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

    def __init__(self):
        self.skype = Skype4Py.Skype()
        self.skype.Attach()
        self.call = None

    def finish_call(self):
        if self.call:
            self.call.Finish()
            self.call = None

    def place_call(self, contacts):
        logger.info('calling {}'.format(contacts))
        self.finish_call()
        if contacts:
            self.call = self.skype.PlaceCall(*contacts)
