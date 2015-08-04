"""Some useful functions"""
import json


def queryset_to_dict(queryset):
    """Convert MongoEngine QuerySet to Python dictionary

    :param queryset QuerySet A QuerySet to convert
    :return dict Dictionary filled with QuerySet's data
    """
    return json.loads(queryset.to_json())
