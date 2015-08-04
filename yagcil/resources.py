"""
    API Server resources
"""
import mongoengine as me
from flask.ext import restful

from flask.ext.restful import reqparse

from yagcil import app, api
from yagcil.models import Organization, Task
from yagcil.errorhandlers import ResourceNotFound, ErrorCode
from yagcil.helpers import queryset_to_dict


class OrganizationListResource(restful.Resource):
    """Get a list of all organizations"""

    def __init__(self):
        self.arg_parser = reqparse.RequestParser()
        self.arg_parser.add_argument(
            'year',
            type=int,
            default=max(app.config['YEARS']),
            help="GCI year"
        )

    def get(self):
        """Get a list of all organizations

        :return list A list of all organizations
        """
        args = self.arg_parser.parse_args()
        year = args.get('year')

        return queryset_to_dict(Organization.objects(year=year))


class OrganizationResource(restful.Resource):
    """Get organization data"""

    @staticmethod
    def get(name, year):
        """Get information about an organization

        :return dict A dictionary filled with org's information
        """
        try:
            org = Organization.objects.get(
                name=name, year=year
            )
        except me.DoesNotExist:
            return []

        return org.to_dict()


class TaskListResource(restful.Resource):
    """Get a list of all organizations"""

    def __init__(self):
        self.arg_parser = reqparse.RequestParser()
        self.arg_parser.add_argument(
            'org',
            help="Organization name (default: all tasks)"
        )
        self.arg_parser.add_argument(
            'year',
            type=int,
            default=max(app.config['YEARS']),
            help="GCI year"
        )
        self.arg_parser.add_argument(
            'limit',
            type=int,
            help="Results length limit"
        )
        self.arg_parser.add_argument(
            'offset',
            type=int,
            default=0,
            help="Results offset"
        )

    def get(self):
        """Get a list of all tasks

        :return list A list of all tasks
        """
        args = self.arg_parser.parse_args()
        org_name = args.get('org')
        year = args.get('year')
        limit = args.get('limit')
        offset = args.get('offset')

        query = Task.objects(year=year)
        if org_name:
            try:
                org = Organization.objects.get(name=org_name, year=year)
            except me.DoesNotExist:
                return []

            query = query(org=org)

        if limit is not None:
            query = query.limit(limit)

        query = query.skip(offset)

        return queryset_to_dict(query)


class TaskResource(restful.Resource):
    """Get task's data"""

    @staticmethod
    def get(task_id):
        """Get information about a task

        :param task_id int Task id from melange (key)
        :return dict A dictionary filled with task's data
        """
        try:
            task = Task.objects.get(key=task_id)
        except me.DoesNotExist:
            raise ResourceNotFound('Task not found', ErrorCode.TaskNotFound)

        return task.to_dict()


api.add_resource(OrganizationListResource, '/organization')
api.add_resource(OrganizationResource, '/organization/<name>/<int:year>')
api.add_resource(TaskListResource, '/task')
api.add_resource(TaskResource, '/task/<int:task_id>')
