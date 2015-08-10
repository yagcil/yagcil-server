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
        self.db = me.connect(TEST_DB_NAME)
        # Reset the database
        self.db.drop_database(TEST_DB_NAME)
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
            Task(key=2, year=2012, org=orgs[1], student='Student B', title='Task B'),
            Task(key=3, year=2012, org=orgs[0], student='Student A', title='Task A')
        ]
        self.tasks_added = {
            'all': 3,
            'orga': 2,
            'orgb': 1,
            'st_A': 2,
            'st_B': 1,
            'st_A_orga': 2,
            2012: 3,
            2011: 0
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
        orgs = json.loads(rv.data.decode())
        self.assertEqual(len(orgs), self.orgs_added[self.active_year])

        rv = self.app.get('/organization?year=2011')
        orgs = json.loads(rv.data.decode())
        self.assertEqual(len(orgs), self.orgs_added[2011])

    def test_all_organization_list(self):
        rv = self.app.get('/organization/all')
        orgs = json.loads(rv.data.decode())
        self.assertEqual(len(orgs), 2)

    def test_organization(self):
        rv = self.app.get('/organization/orgc/2011')
        org = json.loads(rv.data.decode())

        self.assertEqual(org['name'], 'orgc')
        self.assertEqual(org['fullName'], 'Org C')
        self.assertEqual(org['year'], 2011)

    def test_task_list(self):
        rv = self.app.get('/task')
        tasks = json.loads(rv.data.decode())
        self.assertEqual(len(tasks), self.tasks_added[self.active_year])

        rv = self.app.get('/task?org=orga')
        tasks = json.loads(rv.data.decode())
        self.assertEqual(len(tasks), self.tasks_added['orga'])

        rv = self.app.get('/task?year=2011')
        tasks = json.loads(rv.data.decode())
        self.assertEqual(len(tasks), self.tasks_added[2011])

        rv = self.app.get('/task?limit=1')
        tasks = json.loads(rv.data.decode())
        self.assertEqual(len(tasks), 1)

        rv = self.app.get('/task?offset=1')
        tasks = json.loads(rv.data.decode())
        self.assertEqual(len(tasks), self.tasks_added['all'] - 1)

        rv = self.app.get('/task?student=Student A')
        tasks = json.loads(rv.data.decode())
        self.assertEqual(len(tasks), self.tasks_added['st_A'])

    def test_task(self):
        rv = self.app.get('/task/2')
        task = json.loads(rv.data.decode())

        self.assertEqual(task['id'], 2)
        self.assertEqual(task['title'], 'Task B')
        self.assertEqual(task['student'], 'Student B')
        self.assertEqual(task['year'], 2012)
        self.assertEqual(task['orgName'], 'orgb')

    def test_rank(self):
        rv = self.app.get('/organization/orga/2012/rank')
        rank = json.loads(rv.data.decode())
        self.assertEqual(rank[0]['student'], 'Student A')
        self.assertEqual(rank[0]['tasks'], self.tasks_added['st_A_orga'])

        rv = self.app.get('/organization/all/2012/rank')
        rank = json.loads(rv.data.decode())
        self.assertEqual(rank[0]['student'], 'Student A')
        self.assertEqual(rank[0]['tasks'], self.tasks_added['st_A'])
        self.assertEqual(rank[1]['student'], 'Student B')
        self.assertEqual(rank[1]['tasks'], self.tasks_added['st_B'])

    def test_root(self):
        rv = self.app.get('/')
        root = json.loads(rv.data.decode())
        self.assertGreater(len(root), 0)

    def test_config(self):
        rv = self.app.get('/config')
        config = json.loads(rv.data.decode())
        self.assertDictEqual(config, {
            'activeYear': self.active_year,
            'years': self.years
        })


if __name__ == '__main__':
    unittest.main()
