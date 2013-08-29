**Cloud Notifications is a Notifications as a Service offering built on top of Open Stack's Marconi Project.**

The concept is simple:

- Publisher (the application/website) wil publish() messages on to a specific queue
- The application will be responsible for advertising the queue's to the public

- Subscribers will subscribe to queue's that they will be interested in (topics)
- Subscribers will be constantly running, listening to each queue for messages. (Eventually support push for push based queues) 
- Subscribers will contain pluugable middleware for
  - Analysing/Transforming a Message
  - Passing on the message (eg send to another queue for furthur processing, sending an email, sending an sms)

- Publishers and Subscribers will be authenticated using Keystone.

Note : This is a hack day project, and is very much a proof of concept only.


*Execution*
To run this locally: >gunicorn notify:app

*API*

Subscriber Actions

    PUT /v1/{topic}/subscription # subscribe to a topic, returning messages (simulates push)
    DELETE /v1/{topic}/subscription # unsubscribe from a topic
    
Publisher Actions

    POST /v1/{topic}/messages # publish messages to the topic
