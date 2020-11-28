import os
import sys
import slack
import json
import time
import calendar
from time import sleep

# This script helps search number of times a message/team handle/group handle
# was mentioned in a slack channel
# Sample command to run script
# SLACK_TOKEN='<REPLACE_CORRECT_SLACK_TOKEN>' python3 scraper.py "@here" "Nov 28, 2020 @ 06:40:00 UTC" "Nov 28, 2020 @ 07:13:00 UTC"

#GET channel ID from slack web channel url
#It should be the last param when a slack channel is opened
CHANNEL_ID = "<SOME_CHANNEL_ID>"

MESSAGES_PER_PAGE = 200
MAX_MESSAGES = 1000
SEARCH_QUERY = ''
START_TIME = calendar.timegm(time.gmtime())
END_TIME = 0

#Read search term
if len(sys.argv) >= 2:
    search_term = sys.argv[1]
    if search_term[0] == '@':
        SEARCH_QUERY = "<!{}>".format(search_term[1:])
    else:
        SEARCH_QUERY = sys.argv[1]

#Read end time
if len(sys.argv) >= 3:
    END_TIME = calendar.timegm(time.strptime(sys.argv[2], '%b %d, %Y @ %H:%M:%S UTC'))

#Read start time
if len(sys.argv) >= 4:
    START_TIME = calendar.timegm(time.strptime(sys.argv[3], '%b %d, %Y @ %H:%M:%S UTC'))

# init web client
# Token is Signing Secret of the slack app
client = slack.WebClient(token=os.environ['SLACK_TOKEN'])

messages_all = []

def collect_message(messages):
    global messages_all
    for msg in messages:
        if SEARCH_QUERY in msg['text'].lower():
            messages_all.append(msg['text'])

# get first page
page = 1
print("Retrieving page {}".format(page))
response = client.conversations_history(
    channel=CHANNEL_ID,
    limit=MESSAGES_PER_PAGE,
    latest=START_TIME,
    oldest=END_TIME
)
assert response["ok"]
collect_message(response['messages'])

# get additional pages if below max message and if they are any
while len(messages_all) + MESSAGES_PER_PAGE <= MAX_MESSAGES and response['has_more']:
    page += 1
    print("Retrieving page {}".format(page))
    sleep(1)   # need to wait 1 sec before next call due to rate limits
    response = client.conversations_history(
        channel=CHANNEL_ID,
        limit=MESSAGES_PER_PAGE,
        cursor=response['response_metadata']['next_cursor'],
        latest=START_TIME,
        oldest=END_TIME
    )
    assert response["ok"]
    collect_message(response['messages'])

print(
    "Search term {} was mentioned {} number of times in channel {}".format(
        sys.argv[1],
        len(messages_all),
        CHANNEL_ID
))
