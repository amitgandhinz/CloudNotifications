import falcon
import requests
import json
import pymongo
import utils
from bson import BSON
from bson import json_util

class SubscriberCollectionResource:

	def __init__(self):
		# Lazy instantiation
		self._database = None

	@property
	def db(self):
		"""Property for lazy instantiation of mongodb's database."""
		if self._database is None:
			conn = pymongo.MongoClient()
			self._database = conn.notificationsDB

		return self._database

	def on_get(self, req, resp, topic_name):
		"""GET a list of subscribers to this topic"""

		# get the list of subscribers to the topic
		subscribers = self.db.subscriber_collection.find({'topic': topic_name})

		if subscribers is None:
			return

		resp.status = falcon.HTTP_200 
		resp.body = json.dumps(list(subscribers), default=json_util.default)


class SubscriberResource:
	def __init__(self):
		# Lazy instantiation
		self._database = None

	@property
	def db(self):
		"""Property for lazy instantiation of mongodb's database."""
		if self._database is None:
			conn = pymongo.MongoClient()
			self._database = conn.notificationsDB

		return self._database

	def on_put(self, req, resp, topic_name, subscriber_name):
		"""Requests a subscription to this topic"""
		new_subscriber = json.loads(req.stream.read(), 'utf-8')
		new_subscriber['name'] = subscriber_name
		new_subscriber['topic'] = topic_name

		# subscribe to the topic
		subscriberId = self.db.subscriber_collection.insert(new_subscriber)
		
		newSubscriber = self.db.subscriber_collection.find_one({u'_id' : subscriberId})

		resp.status = falcon.HTTP_200 
		resp.body = json.dumps(newSubscriber, cls=utils.MongoEncoder)


	def on_get(self, req, resp, topic_name, subscriber_name):
		"""GET a subscriber in this topic"""

		# return the subscriber.
		newSubscriber = self.db.subscriber_collection.find_one({u'name' : subscriber_name, u'topic' : topic_name})


		resp.status = falcon.HTTP_200 
		resp.body = json.dumps(newSubscriber, cls=utils.MongoEncoder)


	def on_delete(self, req, resp, topic_name, subscriber_name):
		"""REMOVE a subscriber from this topic"""

		self.db.subscriber_collection.remove({u'name' : subscriber_name, u'topic' : topic_name})
		


		resp.status = falcon.HTTP_200 
		resp.body = ''


	
	def on_patch(self, req, resp, topic_name, subscriber_name):
		"""Confirms a subscription request for this topic"""
		self.db.subscriber_collection.update({u'name' : subscriber_name, u'topic' : topic_name}, {'$set': {'confirmed' : True}}, upsert=False)

		resp.status = falcon.HTTP_200 
		resp.body = ''
	
