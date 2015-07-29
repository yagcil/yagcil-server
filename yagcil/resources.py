"""
    API Server resources
"""
from flask.ext import restful
from yagcil import api


class TestResource(restful.Resource):
    """Test resource"""
    @staticmethod
    def get():
        """Get test dictionary
        :return dict
        """
        return {
            'test': 'yez'
        }


api.add_resource(TestResource, '/test')
