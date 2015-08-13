"""
    API Server resources
"""
from operator import itemgetter

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


class AllOrganizationListResource(restful.Resource):
    """Get a list of all organizations for every year"""

    def get(self):
        """Get a list of all organizations for every year

        :return list A list of all organizations for every year
        """
        result = []
        for year in app.config['YEARS']:
            result.append({
                'year': year,
                'orgs': queryset_to_dict(Organization.objects(year=year))
            })

        return result


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


class OrganizationRankResource(restful.Resource):
    """Get rank for organization/all orgs"""

    @staticmethod
    def get(name, year):
        """Get rank for a specified organization

        :param name str Organization name, use all to get rank of all orgs
        :param year int Year of GCI
        :return:
        """

        if name.lower() == 'all':
            tasks = Task.objects(year=year)
        else:
            try:
                org = Organization.objects.get(
                    name=name, year=year
                )
                tasks = Task.objects(org=org)
            except me.DoesNotExist:
                return []

        tasks_students = [x.student for x in tasks]
        rank = []
        for student in set(tasks_students):
            rank.append({
                'student': student,
                'tasks': tasks_students.count(student)
            })

        return sorted(rank, key=itemgetter('tasks'), reverse=True)


class OrganizationStatsResource(restful.Resource):
    """Return organization statistics"""

    @staticmethod
    def get(name, year):
        """Get org stats"""
        if name.lower() == 'all':
            categories = Task.count_categories(year)
        else:
            categories = Task.count_categories(year=year, org_name=name)

        return {
            'categories': categories
        }


class TaskListResource(restful.Resource):
    """Get a list of all organizations"""

    def __init__(self):
        self.arg_parser = reqparse.RequestParser()
        self.arg_parser.add_argument(
            'org',
            help="Organization name (default: all tasks)"
        )
        self.arg_parser.add_argument(
            'student',
            help="Student whose closed task should be returned"
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
        student = args.get('student')
        year = args.get('year')
        limit = args.get('limit')
        offset = args.get('offset')

        query = Task.objects(year=year)
        if org_name:
            try:
                org = Organization.objects.get(name=org_name, year=year)
            except me.DoesNotExist:
                return []

            query = query.filter(org=org)

        if student:
            query = query.filter(student=student)

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


class StudentResource(restful.Resource):
    """Return student's stats"""

    @staticmethod
    def get(name, year, org_name=None):
        """Get org stats"""
        tasks = Task.objects(student=name, year=year)
        if org_name is not None:
            try:
                org = Organization.objects.get(
                    name=org_name, year=year
                )
                tasks = tasks.filter(org=org)
            except me.DoesNotExist:
                return []

        categories = Task.count_categories(year=year, tasks=tasks)

        return {
            'student': name,
            'tasks': [task.to_dict() for task in tasks],
            'stats': {
                'categories': categories
            }
        }


class RootResource(restful.Resource):
    """Return links to all entry points"""

    @staticmethod
    def get():
        """Return links to all entry points

        :return dict All entry points
        """
        entry_points = {
            'configUrl': RootResource.__get_entry_point(
                '/config'
            ),
            'organizationListUrl': RootResource.__get_entry_point(
                '/organization{?year}'
            ),
            'organizationListAllUrl': RootResource.__get_entry_point(
                '/organization/all'
            ),
            'organizationUrl': RootResource.__get_entry_point(
                '/organization/{name}/{year}'
            ),
            'organizationRankUrl': RootResource.__get_entry_point(
                '/organization/{name}/{year}/rank'
            ),
            'organizationStatsUrl': RootResource.__get_entry_point(
                '/organization/{name}/{year}/stats'
            ),
            'studentUrl': RootResource.__get_entry_point(
                '/student/{name}/{year}{/org_name}'
            ),
            'taskListUrl': RootResource.__get_entry_point(
                '/task{?org,year,limit,offset}'
            ),
            'taskUrl': RootResource.__get_entry_point(
                '/task/{id}'
            )
        }
        return entry_points

    @staticmethod
    def __get_entry_point(resource):
        """Return an url to API entry point

        :param resource str Resource url to get the entry point
        :return str Entry point URL
        """
        return '{server_name}{resource}'.format(
            server_name=app.config.get('SERVER_URL'),
            resource=resource
        )


class ConfigResource(restful.Resource):
    """Get yagcil config"""

    @staticmethod
    def get():
        return {
            'activeYear': max(app.config['YEARS']),
            'years': app.config['YEARS']
        }

api.add_resource(OrganizationListResource, '/organization')
api.add_resource(AllOrganizationListResource, '/organization/all')
api.add_resource(OrganizationResource, '/organization/<name>/<int:year>')
api.add_resource(OrganizationRankResource, '/organization/<name>/<int:year>/rank')
api.add_resource(OrganizationStatsResource, '/organization/<name>/<int:year>/stats')

api.add_resource(TaskListResource, '/task')
api.add_resource(TaskResource, '/task/<int:task_id>')

api.add_resource(
    StudentResource,
    '/student/<name>/<int:year>',
    '/student/<name>/<int:year>/<org_name>/'
)

api.add_resource(RootResource, '/')
api.add_resource(ConfigResource, '/config')
