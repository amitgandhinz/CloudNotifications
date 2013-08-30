import Queue
import requests
import json
import time

from worker import WorkerThread

def main(args):
    print 'start main'

    CLOUD_QUEUING_URI = 'http://preview.queue.api.rackspacecloud.com'
    queue_uri = CLOUD_QUEUING_URI + '/v1/queues/StockTicker_RAX/messages'

    # Create a single input queue for all threads.
    notification_q = Queue.Queue()

    # Get the list of subscribers for this queue
    subscribers = get_subscribers('StockTicker_RAX')

    # Create the "thread pool"
    pool = [WorkerThread(notification_q=notification_q, subscribers=subscribers) for i in range(1)]

    # Start all threads
    for thread in pool:
        thread.start()

    # Give the workers some work to do
    print 'Assigning work\n'
    work_count = 0


    

    while True:
        notifications_list = get_notifications(queue_uri)

        if notifications_list is not None: 
            

            queue_uri = CLOUD_QUEUING_URI + notifications_list.get('links', {})[0].get('href')
            
            # for each message
            for notification in notifications_list.get('messages', {}):
                # add the message to the queue
                notification_q.put(notification)
                print 'added new notification to queue:  %s \n' % notification.get('body').get('subject')
        else:
            print 'no notifications received'

        print 'notifications currently in queue = %d \n' % notification_q.qsize()
        time.sleep(10)


    # Ask threads to die and wait for them to do it
    # for thread in pool:
    #    thread.join()

def get_notifications(queue_uri):
    # hardcoded variables for now - these should drive from elsewhere
    token = 'f40749219d704116bdc3a836afaa532a'
    queue_headers = {"X-Auth-Token" : token, "Content-Type" : "application/json; charset=utf-8", "Client-ID" : "CloudNotificationsSubscriber"}

    # get the list of messages on that channel
    r = requests.get(queue_uri, headers=queue_headers)

    if len(r.text) > 0:
        return json.loads(r.text, 'utf-8')
    else:
        return None

def get_subscribers(queue_name):
    subscribers_uri = 'http://localhost:8000/notifications/' + queue_name + '/subscribers'
    
    token = 'f40749219d704116bdc3a836afaa532a'
    queue_headers = {"X-Auth-Token" : token, "Content-Type" : "application/json; charset=utf-8"}

    # get the list of messages on that channel
    r = requests.get(subscribers_uri, headers=queue_headers)

    return json.loads(r.text, 'utf-8')


if __name__ == '__main__':
    import sys
    main(sys.argv[1:])



