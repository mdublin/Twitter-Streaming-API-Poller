import time
import json
import os
import logging
import requests
from threading import Thread
from http.client import IncompleteRead
from twython import TwythonStreamer
from twython import Twython

APP_KEY = '{YOUR APP_KEY}'
APP_SECRET = '{YOUR APP SECRET KEY}'
OAUTH_TOKEN = '{OAUTH_TOKEN}'
OAUTH_TOKEN_SECRET = '{OAUTH_TOKEN_SECRET}'


class StreamListener(TwythonStreamer):
    def __init__(self, APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                 comm_list):
        super().__init__(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
        self.tweet_list = comm_list

    def on_success(self, data):
        # stream data gets saved to tweet_list aka comm_list which is passed
        # during StreamListener instantiation
        print("fetching data...")
        self.tweet_list.append(data)
        logging.info("tweet captured")
        if 'text' in data:
            print(data['text'])

    def on_error(self, status_code, data):
        logging.error(status_code)
        logging.error(data)
        if int(status_code) == 406:
            data = str(data)
            try:
                index = int(data.strip().split()[4])
                logging.error("to remove index:" + str(index))
                raise TooLongTermException(index)
            except ValueError:
                logging.debug("ValueError while trying to extract number")
        self.disconnect()

    def stop_stream(self):
        print("Disconnecting stream......")
        self.disconnect()


def run_listener(*args):
    try:
        streamer.statuses.filter(track=tags)
        print("after")
    except requests.exceptions.ChunkedEncodingError:
        print('error, but under control\n')
        pass
    except IncompleteRead:
        print('incompletetereaderror, but under control')
        pass
    except TooLongTermException as e:
        index_to_remove = e.get_too_long_index()
        filter_terms.pop(index_to_remove)


def disconnection_timer(*args):
    print(*args)
    time.sleep(30)
    # calling stop_stream() method on streamer instance
    streamer.stop_stream()
    return comm_list


def start_twitter_stream(request_tags):
    print("start_twitter_stream() called!!!")
    global tags
    tags = request_tags
    global comm_list
    comm_list = []

    # making this global so that disconnect_timer can call stop_stream()
    # method on the same instance that run_stream is using
    global streamer

    streamer = StreamListener(
        APP_KEY,
        APP_SECRET,
        OAUTH_TOKEN,
        OAUTH_TOKEN_SECRET,
        comm_list)

    # Start the threads

    timer = Thread(target=disconnection_timer, args=(comm_list))
    timer.start()
    listener = Thread(target=run_listener, args=(tags))
    listener.start()
    listener.join()
    timer.join()
    return comm_list
