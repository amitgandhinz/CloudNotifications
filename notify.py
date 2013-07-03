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

	def on_get(self, req, resp, queue_name):
		"""GETs a list of notifications from this queue"""
		token = req.get_header('X-Auth-Token')
		
		queue_uri = CLOUD_QUEUING_URI + 'queues/' + queue_name + '/messages?echo=true'
		queue_headers = {"X-Auth-Token" : token, "Content-Type" : "application/json; charset=utf-8", "Client-ID" : "CloudNotificationsPublisher"}
		
		r = requests.get(queue_uri, headers=queue_headers)

		resp.status = r.status_code
		resp.body = r.text

	def on_post(self, req, resp, queue_name):
		"""POSTs a new notification to the queue"""

		token = req.get_header('X-Auth-Token')

		# Lets create the queue if it doesnt exist (this should happen somewhere else)
		queue_uri = CLOUD_QUEUING_URI + 'queues/' + queue_name 
		queue_data = {"metadata": "Notifications Queue"}
		queue_headers = {"X-Auth-Token" : token, "Content-Type" : "application/json; charset=utf-8"}
		
		r = requests.put(queue_uri, data=json.dumps(queue_data), headers=queue_headers)

		# Determine the set of addresses that map for this message destination

		
		# Build the notification body using the set of addresses to broadcast to
		raw_json = req.stream.read()
		notification_body = json.loads(raw_json, 'utf-8')
			

		# Lets broadcast the notification to the Cloud Queuing API
		queue_uri = CLOUD_QUEUING_URI + 'queues/' + queue_name  + '/messages'
		queue_data = [{"ttl": 300,"body": notification_body}]
		queue_headers = {"X-Auth-Token" : token, "Content-Type" : "application/json; charset=utf-8", "Client-ID" : "CloudNotificationsPublisher"}

		r = requests.post(queue_uri, data=json.dumps(queue_data), headers=queue_headers)

		resp.status = r.status_code
		resp.body = r.text

class SubscriberResource:
	def on_get(self, req, resp, queue_name):
		"""GET a list of subscribers to this queue"""

		# get the list of subscribers to the queue from ObjectRocket
		
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


		resp.status = falcon.HTTP_200  # This is the default status
		resp.body = json.dumps(subscribers)

class UserResource:
	def on_get(self, req, resp):
		"""GET a list of users registered"""

		# return the list of users from ObjectRocket


		resp.status = falcon.HTTP_200  # This is the default status
		resp.body = ('Retrieved a list of users\n')

	def on_post(self, req, resp):
		"""POST a new user to be registered (Insert)"""

		# insert a new user into ObjectRocket, including what they want to subscribe to


		resp.status = falcon.HTTP_200
		resp.body = ('User Created\n')

	def on_put(self, req, resp):
		"""PUT an existing user back in the system (Update)"""

		# Update an existing User in ObjectRocket, including what they want to subscribe to


		resp.status = falcon.HTTP_200
		resp.body = ('User Updated\n')


# falcon.API instances are callable WSGI apps
app = api = falcon.API()

# Resources are represented by long-lived class instances
notify = NotifyResource()
subscribers = SubscriberResource()
users = UserResource()

# hardcoded variables for now - these should drive from elsewhere
CLOUD_QUEUING_URI = 'http://preview.queue.api.rackspacecloud.com/v1/'



# GET or PUT new notifications on the queue for broadcasting
api.add_route('/notifications/{queue_name}/messages', notify)

# GET users subscribed to this queue
api.add_route('/notifications/{queue_name}/subscribers', subscribers)

# GET or PUT new users who will subscribe to notifications
api.add_route('/users/', users)




