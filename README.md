This is a basic proof-of-principal Django app that utilizes Twitter's Streaming API for streaming and parsing/polling realtime data from Twitter.

You can search by hashtags in the frontend and then monitor in Terminal the stream as it pulls relevant content:


Setup:

```$ virtualenv ENV```

```$ source ENV/bin/activate```

```$ pip install -r requirements.txt```


Include your Twitter app credentials in ```twitter_poller/twitter_streaming_API.py``` and ```twitter_poller/poller.py```

Include the URL of your Heroku app in ALLOWED_HOSTS in ```twitterpollersite/settings.py```

Heroku deploy notes:

After initial attempts to push git repo, it was failing during collectstatic. Turns out, because I had no ```static``` directory inside the project package (because all static files are in the pollerapp app package). Even after creating an empty ```static``` directory, still no dice, because git won't push empty directories. So cd inside ```static``` and created a file called ```.keep```, which did the trick.

https://stackoverflow.com/questions/36665889/collectstatic-error-while-deploying-django-app-to-heroku


MONITORING:

For local requests monitoring for deployed app, in the git-heroku project run ```$ heroku logs --tail```
