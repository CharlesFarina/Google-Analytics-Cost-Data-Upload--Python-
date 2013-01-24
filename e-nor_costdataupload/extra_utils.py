#!/usr/bin/python

import logging
import os
import sys
from apiclient.discovery import build
import gflags
import httplib2
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import OOB_CALLBACK_URN
from oauth2client.file import Storage
from oauth2client.tools import run


FLAGS = gflags.FLAGS

# CLIENT_SECRETS, name of a file containing the OAuth 2.0 information for this
# application, including client_id and client_secret. You get these values by
# creating a new project in the Google APIs console and registering for
# OAuth2.0 for installed applications: <https://code.google.com/apis/console>
CLIENT_SECRETS = 'client_secrets.json'


# Helpful message to display in the browser if the CLIENT_SECRETS file
# is missing.
MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0

To make this sample run you will need to populate the client_secrets.json file
found at:

   %s

with information from the APIs Console <https://code.google.com/apis/console>.

""" % os.path.join(os.path.dirname(__file__), CLIENT_SECRETS)

# Set up a Flow object to be used if we need to authenticate.
FLOW = flow_from_clientsecrets(CLIENT_SECRETS,
    scope='https://www.googleapis.com/auth/analytics',
    redirect_uri=OOB_CALLBACK_URN,
    message=MISSING_CLIENT_SECRETS_MESSAGE)

# The gflags module makes defining command-line options easy for applications.
# Run this program with the '--help' argument to see all the flags that it
# understands.
gflags.DEFINE_enum('logging_level', 'ERROR',
                   ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                   'Set the level of logging detail.')
gflags.DEFINE_integer('append_number', 1,
                   'Set the append number for this date.')
gflags.DEFINE_bool('reset_date', False,
                   'Reset data for input date.')


# Name of file that will store the access and refresh tokens to access
# the API without having to login each time. Make sure this file is in
# a secure place.
TOKEN_FILE_NAME = 'analytics.dat'


def process_flags(argv):
  """Uses the command-line flags to set the logging level.

  Args:
    argv: List of command line arguments passed to the python script.
  """

  # Let the gflags module process the command-line arguments.
  try:
    argv = FLAGS(argv)
  except gflags.FlagsError, e:
    print '%s\nUsage: %s ARGS\n%s' % (e, argv[0], FLAGS)
    sys.exit(1)

  # Set the logging according to the command-line flag.
  logging.getLogger().setLevel(getattr(logging, FLAGS.logging_level))

  return (argv, FLAGS.append_number, FLAGS.reset_date)


def initialize_service():
  """Returns an instance of service from discovery data and does auth.

  This method tries to read any existing OAuth 2.0 credentials from the
  Storage object. If the credentials do not exist, new credentials are
  obtained. The crdentials are used to authorize an http object. The
  http object is used to build the analytics service object.

  Returns:
    An analytics v3 service object.
  """

  # Create an httplib2.Http object to handle our HTTP requests.
  http = httplib2.Http()

  # Prepare credentials, and authorize HTTP object with them.
  storage = Storage(TOKEN_FILE_NAME)
  credentials = storage.get()
  if credentials is None or credentials.invalid:
    credentials = run(FLOW, storage)

  http = credentials.authorize(http)

  # Retrieve service.
  return build('analytics', 'v3', http=http)
