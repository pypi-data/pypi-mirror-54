#
# Copyright (c)
#  2014 Adam Tauno Williams <awilliam@whitemice.org>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE
#
from time import time
from coils.core import Command, CoilsException


class GetProxyLog(Command):
    __domain__ = "admin"
    __operation__ = "get-proxy-log"

    def parse_parameters(self, **params):
        Command.parse_parameters(self, **params)
        self._callback = params.get('callback', None)

    def _local_callback(self, uuid, source, target, data):
        self.log.debug('admin:get-proxy-log self callback reached.')
        if (uuid == self._uuid):
            if (data is not None):
                if (isinstance(data, dict)):
                    if (data.get('status', 500) == 200):
                        self._data = data.get('payload', 'No content')
                    else:
                        raise CoilsException(
                            'Administrator reports error returning proxy log.'
                        )
                else:
                    raise CoilsException(
                        'Unexpected data type in packet payload from '
                        'administrator.'
                    )
            else:
                raise CoilsException(
                    'Administrator responded with packet having no payload.'
                )
            return True
        return False

    def _wait(self):
        if (self._data is None):
            if (time() < self._timeout):
                return True
        return False

    def run(self):
        self._data = None
        if (self._callback is None):
            self._callback = self._local_callback
            local_callback = True
            self.log.debug('admin::get-proxy-log using self callback')
        else:
            local_callback = False
        self._uuid = self._ctx.send(
            None,
            'coils.administrator/get_proxy_log',
            None,
            callback=self._callback,
        )

        if (local_callback):
            self._timeout = time() + 10
            self.log.debug(
                'entering wait @ {0} till {1}'
                .format(time(), self._timeout, )
            )
            while (self._wait()):
                self._ctx.wait(timeout=10000)
                self.log.debug('resuming wait @ {0}'.format(time()))
            self.log.debug('exited wait @ {0}'.format(time()))
            if (self._data is None):
                raise CoilsException('No response from coils.administrator')
            else:
                self._result = self._data
        else:
            self._result = self._uuid
