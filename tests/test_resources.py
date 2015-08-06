#!/usr/bin/env python
"""Test API Server resources"""
import unittest
import json

import mongoengine as me

from yagcil import app
from yagcil.models import Organization, Task

TEST_DB_NAME = 'yagcil-test'


class YagcilTestCase(unittest.TestCase):
    def __setupDatabase(self):
        """Connect to the testing database and add some entries"""
        self.db = me.connect('TEST_DB_NAME')
        # Reset the database
        self.db.drop_database('TEST_DB_NAME')
        # Add few test entries to the database
        orgs = [
            Organization(name='orga', full_name='Org A', year=2012),
            Organization(name='orgb', full_name='Org B', year=2012),
            Organization(name='orga', full_name='Org A', year=2011),
            Organization(name='orgc', full_name='Org C', year=2011),
            Organization(name='orgd', full_name='Org D', year=2011)
        ]
        self.orgs_added = {
            2011: 3,
            2012: 2
        }
        for org in orgs:
            org.save()

        tasks = [
            Task(key=1, year=2012, org=orgs[0], student='Student A', title='Task A'),
            Task(key=2, year=2012, org=orgs[1], student='Student B', title='Task B')
        ]
        self.tasks_added = {
            2012: 2
        }
        for task in tasks:
            task.save()

    def setUp(self):
        self.__setupDatabase()
        self.years = app.config['YEARS'] = [2011, 2012]
        self.active_year = max(self.years)

        self.app = app.test_client()

    def tearDown(self):
        self.db.drop_database('TEST_DB_NAME')

    def test_organization_list(self):
        rv = self.app.get('/organization')
        orgs = json.loads(rv.data)
        self.assertEqual(len(orgs), self.orgs_added[self.active_year])

        rv = self.app.get('/organization?year=2011')
        orgs = json.loads(rv.data)
        self.assertEqual(len(orgs), self.orgs_added[2011])

    def test_organization(self):
        rv = self.app.get('/organization/orgc/2011')
        org = json.loads(rv.data)

        self.assertEqual(org['name'], 'orgc')
        self.assertEqual(org['fullName'], 'Org C')
        self.assertEqual(org['year'], 2011)

    def test_task(self):
        rv = self.app.get('/task/2')
        task = json.loads(rv.data)

        self.assertEqual(task['id'], 2)
        self.assertEqual(task['title'], 'Task B')
        self.assertEqual(task['student'], 'Student B')
        self.assertEqual(task['year'], 2012)
        self.assertEqual(task['orgName'], 'orgb')


if __name__ == '__main__':
    unittest.main()
