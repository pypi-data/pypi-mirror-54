"""Bot"""
import logging
import yaml

import slack
from playsound import playsound


class Bot:
    """Read the config file, subscribe to RTM events, parse messages and play sounds.

    Args:
        config (file): The config YAML file
    """

    def __init__(self, config):
        self._logger = self._get_logger()
        self._config = self._load_config(config)

        slack.RTMClient.run_on(event="message")(self._read_message)
        slack.RTMClient.run_on(event="hello")(self._hello)

    @staticmethod
    def _load_config(config):
        """Load the config"""
        return yaml.safe_load(config)

    @staticmethod
    def _get_logger():
        """Configure the logger"""
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)

        logger_handler = logging.StreamHandler()
        logger_handler.setLevel(logging.INFO)

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        logger_handler.setFormatter(formatter)
        logger.addHandler(logger_handler)

        return logger

    def _hello(self, **_payload):
        """Log if client connected successfully

        Args:
            **_payload (dict): Slack RTM payload
        """
        self._logger.info("client connected")

    def _read_message(self, **payload):
        """Read messages, extract trigger words and play sounds.

        Args:
            **payload (dict): Slack RTM payload
        """
        message_text = payload["data"].get("text", [])

        for trigger in self._config["triggers"]:
            if trigger["trigger"] in message_text:
                self._play_sound(trigger["sound"])

    def _play_sound(self, sound):
        """Play sounds from a mp3 or wav file.

        Args:
            sound (str): File path to a mp3 or wav file
        """
        self._logger.info("playing %s", sound)
        playsound(sound)
