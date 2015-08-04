"""
    API Server resources
"""
from flask.ext import restful
from flask.ext.restful import reqparse

from yagcil import app, api
from yagcil.models import Organization, Task
from yagcil.helpers import queryset_to_dict


class OrganizationListResource(restful.Resource):
    """Get a list of all organizations"""

    def __init__(self):
        self.arg_parser = reqparse.RequestParser()
        self.arg_parser.add_argument('year', type=int, help="GCI year")

    def get(self):
        """Get a list of all organizations

        :return list A list of all organizations
        """
        args = self.arg_parser.parse_args()
        year = args.get('year')
        if year is None:
            year = max(app.config['YEARS'])

        return queryset_to_dict(Organization.objects(year=year))


class OrganizationResource(restful.Resource):
    """Get organization data"""

    @staticmethod
    def get(name, year):
        """Get information about an organization

        :return dict A dictionary filled with org's information
        """
        return Organization.objects(
            name=name, year=year
        ).first().to_dict()


class TaskResource(restful.Resource):
    """Get task's data"""

    @staticmethod
    def get(task_id):
        """Get information about a task

        :param task_id int Task id from melange (key)
        :return dict A dictionary filled with task's data
        """
        return Task.objects(key=task_id).first().to_dict()


api.add_resource(OrganizationListResource, '/organization')
api.add_resource(OrganizationResource, '/organization/<name>/<int:year>')
api.add_resource(TaskResource, '/task/<int:task_id>')
