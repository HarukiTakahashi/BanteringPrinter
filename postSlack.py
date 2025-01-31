import os
import time
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import time, datetime
import threading

class Slack:

    def __init__(self, token, channel,id):
        self.SLACK_TOKEN = token
        self.SLACK_CHANNEL = channel
        self.SLACK_MEMBER_ID = id
        self.ENABLE = False
        self.client = WebClient(token=self.SLACK_TOKEN)

    def post(self, mes, notification=False):
        if self.ENABLE is False:
            return
        
        d = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        
        if notification:
            m = "<@" + self.SLACK_MEMBER_ID + ">\n" + d + "\n" + mes
        else:
            m = d + "\n" + mes
        
        try:
            response = self.client.chat_postMessage(
                channel=self.SLACK_CHANNEL,
                text=m
            )
        except Exception as e:
            print("Slack post error")

    def enable(self, b):
        self.ENABLE = b

