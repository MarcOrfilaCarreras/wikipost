from urllib.parse import unquote

import requests


def download_image(url: str, path: str = '/tmp', filename: str = None):
    if filename is None:
        filename = url.split('/')[-1]

    path = path[:len(filename)-1] if path.endswith('/') else path

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:135.0) Gecko/20100101 Firefox/135.0'
    }

    response = requests.get(url, headers=headers)
    if not response.ok:
        return None

    decoded_filename = unquote(filename)
    decoded_filename = decoded_filename.replace("'", '')
    decoded_filename = decoded_filename.replace('(', '')
    decoded_filename = decoded_filename.replace(')', '')

    with open(f'{path}/{decoded_filename}', 'wb') as handle:
        for block in response.iter_content(1024):
            if not block:
                break

            handle.write(block)

    return f'{path}/{decoded_filename}'
