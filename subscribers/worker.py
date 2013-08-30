import os, time
import threading, Queue
import json
import requests

class WorkerThread(threading.Thread):
    """ A worker thread that takes notifications from a queue, and sends out the notification to each subscriber

        Ask the thread to stop by calling its join() method.
    """
    def __init__(self, notification_q, subscribers):
        super(WorkerThread, self).__init__()

        print 'initializing worker'
        self.notification_q = notification_q
        self.subscribers = subscribers
        self.stoprequest = threading.Event()

    def run(self):
        # As long as we weren't asked to stop, try to take new tasks from the
        # queue. The tasks are taken with a blocking 'get', so no CPU
        # cycles are wasted while waiting.
        # Also, 'get' is given a timeout, so stoprequest is always checked,
        # even if there's nothing in the queue.
        while not self.stoprequest.isSet():
            try:
                # send out the notification
                notification = self.notification_q.get(True, 0.05)
                
                print 'worker assigned to ', notification.get('body').get('default')
            
                # send out the notification to all subscribers
                self.notify_email(notification, self.subscribers)


            except Queue.Empty:
                continue

    def join(self, timeout=None):
        self.stoprequest.set()
        super(WorkerThread, self).join(timeout)


    def notify_email(self, notification, subscribers):


        MailGunAPI = 'https://api.mailgun.net/v2/gandhi.co.nz/messages'
        MailGunKey = '<GET FROM CONFIG>'

        # authenticate with mailgun

        for subscriber in subscribers:
            notification_types = subscriber.get('notification_types')

            for n_type in notification_types:
                if n_type.get('protocol') == 'email':
                    from_address = 'Amit Gandhi <amit@example.com>'
                    to_address = n_type.get('value')
                    body = notification.get('body').get('default')
                    subject = notification.get('body').get('default')

                    print 'sending out a notification to ' + to_address
                    print subject

                    # send the notification
                    r = requests.post(MailGunAPI, 
                            auth=('api', MailGunKey),
                            data={
                                "from": from_address,
                                "to": to_address,
                                "subject": subject,
                                "text": body
                            }  
                        )
                    print r, r.text




