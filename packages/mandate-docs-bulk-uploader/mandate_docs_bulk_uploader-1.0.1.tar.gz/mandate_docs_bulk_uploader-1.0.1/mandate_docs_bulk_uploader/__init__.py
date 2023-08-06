import os
from os import walk

import click
import requests


def upload_doc(mandate_id, file, api_url, token):
    print(
        requests.post(
            api_url,
            data={
                'type': '/api/crm/document_types/RMP',
                'investorMandates': [mandate_id]
            },
            files={
                'file': open(file, 'rb')
            },
            headers={
                'Authorization': 'Bearer {}'.format(token)
            }
        ).json()
    )


def valid_file(file):
    return file.endswith('xls') or file.endswith('xlsx') or file.endswith('csv')


@click.command()
@click.option('-p', '--path')
@click.option('-a', '--crosslend_api_url')
@click.option('-t', '--token')
def tool(path, api_url, token):
    for root, dirs, files in walk(path):
        for file in files:
            if valid_file(file):
                mandate_id = root.split('/')[-1]
                upload_doc(mandate_id, os.path.join(root, file), api_url, token)
