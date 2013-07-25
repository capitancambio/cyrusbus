#!/usr/bin/env python
#-*- coding:utf-8 -*-
import threading

class Bus(object):

    def __init__(self):
        self.reset()

    def subscribe(self, key, callback, force=False):
        if key not in self.subscriptions:
            self.subscriptions[key] = []

        subscription = {
            'key': key,
            'callback': callback
        }

        if force or not self.has_subscription(key, callback):
            self.subscriptions[key].append(subscription)

        return self

    def unsubscribe(self, key, callback):
        if not self.has_subscription(key, callback):
            return self

        self.subscriptions[key].remove({
            'key': key,
            'callback': callback
        })

    def unsubscribe_all(self, key):
        if key not in self.subscriptions:
            return self

        self.subscriptions[key] = []

    def has_subscription(self, key, callback):
        if key not in self.subscriptions:
            return False

        subscription = {
            'key': key,
            'callback': callback
        }

        return subscription in self.subscriptions[key]

    def has_any_subscriptions(self, key):
        return key in self.subscriptions and len(self.subscriptions[key]) > 0

    def publish(self, key, *args, **kwargs):
        if not self.has_any_subscriptions(key):
            return self

        for subscriber in self.subscriptions[key]:
            AnonymousThread(lambda:subscriber['callback'](self, *args, **kwargs)).start()

    def reset(self):
        self.subscriptions = {}

class AnonymousThread(threading.Thread):
	"""AnonymousThread"""
	def __init__(self, function):
		super(AnonymousThread, self).__init__()
		self.function= function
	def run(self):
		self.function()
