import falcon
import requests
import json
import topics
import messages
import subscribers

# falcon.API instances are callable WSGI apps
app = api = falcon.API()

# Resources are represented by long-lived class instances
topicCollection = topics.TopicCollectionResource()
topicResource = topics.TopicResource()
messageCollection = messages.MessageCollectionResource()
subscriberCollection = subscribers.SubscriberCollectionResource()
subscriberResource = subscribers.SubscriberResource()


# subscriber actions
api.add_route('/v1/topics/{topic_name}/subscribers', subscriberCollection)
api.add_route('/v1/topics/{topic_name}/subscribers/{subscriber_name}', subscriberResource)


# publisher actions
api.add_route('/v1/topics', topicCollection)
api.add_route('/v1/topics/{topic_name}', topicResource)
api.add_route('/v1/topics/{topic_name}/messages', messageCollection)
