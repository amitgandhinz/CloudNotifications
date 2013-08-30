import falcon
import requests
import json

class SubscriberCollectionResource:
	def on_get(self, req, resp, topic_name):
		"""GET a list of subscribers to this topic"""

		# get the list of subscribers to the topic
		
		# return the list of subscribers.
		subscribers = [
			{
				"userid" : 1, 
				"display_name" : "Amit Gandhi", 
				"notification_types" : [
					{"type" : "email", "value" : "amit.gandhi@rackspace.com"}, 
					{"type" : "twitter", "value" : "@amitgandhinz"}
				]
			},
			{
				"userid" : 2, 
				"display_name" : "Hulk Hogan", 
				"notification_types" : [
					{"type" : "instagram", "value" : "#greenguy"},
					{"type" : "irc", "value" : "freenode.org #greenguy"}
				]
			}
		]


		resp.status = falcon.HTTP_200 
		resp.body = json.dumps(subscribers)


class SubscriberResource:
	def on_get(self, req, resp, topic_name, subscriber_name):
		"""GET a subscriber in this topic"""

		# get the list of subscribers to the topic
		
		# return the list of subscribers.
		subscribers = {
				"userid" : 1, 
				"display_name" : "Amit Gandhi", 
				"notification_types" : [
					{"type" : "email", "value" : "amit.gandhi@rackspace.com"}, 
					{"type" : "twitter", "value" : "@amitgandhinz"}
				]
			}
		


		resp.status = falcon.HTTP_200 
		resp.body = json.dumps(subscribers)

	def on_delete(self, req, resp, topic_name, subscriber_name):
		"""REMOVE a subscriber from this topic"""

		# get the list of subscribers to the topic
		
		# return the list of subscribers.
		subscribers = {
			"userid" : 1, 
			"display_name" : "Amit Gandhi", 
			"notification_types" : [
				{"type" : "email", "value" : "amit.gandhi@rackspace.com"}, 
				{"type" : "twitter", "value" : "@amitgandhinz"}
			]
		}
		


		resp.status = falcon.HTTP_200 
		resp.body = json.dumps(subscribers)


	def on_put(self, req, resp, topic_name, subscriber_name):
		"""Requests a subscriber to this topic"""

		# get the list of subscribers to the topic
		
		# return the list of subscribers.
		subscribers = {
				"userid" : 1, 
				"display_name" : "Amit Gandhi", 
				"notification_types" : [
					{"type" : "email", "value" : "amit.gandhi@rackspace.com"}, 
					{"type" : "twitter", "value" : "@amitgandhinz"}
				]
			}
		


		resp.status = falcon.HTTP_200 
		resp.body = json.dumps(subscribers)

	def on_patch(self, req, resp, topic_name, subscriber_name):
		"""Confirms a subscriber request for this topic"""

		# get the list of subscribers to the topic
		
		# return the list of subscribers.
		subscribers = {
				"userid" : 1, 
				"display_name" : "Amit Gandhi", 
				"notification_types" : [
					{"type" : "email", "value" : "amit.gandhi@rackspace.com"}, 
					{"type" : "twitter", "value" : "@amitgandhinz"}
				]
			}
		


		resp.status = falcon.HTTP_200 
		resp.body = json.dumps(subscribers)
