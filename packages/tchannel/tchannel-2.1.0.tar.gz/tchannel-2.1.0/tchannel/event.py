# Copyright (c) 2016 Uber Technologies, Inc.
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
# THE SOFTWARE.

from __future__ import absolute_import

import sys
import collections
import functools
import logging
import tornado

from .enum import enum

log = logging.getLogger('tchannel')


"""Types to represent system events"""
EventType = enum(
    'EventType',
    before_send_request=0x00,
    after_send_request=0x01,
    before_serialize_request_headers=0x02,
    before_send_response=0x10,
    after_send_response=0x11,
    before_receive_request=0x20,
    after_receive_request=0x21,
    before_receive_response=0x30,
    after_receive_response=0x31,
    after_receive_error=0x41,
    after_send_error=0x42,
    on_exception=0x50,
)


class EventHook(object):
    """provide all event hook interfaces

    Customized Hook should should inherit from EventHook class and implement
    the events' hooks that it wants to listen.

    Example::

        TraceHook(EventHook):
            def before_send_request(self, request):
                ....

    """

    def before_serialize_request_headers(self, headers, service):
        """Called before an outgoing request is serialized.
        Only to be used for modifying application headers.
        """
        pass

    def before_send_request(self, request):
        """Called before any part of a ``CALL_REQ`` message is sent."""
        pass

    def after_send_request(self, request):
        """Not implemented."""
        pass

    def before_send_response(self, response):
        """Not implemented."""
        pass

    def after_send_response(self, response):
        """Called after all of a ``CALL_RESP`` message is sent."""
        pass

    def before_receive_request(self, request):
        """Called after a ``CALL_REQ`` message's arg1 (endpoint) is read."""
        pass

    def after_receive_request(self, request):
        """Not implemented."""
        pass

    def before_receive_response(self, response):
        """Not implemented."""
        pass

    def after_receive_response(self, request, response):
        """Called after a ``CALL_RESP`` message is read."""
        pass

    def after_receive_error(self, request, err):
        """Called after a ``error`` message is read."""
        pass

    def after_send_error(self, err):
        """Called after a ``error`` message is sent."""
        pass

    def on_exception(self, request, err):
        """Called on exceptions within TChannel instance.

        :param request:
            The :py:class:`tchannel.tornado.request.Request` object associated
            with this uncaught exception.

        :param err:
            An instance of the unhandled exception.

            As long as this method is not a :py:func:`coroutine`, it will be
            run in the same exception context as the original error. The
            ``traceback`` module may be useful here.
        """
        pass


class EventEmitter(object):
    def __init__(self):
        self.hooks = collections.defaultdict(lambda: [])

    def register_hook(self, hook, event_type=None):
        """
        If ``event_type`` is provided, then ``hook`` will be called whenever
        that event is fired.

        If no ``event_type`` is specifid, but ``hook`` implements any methods
        with names matching an event hook, then those will be registered with
        their corresponding events. This allows for more stateful, class-based
        event handlers.
        """
        if event_type is not None:
            assert type(event_type) is int, "register hooks with int values"
            return self.hooks[event_type].append(hook)

        for event_type in EventType._fields:
            func = getattr(hook, event_type, None)
            if callable(func):
                event_value = getattr(EventType, event_type)
                self.register_hook(func, event_value)

    @tornado.gen.coroutine
    def fire(self, event, *args, **kwargs):
        for hook in self.hooks[event]:
            try:
                possible_future = hook(*args, **kwargs)
                if tornado.concurrent.is_future(possible_future):
                    yield possible_future
            except Exception:
                log.error("error calling hook", exc_info=sys.exc_info())


class EventRegistrar(object):

    def __init__(self, event_emitter):
        self.event_emitter = event_emitter

    def register(self, hook, event_type=None):
        return self.event_emitter.register_hook(hook, event_type)

    def __getattr__(self, attr):
        if attr in EventType._fields:
            event_type = getattr(EventType, attr)
            return functools.partial(
                self.register,
                event_type=event_type,
            )
        return super(EventEmitter, self).__getattr__(attr)
