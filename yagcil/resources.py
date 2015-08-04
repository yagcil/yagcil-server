"""
    API Server resources
"""
from flask.ext import restful
from flask.ext.restful import reqparse

from yagcil import app, api
from yagcil.models import Organization
from yagcil.helpers import queryset_to_dict


class OrganizationListResource(restful.Resource):
    """Get a list of all organizations"""

    def __init__(self):
        self.arg_parser = reqparse.RequestParser()
        self.arg_parser.add_argument('year', type=int, help="GCI year")

    def get(self):
        """Get a list of all organizations
        :return list
        """
        args = self.arg_parser.parse_args()
        year = args.get('year')
        if year is None:
            year = max(app.config['YEARS'])

        return queryset_to_dict(Organization.objects(year=year))


api.add_resource(OrganizationListResource, '/organization')
