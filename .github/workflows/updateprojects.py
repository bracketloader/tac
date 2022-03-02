#!/usr/bin/env python3                                                                                                  
#                                                                                                                       
# Copyright this project and it's contributors                                                                          
# SPDX-License-Identifier: Apache-2.0                                                                                   
#                                                                                                                       
# encoding=utf8

import csv
import urllib.request
import json
import os

projectsCsvFile = os.path.dirname(os.path.realpath(__file__))+'/../../_data/projects.csv'

landscapeBaseURL = 'https://landscape.openmainframeproject.org'
landscapeHostedProjects = landscapeBaseURL+'/data/exports/projects-hosted.json'
landscapeSingleItem = landscapeBaseURL+'/data/items/{}.json'

# map landscape ID to slug
keyMapping = {
    'open-mainframe-education': 'mainframe-open-education' 
}

csvRows = []

with urllib.request.urlopen(landscapeHostedProjects) as hostedProjectsResponse:
    for projectStage in json.load(hostedProjectsResponse):
        for project in projectStage['items']:
            with urllib.request.urlopen(landscapeSingleItem.format(project['id'])) as singleItemResponse:
                projectData = json.load(singleItemResponse)
                print("Processing {}...".format(projectData['name']))
                csvRows.append({
                        'Name': projectData['name'],
                        'Level': projectData['project'],
                        'Logo URL': project['logo'],
                        'Slug': projectData['id'],
                        'Website': projectData['homepage_url'],
                        'Leads': projectData['extra']['leads'] if 'extra' in projectData and 'leads' in projectData['extra'] else None,
                        'Meeting Cadence': projectData['extra']['meeting_cadence'] if 'extra' in projectData and 'meeting_cadence' in projectData['extra'] else None,
                        'LFX Insights URL': projectData['extra']['lfx_insights_url'] if 'extra' in projectData and 'lfx_insights_url' in projectData['extra'] else None,
                        'Accepted Date': projectData['extra']['date_accepted'] if 'extra' in projectData and 'date_accepted' in projectData['extra'] else None,
                        'Last Review Date': projectData['extra']['last_review_date'] if 'extra' in projectData and 'last_review_date' in projectData['extra'] else None,
                        'Next Review Date': projectData['extra']['next_review_date'] if 'extra' in projectData and 'next_review_date' in projectData['extra'] else None,
                        'Slack': projectData['extra']['slack_channel'] if 'extra' in projectData and 'slack_channel' in projectData['extra'] else None,
                        'Mailing List': projectData['extra']['mailing_list_url'] if 'extra' in projectData and 'mailing_list_url' in projectData['extra'] else None,
                        'User Mailing List': projectData['extra']['user_mailing_list_url'] if 'extra' in projectData and 'user_mailing_list_url' in projectData['extra'] else None,
                        'Dev Mailing List': projectData['extra']['dev_mailing_list_url'] if 'extra' in projectData and 'dev_mailing_list_url' in projectData['extra'] else None,
                        'Primary Github Repo': projectData['project_org'] if 'extra' in projectData and 'project_org' in projectData else None,
                        'Github Org': projectData['repo_url'] if 'extra' in projectData and 'repo_url' in projectData else None
                        })

with open(projectsCsvFile, 'w') as projectsCsvFileObject:
    writer = csv.DictWriter(projectsCsvFileObject, fieldnames = csvRows[0].keys())
    writer.writeheader() 
    writer.writerows(csvRows) 
