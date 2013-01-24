#!/usr/bin/python
# -*- coding: utf-8 -*-
#Code taken from code.google.com
#
#                             .ooooo.          ooo. .oo.     .ooooo.    oooo d8b
#                            d88" `88b         `888P"Y88b   d88" `88b   `888""8P
#                            888888888  88888   888   888   888   888    888
#                            888        88888   888   888   888   888    888      
#                            `"88888"          o888o o888o  `Y8bod8P"   d888b     
#
#****************************************************************************************************************
#     Upload Cost and Click Data to Google Analytics
#     Author: Nicholas Jagusiak and Charles Farina
#     Last Updated: 12/28/2012
#****************************************************************************************************************

import sys
import extra_utils

from apiclient.errors import HttpError
from oauth2client.client import AccessTokenRefreshError
from apiclient.http import MediaFileUpload


def main(argv):
  (argv, append_number, reset_date) = extra_utils.process_flags(argv)

  # Authenticate and construct service.
  service = extra_utils.initialize_service()

  # Try to make a request to the API. Print the results or handle errors.
  try:
    upload_return = upload_cost_file(service, argv[1], argv[2],
        append_number, reset_date)

  except TypeError, error:
    # Handle errors in constructing a query.
    print ('There was an error in constructing your query : %s' % error)

  except HttpError, error:
    # Handle API errors.
    print ('Arg, there was an API error : %s : %s' %
           (error.resp.status, error._get_reason()))

  except AccessTokenRefreshError:
    # Handle Auth errors.
    print ('The credentials have been revoked or expired, please re-run '
           'the application to re-authorize')


def upload_cost_file(service, upload_date, filename, append_number=1, reset_date=False):
  media = MediaFileUpload(
      filename, # The CSV file to upload
      mimetype='application/octet-stream',
      resumable=False)

  service.management().dailyUploads().upload (
      accountId='xxxxxx',  # Google Analytics Account Id,
      webPropertyId='UA-xxxxxxx-x',  # Web Property Id (child of the Account)
      customDataSourceId='xxxxxxxxxxxxxx',  # Custom Data Source Id (UID in Web Interface)
      date=upload_date,  # Upload Date
      appendNumber=append_number,  # The append number of the current upload
      reset=reset_date,  # Reset will delete any existing data for the date if set to true
      type='cost',  # Type of data being uploaded
      media_body=media).execute()

if __name__ == '__main__':
  main(sys.argv)
