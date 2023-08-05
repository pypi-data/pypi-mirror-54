# Copyright 2018 Red Hat
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
from __future__ import absolute_import

import collections
import sys

from oslo_log import log
import six


LOG = log.getLogger(__name__)


class TobikoException(Exception):
    """Base Tobiko Exception.

    To use this class, inherit from it and define attribute 'message' string.
    If **properties parameters is given, then it will format message string
    using properties as key-word arguments.

    Example:

        class MyException(TobikoException):
            message = "This exception occurred because of {reason}"

        try:
            raise MyException(reason="something went wrong")
        except MyException as ex:

            # It should print:
            #   This exception occurred because of something went wrong
            print(ex)

            # It should print:
            #   something went wrong
            print(ex.reason)

    :attribute message: the message to be printed out.
    """

    message = None

    def __init__(self, message=None, **properties):
        # pylint: disable=exception-message-attribute
        message = message or self.message or "unknown reason"
        if properties:
            message = message.format(**properties)
        self.message = message
        self._properties = properties or {}
        super(TobikoException, self).__init__(message)

    def __getattr__(self, name):
        try:
            return self._properties[name]
        except KeyError:
            msg = ("{!r} object has no attribute {!r}").format(self, name)
            raise AttributeError(msg)

    def __repr__(self):
        return "{class_name}({message!r})".format(
            class_name=type(self).__name__,
            message=self.message)


def check_valid_type(obj, *valid_types):
    if not isinstance(obj, valid_types):
        types_str = ", ".join(str(t) for t in valid_types)
        message = ("Object {!r} is not of a valid type ({!s})").format(
            obj, types_str)
        raise TypeError(message)
    return obj


class ExceptionInfo(collections.namedtuple('ExceptionInfo',
                                           ['type', 'value', 'traceback'])):

    reraise_on_exit = True

    def __enter__(self):
        return self

    def __exit__(self, _type, _value, _traceback):
        if self.reraise_on_exit:
            if _type is not None:
                LOG.exception("Exception occurred while handling %s(%s) "
                              "exception.", self.type, self.value)
            self.reraise()

    def reraise(self):
        if self.type is not None:
            six.reraise(*self)


def exc_info(reraise=True):
    info = ExceptionInfo(*sys.exc_info())
    info.reraise_on_exit = reraise
    return info
