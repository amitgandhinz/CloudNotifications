import falcon
import requests
import json
import configs


class MessageCollectionResource:
	def __init__(self):
		"""Initialize"""

	def on_get(self, req, resp, topic_name):
		"""GETs a list of notifications in the topic"""
		token = req.get_header('X-Auth-Token')
		
		queue_uri = configs.queue_uri + 'queues/' + topic_name + '/messages'
		queue_headers = {"X-Auth-Token" : token, "Content-Type" : "application/json; charset=utf-8", "Client-ID" : "CloudNotificationsSubscriber"}
		
		r = requests.get(queue_uri, headers=queue_headers)

		resp.status = r.status_code
		resp.body = r.text

	def on_post(self, req, resp, topic_name):
		"""POSTs notifications to the topic"""

		token = req.get_header('X-Auth-Token')
		
		queue_uri = configs.queue_uri + 'queues/' + topic_name + '/messages'
		queue_headers = {"X-Auth-Token" : token, "Content-Type" : "application/json; charset=utf-8", "Client-ID" : "CloudNotificationsPublisher"}
		raw_json = req.stream.read()
		message = json.loads(raw_json, 'utf-8')

		r = requests.post(queue_uri, data=json.dumps(message), headers=queue_headers)

		resp.status = r.status_code
		resp.body = r.text