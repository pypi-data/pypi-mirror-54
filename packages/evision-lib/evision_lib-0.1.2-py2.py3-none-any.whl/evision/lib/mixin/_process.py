#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2019 eVision.ai Inc. All Rights Reserved.
#
# @author: Chen Shijiang(chenshijiang@evision.ai)
# @date: 2019-10-16 19:52
# @version: 1.0
import multiprocessing
import threading


class ServiceWrapperMixin(object):
    """后台服务（进程或线程）公共方法封装"""
    _initialized = False
    _running = False
    _lock = None
    _stop_event = None
    _daemon = False

    def init(self):
        pass

    def is_inited(self):
        raise NotImplementedError

    def start_working(self):
        pass

    def on_start(self):
        pass

    def stop_working(self):
        pass

    def on_stop(self):
        pass

    def start(self):
        self.on_start()
        self.start_working()
        pass

    def run(self):
        while self._running:
            with self._lock:
                self.process()

    def process(self):
        pass


class ProcessWrapper(multiprocessing.Process, ServiceWrapperMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _lock = multiprocessing.Lock()
        _stop_event = multiprocessing.Event()

    def start_working(self):
        pass

    def stop_working(self):
        pass


class ThreadWrapper(threading.Thread, ServiceWrapperMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._lock = threading.Lock()
        self._stop_event = threading.Event()

    def start_working(self):
        pass

    def stop_working(self):
        pass
