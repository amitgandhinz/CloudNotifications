# notify.py

# Let's get this party started
import falcon
import requests
import json

# Falcon follows the REST architectural style, meaning (among
# other things) that you think in terms of resources and state
# transitions, which map to HTTP verbs.
class NotifyResource:
	def __init__(self):
		"""Initialize"""

	def on_get(self, req, resp, appname):
		"""Handles GET requests"""
		queue_uri = CLOUD_QUEUING_URI + 'queues/' + appname + QUEUE_SUFFIX + '/messages?echo=true'
		queue_headers = {"X-Auth-Token" : AUTH_TOKEN, "Content-Type" : "application/json; charset=utf-8", "Client-ID" : "CloudNotifications"}
		
		r = requests.get(queue_uri, headers=queue_headers)

		resp.status = r.status_code
		resp.body = r.text

	def on_post(self, req, resp, appname):
		"""Handle POST requests"""

		# Lets create the queue if it doesnt exist (this should happen somewhere else)
		queue_uri = CLOUD_QUEUING_URI + 'queues/' + appname + QUEUE_SUFFIX
		queue_data = {"metadata": "Notifications Queue"}
		queue_headers = {"X-Auth-Token" : AUTH_TOKEN, "Content-Type" : "application/json; charset=utf-8"}
		
		r = requests.put(queue_uri, data=json.dumps(queue_data), headers=queue_headers)

		# Determine the set of addresses that map for this message destination

		
		# Build the notification body using the set of addresses to broadcast to
		raw_json = req.stream.read()
		notification_body = json.loads(raw_json, 'utf-8')
			

		# Lets broadcast the notification to the Cloud Queuing API
		queue_uri = CLOUD_QUEUING_URI + 'queues/' + appname + QUEUE_SUFFIX + '/messages'
		queue_data = [{"ttl": 300,"body": notification_body}]
		queue_headers = {"X-Auth-Token" : AUTH_TOKEN, "Content-Type" : "application/json; charset=utf-8", "Client-ID" : "CloudNotifications"}

		r = requests.post(queue_uri, data=json.dumps(queue_data), headers=queue_headers)

		resp.status = r.status_code
		resp.body = r.text

class UserResource:
	def on_get(self, req, resp, appname):
		"""Handles GET requests (LIST)"""
		resp.status = falcon.HTTP_200  # This is the default status
		resp.body = ('Retrieved a list of users\n')

	def on_post(self, req, resp, appname):
		"""Handles POST requests (CREATE)"""
		resp.status = falcon.HTTP_200
		resp.body = ('User Created\n')

	def on_put(self, req, resp, appname):
		"""Handles PUT requests (UPDATE)"""
		resp.status = falcon.HTTP_200
		resp.body = ('User Updated\n')


# falcon.API instances are callable WSGI apps
app = api = falcon.API()

# Resources are represented by long-lived class instances
notify = NotifyResource()
users = UserResource()

# hardcoded variables for now - these should drive from elsewhere
AUTH_TOKEN = 'f907ef4ee4ad477c83bf84a209472071'
CLOUD_QUEUING_URI = 'http://preview.queue.api.rackspacecloud.com/v1/'
QUEUE_SUFFIX = '_notifications'

# notify will handle all requests to the '/notify' URL path
api.add_route('/notifications/{appname}/messages', notify)
api.add_route('/users/', users)