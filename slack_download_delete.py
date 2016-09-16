import requests
import time
import json
import urllib.request

token = ''

# Delete files older than this:
ts_to = int(time.time()) - 30 * 24 * 60 * 60


def list_files():
    params = {
        'token': token
        , 'ts_to': ts_to
        , 'count': 1000
    }
    uri = 'https://slack.com/api/files.list'
    response = requests.get(uri, params=params)
    return json.loads(response.text)['files']


def download_files(files, delete=False):
    count = 0
    num_files = len(files)
    for file in files:
        count = count + 1

        header = {
            'Authorization': ('Bearer ' + token)
        }

        if 'url_private_download' in file:
            r = requests.get(file['url_private_download'], headers=header, stream=True)
            if r.status_code == 200:
                with open((file['id'] + '_' + file['name']), 'wb') as f:
                    for chunk in r:
                        f.write(chunk)

            if delete:
                params = {
                    'token': token
                    , 'file': file['id']
                }
                delete_uri = 'https://slack.com/api/files.delete'
                response = requests.get(delete_uri, params=params)
                print(count, "of", num_files, " deleted -", file['id'], json.loads(response.text)['ok'])

            print(count, "of", num_files, "-", file['id'])
            print(file['url_private_download'])

files = list_files()
download_files(files, delete=True)