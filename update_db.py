#!/usr/bin/env python
"""Update yagcil's database"""
import sys
import logging
import argparse
import json
import requests

from yagcil import app
from yagcil.models import Task, Organization


class Crawler(object):
    URLS = {
        'TASKS': 'http://www.google-melange.com/gci/org/google/'
                 'gci{year}/{orgname}?fmt=json&limit=1000&idx=1',
        'ORGS': 'https://www.google-melange.com/gci/org/'
                'list/public/google/gci{year}?fmt=json'
    }

    def __init__(self, logger):
        self.years = sorted(app.config['YEARS'])
        self.active_year = max(self.years)
        self.archive_years = filter(
            lambda x: x != self.active_year, self.years
        )

        self.logger = logger

    def __fetch_org_tasks_by_year(self, org, year):
        url = self.URLS['TASKS'].format(orgname=org.name, year=year)
        self.logger.info('Getting %d/%s', year, org.name)
        self.logger.debug('Fetching %s', url)

        r = requests.get(url)
        fetched_tasks = json.loads(r.text).get('data').get('')
        self.logger.info('Got %d tasks', len(fetched_tasks))
        for fetched_task in fetched_tasks:
            fetched_task = fetched_task.get('columns')
            task = Task.objects(key=fetched_task.get('key')).first()
            if not task:
                # New task
                Task(
                    key=fetched_task.get('key'),
                    year=year,
                    org=org,
                    student=fetched_task.get('student'),
                    title=fetched_task.get('title'),
                    categories=fetched_task.get('types').split(', ')
                ).save()

    def __fetch_year(self, year):
        """Fetch specified year"""
        # Get all the organizations from this year
        url = self.URLS['ORGS'].format(year=year)
        self.logger.info('Getting list of the organizations for %d', year)
        self.logger.debug('Fetching %s', url)

        r = requests.get(url)
        fetched_orgs = json.loads(r.text).get('data').get('')
        self.logger.info('Got %d organizations', len(fetched_orgs))
        for fetched_org in fetched_orgs:
            fetched_org = fetched_org.get('columns')
            org = Organization.objects(name=fetched_org.get('name')).first()
            if not org:
                # Add new org
                org = Organization(
                    name=fetched_org.get('org_id'),
                    full_name=fetched_org.get('name'),
                    year=year
                )
                org.save()

            self.__fetch_org_tasks_by_year(
                org, year
            )

    def fetch_active_year(self):
        """Fetch active year"""
        self.__fetch_year(self.active_year)

    def fetch_archive(self):
        """Fetch archive years"""
        for year in self.archive_years:
            self.__fetch_year(year)

    def fetch_all(self):
        self.fetch_archive()
        self.fetch_active_year()


def get_args():
    parser = argparse.ArgumentParser(
        description='Crawl closed tasks from GCI Melange (SoC)'
    )
    parser.add_argument(
        '--all',
        action='store_true',
        help='Fetch all years',
        default=False
    )
    parser.add_argument(
        '--active-year',
        action='store_true',
        help='Fetch active year',
        default=True
    )
    parser.add_argument(
        '--archive',
        action='store_true',
        help='Fetch all years excluding the active year',
        default=False
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Be verbose',
        default=False
    )
    parser.add_argument(
        '-d', '--debug',
        action='store_true',
        help='Enable debug information',
        default=False
    )

    return parser.parse_args()


def main():
    args = get_args()
    # Setup logging
    logging.basicConfig()
    logger = logging.getLogger('yagcil-crawler')
    if args.verbose:
        logger.setLevel(logging.INFO)

    if args.debug:
        logger.setLevel(logging.DEBUG)

    crawler = Crawler(logger)
    if args.all:
        crawler.fetch_all()
        return

    if args.active_year:
        crawler.fetch_active_year()

    if args.archive:
        crawler.fetch_archive()

    sys.exit(0)

if __name__ == '__main__':
    main()
