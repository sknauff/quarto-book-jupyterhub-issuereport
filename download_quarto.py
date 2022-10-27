import requests
import json
import hashlib

def download_newest_quarto(LOCAL_QUARTO_DOWNLOAD_PATH_AND_NAME = '/tmp/quarto.deb'):
    # get json of quarto releases
    r = requests.get('https://api.github.com/repos/quarto-dev/quarto-cli/releases/tags/v1.2.247')
    j = json.loads(r.text)

    # select assets from newest release
    j_assets = j['assets']

    # download deb-package
    deb_browser_download_url = [x for x in j_assets if x['content_type'] == "application/deb"][0]['browser_download_url']
    r = requests.get(deb_browser_download_url, allow_redirects=True)
    with open(LOCAL_QUARTO_DOWNLOAD_PATH_AND_NAME, 'wb') as f:
        f.write(r.content)

    # get expected checksum
    sha256sum_browser_download_url = [x for x in j_assets if x['content_type'] == "text/plain"][0]['browser_download_url']
    r = requests.get(sha256sum_browser_download_url)
    deb_expected_check_sum = [x for x in r.text.splitlines() if x.endswith('-linux-amd64.deb')][0].split()[0]

    # get local checksum
    with open(LOCAL_QUARTO_DOWNLOAD_PATH_AND_NAME, 'rb') as f:
        f_bytes = f.read()
        deb_file_check_sum = hashlib.sha256(f_bytes).hexdigest()

    # raise exception, if local checksum deviates from expected checksum
    if deb_expected_check_sum != deb_file_check_sum:
        raise ValueError("Missmatch: sha256 checksum")
        sys.exit(1)


if __name__ == '__main__':
    download_newest_quarto()