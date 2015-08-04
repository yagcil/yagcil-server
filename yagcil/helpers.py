"""Some useful functions"""


def queryset_to_dict(queryset):
    """Convert MongoEngine QuerySet to Python dictionary

    :param queryset QuerySet A QuerySet to convert
    :return dict Dictionary filled with QuerySet's data
    """
    result = []
    for item in queryset:
        result.append(item.to_dict())

    return result
