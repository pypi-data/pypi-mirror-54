# Cloud-Push-Notifications Python Client
This repository contains a simple Python client for the Bluemix/IBM push notification service

Installation
===
```bash
pip install cloud-push-client
```

Getting Started
===
Log into IBM/Bluemix cloud and retrieve api_key, app_id and client_secret from your push service
```python
import cloudpush.Client as cp
push_client = cp.Client("api_key", "app_id", "client_secret")
```

Methods
===

devices
---
```python
register_device(token, platform, device_id=None)

delete_device(device_id)

get_devices()

get_device_stats()
```

topics
---
```python
register_topic(name,description=None)

delete_topic(name)
```

subscriptions
---
```python
subscribe( topic, device_id)

unsubscribe(self, topic, device_id)

get_subscriptions( topic, device_id=None)
```

push messages
---
```python
get_push_stats()


send_message(alert, url=None,
                     platforms=["A", "G"],
                     payload="", 
                     device_ids=None,
                     topics=None,
                     badge=1,
                     ttl=3600,
                     type='DEFAULT',
                     title=None,
                     subtitle=None,
                     validate=True)
```

