import falcon
import requests
import json
import configs

class TopicCollectionResource:
	def __init__(self):
		"""Initialize"""

	def on_get(self, req, resp):
		"""GETs a list of topics"""
		token = req.get_header('X-Auth-Token')
		
		queue_uri = configs.queue_uri + 'queues/'
		queue_headers = {"X-Auth-Token" : token, "Content-Type" : "application/json; charset=utf-8", "Client-ID" : "CloudNotificationsPublisher"}
		
		r = requests.get(queue_uri, headers=queue_headers)

		resp.status = r.status_code
		resp.body = r.text

class TopicResource:
	def __init__(self):
		pass

	def on_put(self, req, resp, topic_name):
		"""Creates the topic"""

		token = req.get_header('X-Auth-Token')

		# Lets create the queue if it doesnt exist (this should happen somewhere else)
		queue_uri = configs.queue_uri + 'queues/' + topic_name
		queue_data = {"metadata": "Notifications Queue"}
		queue_headers = {"X-Auth-Token" : token, "Content-Type" : "application/json; charset=utf-8"}
		
		r = requests.put(queue_uri, data=json.dumps(queue_data), headers=queue_headers)

		
		resp.status = r.status_code
		resp.body = r.text

	def on_delete(self, req, resp, topic_name):
		"""DELETEs the topic"""
		token = req.get_header('X-Auth-Token')
		
		queue_uri = configs.queue_uri + 'queues/' + topic_name
		queue_headers = {"X-Auth-Token" : token, "Content-Type" : "application/json; charset=utf-8", "Client-ID" : "CloudNotificationsPublisher"}
		
		r = requests.delete(queue_uri, headers=queue_headers)

		resp.status = r.status_code
		resp.body = r.text









