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

import envoy
import logging


logger = logging.getLogger(__name__)


class KdeWindowManager(object):

    def __init__(self, workspace=6):
        self.prev_workspace = 1
        self.workspace = 6

    def show(self):
        logger.info('kde show')
        envoy.run('qdbus org.kde.kwin /KWin org.kde.KWin.setCurrentDesktop 6',
                  timeout=2)
        # envoy.run('killall firefox', timeout=2)
        # envoy.connect('firefox http://standup-backend.herokuapp.com/?room=12')

    def hide(self):
        logger.info('kde hide')
        envoy.run(('qdbus org.kde.kwin /KWin '
                  'org.kde.KWin.setCurrentDesktop {}')
                      .format(self.prev_workspace),
                  timeout=2)
        # envoy.run('killall firefox', timeout=2)
