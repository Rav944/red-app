import pprint
import time
from json import JSONDecodeError

import argh
import requests

from settings import GET_DATA_ADDRESS, CLONE_ADDRESS, REMOVE_ADDRESS


def get() -> None:
    """
    Print CPU and OS data.
    """
    r = requests.get(GET_DATA_ADDRESS)
    pprint.pprint(r.json())


@argh.arg('repo', choices=['node-hello', 'nodejs-sample'])
def clone(repo: str, minutes=5) -> None:
    """
    Clone and build project from given repo.
    """
    sec_in_min = 60 * 5
    payload = {'repo': repo}
    try:
        r = requests.get(CLONE_ADDRESS, params=payload, timeout=sec_in_min)
    except requests.exceptions.ReadTimeout:
        print('Debugging in progress...')
        clone(repo, minutes)
    else:
        if r.status_code != 200:
            try:
                response_message = r.json()
            except JSONDecodeError:
                print("Unclassified server error !")
            else:
                print(f'{response_message.get("type")}: {response_message.get("message")}', end='\n')
                print('Debugging initiation:\n')
            finally:
                time.sleep(sec_in_min)
                clone(repo, minutes)
        print('Cloning and building was successful')


@argh.arg('repo', choices=['node-hello', 'nodejs-sample'])
def clean_repo(repo: str) -> None:
    """
    Remove selected repo from machine.
    """
    payload = {'repo': repo}
    r = requests.get(REMOVE_ADDRESS, params=payload)
    if r.status_code == 200:
        print("Removal completed successfully ")
    else:
        response_message = r.json()
        print(f'{response_message.get("type")}: {response_message.get("message")}', end='\n')


if __name__ == '__main__':
    argh.dispatch_commands([get, clone, clean_repo])
