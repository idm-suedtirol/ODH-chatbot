from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)
from typing import Text, List, Dict, Any, Callable
import yaml
import os

from flask import Blueprint, request, jsonify
import requests
from rasa_core.channels.facebook import Messenger as FBMessenger, MessengerBot as FBMessengerBot, FacebookInput as FBFacebookInput, UserMessage

class Messenger(FBMessenger):
    """Implement a fbmessenger to parse incoming webhooks and send msgs."""

    def __init__(self, page_access_token, on_new_message):
        super(Messenger, self).__init__(page_access_token, on_new_message)

    def _handle_user_message(self, text, sender_id):
        # type: (Text, Text) -> None
        """Pass on the text to the dialogue engine for processing."""

        out_channel = MessengerBot(self.client)
        user_msg = UserMessage(text, out_channel, sender_id,
                               input_channel=self.name())

        # noinspection PyBroadException
        try:
            self.on_new_message(user_msg)
        except Exception:
            logger.exception("Exception when trying to handle webhook "
                             "for facebook message.")
            pass


class MessengerBot(FBMessengerBot):
    """A bot that uses fb-messenger to communicate."""

    def __init__(self, messenger_client):
        # type: (MessengerClient) -> None
        super(MessengerBot, self).__init__(messenger_client)

    def send_custom_message(self, recipient_id, elements):
        # type: (Text, List[Dict[Text, Any]]) -> None
        """Sends elements to the output."""

        payload = {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": elements
                }
            }
        }
        self.messenger_client.send(payload,
                                   self._recipient_json(recipient_id),
                                   'RESPONSE')


class FacebookInput(FBFacebookInput):
    """Facebook input channel implementation. Based on the HTTPInputChannel."""

    def __init__(self, fb_verify, fb_secret, fb_access_token):
        super(FacebookInput, self).__init__(fb_verify, fb_secret, fb_access_token)

    def blueprint(self, on_new_message):

        fb_webhook = Blueprint('fb_webhook', __name__)

        @fb_webhook.route("/", methods=['GET'])
        def health():
            return jsonify({"status": "ok"})

        @fb_webhook.route("/webhook", methods=['GET'])
        def token_verification():
            if request.args.get("hub.verify_token") == self.fb_verify:
                return request.args.get("hub.challenge")
            else:
                logger.warning(
                        "Invalid fb verify token! Make sure this matches "
                        "your webhook settings on the facebook app.")
                return "failure, invalid token"

        @fb_webhook.route("/webhook", methods=['POST'])
        def webhook():
            signature = request.headers.get("X-Hub-Signature") or ''
            if not self.validate_hub_signature(self.fb_secret, request.data,
                                               signature):
                logger.warning("Wrong fb secret! Make sure this matches the "
                               "secret in your facebook app settings")
                return "not validated"

            messenger = Messenger(self.fb_access_token, on_new_message)

            messenger.handle(request.get_json(force=True))
            return "success"

        return fb_webhook
