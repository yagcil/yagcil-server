"""
    MongoDB data models
"""

import mongoengine as me


class Organization(me.Document):
    """Organization model

    :var name Short name of the organization, e.g., brlcad, sugarlabs
    :var full_name Full (might be unsafe)
    name of the organization, e.g., BRL-CAD, Sugar Labs
    """
    name = me.StringField(required=True)
    full_name = me.StringField()


class Task(me.Document):
    """Task model

    :var key An unique task's id (in Melange database)
    :var year The year which the task belongs to
    :var org_id Id of the org that created the task
    :var student Name of the student who has finished the task
    :var categories A list of categories which the task is related to
    :var title Task's title
    """
    key = me.IntField(required=True)
    year = me.IntField(required=True)
    org = me.ReferenceField('Organization')
    student = me.StringField(required=True)
    categories = me.ListField(me.StringField())
    title = me.StringField(required=True)
