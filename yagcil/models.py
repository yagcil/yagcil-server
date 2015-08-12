"""
    MongoDB data models
"""

import mongoengine as me


class Organization(me.Document):
    """Organization model

    :var name Short name of the organization, e.g., brlcad, sugarlabs
    :var full_name Full (might be unsafe)
    :var year Year which the org was in
    name of the organization, e.g., BRL-CAD, Sugar Labs
    """
    name = me.StringField(required=True)
    full_name = me.StringField()
    year = me.IntField(required=True)

    def to_dict(self):
        """Serialize Organization data

        :return dict Serialized Organization data
        """
        return {
            'name': self.name,
            'fullName': self.full_name,
            'year': self.year
        }


class Task(me.Document):
    """Task model

    :var key An unique task's id (in Melange database)
    :var year The year which the task belongs to
    :var org_id Id of the org that created the task
    :var student Name of the student who has finished the task
    :var categories A list of categories which the task is related to
    :var title Task's title
    """
    key = me.IntField(required=True, primary_key=True)
    year = me.IntField(required=True)
    org = me.ReferenceField('Organization')
    student = me.StringField(required=True)
    categories = me.ListField(me.StringField())
    title = me.StringField(required=True)

    def to_dict(self):
        """Serialize Task data

        :return dict Serialized Task data
        """
        return {
            'id': self.key,
            'title': self.title,
            'orgName': self.org.name,
            'year': self.year,
            'student': self.student,
            'categories': self.categories
        }

    @staticmethod
    def count_categories(year, org_name=None, student=None, tasks=None):
        """Get categories count by an organization or a student

        :param year int GCI Year
        :param org_name str Organization's name
        :param student str Student's name
        :param tasks list(Task) Optional list of tasks to work on

        :return dict A number of tasks in each category
                     e.g, { 'Category': number of tasks }
        """
        if tasks is None:
            tasks = Task.objects(year=year)

        if org_name is not None:
            try:
                org = Organization.objects.get(
                    name=org_name, year=year
                )
                tasks = Task.objects(org=org)
            except me.DoesNotExist:
                return []

        if student is not None:
            tasks = tasks.filter(student=student)

        categories = {}
        for task in tasks:
            for category in task.categories:
                categories[category] = categories.get(category, 0) + 1

        return categories
