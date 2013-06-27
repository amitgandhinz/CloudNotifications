**Cloud Notifications is a Notifications as a Service offering built on top of Open Stack's Marconi Project.**

The concept is simple:

- Publisher (the application/website) will broadcast messages on to a specific queue
- The application will be responsible for advertising the queue's to the public
- Users will register with the Notifications product (application can do this on behalf of user)
- Users will (be) subscribed to queue's that they will be interested in
- Subscribers/Workers will be constantly running, listening to each queue for messages.  
- Users subscribed to that queue will be notified based on their preferences when a message appears.


Note : This is a hack day project, and is very much a proof of concept only.
