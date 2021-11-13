"""
This class was modified and adjusted.
The original class find in this link:
https://github.com/licht1stein/ptb-firebase-persistence
User: https://github.com/licht1stein
"""
import json
import os
from ast import literal_eval
import firebase_admin
from firebase_admin import db
from telegram.ext import DictPersistence

class FirebasePersistence(DictPersistence):
    def __init__(
        self,
        database_url: str,
        credentials: dict,
        auth: str,
        store_user_data=True,
        store_chat_data=True,
        store_bot_data=True,
    ):
        cred = firebase_admin.credentials.Certificate(credentials)
        self.app = firebase_admin.initialize_app(cred, {"databaseURL": database_url,
                                                        'databaseAuthVariableOverride': {
                                                        'uid': auth}})
        self.fb_chat_data = db.reference("chat_data")
        self.fb_conversations = db.reference("conversations")
        super().__init__(
            store_user_data=store_user_data,
            store_chat_data=store_chat_data,
            store_bot_data=store_bot_data,
        )

    @classmethod
    def from_environment(cls, **kwargs):
        credentials = json.loads(os.environ["FIREBASE_CREDENTIALS"])
        database_url = os.environ["FIREBASE_URL"]
        auth = os.environ['FIREBASE_AUTH']
        return cls(database_url=database_url, credentials=credentials, auth=auth, **kwargs)

    def get_chat_data_(self, user_id, name):
        data = self.fb_chat_data.child(str(user_id)).child(name).get()
        return data

    def get_conversations(self, name):
        res = self.fb_conversations.child(name).get() or {}
        res = {literal_eval(k): v for k, v in res.items()}
        return res

    def update_conversation(self, name, key, new_state):
        if new_state:
            self.fb_conversations.child(name).child(str(key)).set(new_state)
        else:
            self.fb_conversations.child(name).child(str(key)).delete()

    def update_chat_data_(self, chat_id, data):
        self.fb_chat_data.child(str(chat_id)).update(data)

