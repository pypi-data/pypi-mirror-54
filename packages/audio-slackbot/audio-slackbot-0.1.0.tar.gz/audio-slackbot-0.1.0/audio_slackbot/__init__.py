"""A Slack bot which plays sounds from the filesystem upon certain triggers. Install and configure
it on a RaspberryPi, connect some speakers and have fun.
"""
import os
import argparse

import slack

from .bot import Bot


def run():
    """Main method"""
    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument(
        "--config", type=argparse.FileType("r"), help="path to the configuration file"
    )
    args = parser.parse_args()

    Bot(args.config)

    slack_token = os.environ["SLACK_API_TOKEN"]
    rtm_client = slack.RTMClient(token=slack_token)
    rtm_client.start()
