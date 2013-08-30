import Queue
import requests
import json
import time

from worker import WorkerThread

def main(args):

    topic_name = "amits_stocks"

    # Create a single input queue for all threads.
    notification_q = Queue.Queue()

    # Get the list of subscribers for this topic
    subscribers = get_subscribers(topic_name)

    # Create the "thread pool"
    pool = [WorkerThread(notification_q=notification_q, subscribers=subscribers) for i in range(1)]

    # Start all threads
    for thread in pool:
        thread.start()

    # Give the workers some work to do
    print 'Assigning work\n'
    work_count = 0


    while True:
        notifications_list = get_notifications(topic_name)

        if notifications_list is not None: 
            # for each message
            for notification in notifications_list.get('messages', {}):
                # add the message to the queue
                notification_q.put(notification)
                print 'added new notification to queue:  %s \n' % notification.get('body').get('default')
        else:
            print 'no notifications received'

        print 'notifications currently in queue = %d \n' % notification_q.qsize()
        time.sleep(10) # poll every 10 seconds for new notifications


    # Ask threads to die and wait for them to do it
    # for thread in pool:
    #    thread.join()

def get_notifications(topic_name):

    notifications_uri = 'http://localhost:8000/v1/topics/' + topic_name + '/messages'

    # hardcoded variables for now - these should drive from elsewhere
    token = 'TOKEN_FROM_CONFIG'
    headers = {"X-Auth-Token" : token, "Content-Type" : "application/json; charset=utf-8"}

    # get the list of messages on that channel
    r = requests.get(notifications_uri, headers=headers)

    if len(r.text) > 0:
        return json.loads(r.text, 'utf-8')
    else:
        return None

def get_subscribers(topic_name):
    subscribers_uri = 'http://localhost:8000/v1/topics/' + topic_name + '/subscribers'
    
    token = 'TOKEN_FROM_CONFIG'
    queue_headers = {"X-Auth-Token" : token, "Content-Type" : "application/json; charset=utf-8"}

    # get the list of messages on that channel
    r = requests.get(subscribers_uri, headers=queue_headers)

    if len(r.text) > 0:
        return json.loads(r.text, 'utf-8')
    else:
        return None


if __name__ == '__main__':
    import sys
    main(sys.argv[1:])



