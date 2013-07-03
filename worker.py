import os, time
import threading, Queue
import json
import requests

class WorkerThread(threading.Thread):
    """ A worker thread that takes notifications from a queue, and sends out the notification

        Ask the thread to stop by calling its join() method.
    """
    def __init__(self, notification_q, subscribers):
        super(WorkerThread, self).__init__()
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
                
                # send out the notification to all subscribers
                self.notify_email(notification, self.subscribers)


            except Queue.Empty:
                continue

    def join(self, timeout=None):
        self.stoprequest.set()
        super(WorkerThread, self).join(timeout)


    def notify_email(self, notification, subscribers):


        MailGunUri = 'https://api.mailgun.net/v2/samples.mailgun.org/messages '
        MailGunAPI = 'https://api.mailgun.net/v2'
        MailGunKey = 'key-6ics5m3vw3-99m-dxt85hv5mamfhm-b4'

        # authenticate with mailgun

        for subscriber in subscribers:
            notification_types = subscriber.get('notification_types')

            for n_type in notification_types:
                if n_type.get('type') == 'email':
                    to_address = n_type.get('value')
                    body = notification.get('body')
                    subject = notification.get('subject')

                    print 'sending out a notification to ' + to_address
                    print subject
                    print body

                    # send the notification
                    r = requests.post(MailGunUri, data='from="Cloud Notifications" to="'+ to_address  +'" subject="' + subject + '" text="' + body + '"',  auth=('api', MailGunKey))
        


