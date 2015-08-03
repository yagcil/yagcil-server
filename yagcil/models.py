"""
    MongoDB data models
"""

import mongoengine as me


class Task(me.Document):
    """Task model

    :var key An unique task's id (in Melange database)
    :var student Name of the student who has finished the task
    :var categories A list of categories which the task is related to
    """
    key = me.IntField(required=True)
    student = me.StringField(required=True)
    categories = me.ListField(me.StringField())
    title = me.StringField(required=True)
