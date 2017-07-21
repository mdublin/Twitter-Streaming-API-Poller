import json
import twitter
from math import floor

# registering python-twitter instance
api = twitter.Api(
    consumer_key='{YOUR CONSUMER KEY}',
    consumer_secret='{YOUR CONSUMER SECRET}',
    access_token_key='{YOUR ACCESS_TOKEN_KEY}',
    access_token_secret='{YOUR ACCESS_TOKEN_SECRET}')

def poll_twitter(tags_request):

    if len(tags_request) == 0:
        return None
    # updating for case insensitivity
    tags_request = [tag.upper() for tag in tags_request]

    # build raw_query
    query_string = "l=&q="
    if len(tags_request) > 1:
        for index, item in enumerate(tags_request):
            if index != len(tags_request) - 1:
                query_string += "%23" + str(item) + "%20OR%20"
            else:
                query_string += "%23" + str(item)
    else:
        query_string = "q=%23" + str(tags_request[0])

    query_string = query_string + "%20&result_type=recent&count=1000000"

    # using our module built to utilize Twitter Streaming API
    from .twitter_streaming_API import start_twitter_stream
    search = start_twitter_stream(tags_request)
    return parse_twitter_response(search, tags_request)

running_count_sums = []

def parse_twitter_response(search, tags_request):

    global running_count_sums

    tags_container = []

    for index, item in enumerate(search):
        try:
            for idx, i in enumerate(item["entities"]["hashtags"]):
                print(i["text"])
                tags_container.append((i["text"]).upper()) # for case insensitivity
        except KeyError as e:
            print(e)

    # building customized JSON response object
    hashtag_entries = []
    JSON_output = {"scene": {"twitterpoll": hashtag_entries}}

    # hold counts for percent maker
    counts = []

    # counting tags and populating JSON_output with entries
    for idx, i in enumerate(tags_request):
        tag_entry = {}
        tag_count = tags_container.count(tags_request[idx])
        counts.append(tag_count)
        tag_entry["choice"] = i
        tag_entry["hits"] = tag_count
        hashtag_entries.append(tag_entry)

    # sum of tag counts
    countsum = sum(counts)
    running_count_sums.append(countsum)

    print("countsum: {}".format(countsum))
    print("counts: {}".format(counts))

    return get_percents(counts, countsum, JSON_output, hashtag_entries)


def get_percents(counts, countsum, JSON_output, hashtag_entries):
    # iterate through counts list, do some math that eventually results in percentage string
    # insert that percent value back into hashtag_entries items (which as dicts)
    # indexes from counts and hashtag_entries match up obviously, allowing easy insert without Big O of n**2 nested loop
    for idx, item in enumerate(counts):
        try:
            percent = '{}%'.format(str((floor(((float(item) / float(countsum))) * 10000) / 100)))
            hashtag_entries[idx]["percentage"] = percent
        except ZeroDivisionError as e:
            print(e)
            return None

    with open('pollerapp/static/JSONOutput/testoutput.json', 'w') as myfile:
        myfile.write(json.dumps(JSON_output))

    return json.dumps(JSON_output)
