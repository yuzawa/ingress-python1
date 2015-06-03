# -*- coding:utf-8 -*-

import sys
sys.path.insert(1, '/Library/Python/2.7/site-packages')

from datetime import datetime
import os

from apiclient.discovery import build
from httplib2 import Http
import oauth2client
from oauth2client import client
from oauth2client import tools

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Gmail API Quickstart'

def get_attacker(service, id):
    message = service.users().messages().get(userId='me',id=id)


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'gmail-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatability with Python 2.6
            credentials = tools.run(flow, store)
        print 'Storing credentials to ' + credential_path
    return credentials

def main():
    """Shows basic usage of the Gmail API.

    Creates a Gmail API service object and outputs a list of label names
    of the user's Gmail account.
    """
    credentials = get_credentials()
    service = build('gmail', 'v1', http=credentials.authorize(Http()))

#    results = service.users().labels().list(userId='me').execute()
#    labels = results.get('labels', [])

    results = service.users().messages().list(userId='me',q="from:ingress-support@google.com" ).execute()
    messages = results.get('messages', [])

    if not messages:
        print 'No labels found.'
    else:
        print 'Messages:'
        for message in messages:
            print message['id']
            get_attacker(service, message['id'])


#    if not labels:
#        print 'No labels found.'
#    else:
#      print 'Labels:'
#      for label in labels:
#        print label['name']


if __name__ == '__main__':
    main()
