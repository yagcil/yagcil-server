"""
    MongoDB data models
"""

import mongoengine as me


class TestModel(me.Document):
    rotfl = me.StringField(required=True)
