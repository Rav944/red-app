import pprint
import sys
import time
from retrying import retry

import argh
import requests

from settings import GET_DATA_ADDRESS, CLONE_ADDRESS, REMOVE_ADDRESS


def timer(attempts, delay) -> None:
    for remaining in range(60*5, 0, -1):
        sys.stdout.write("\r")
        sys.stdout.write("Time to DEBUG !!! {:2d} seconds remaining.".format(remaining))
        sys.stdout.flush()
        time.sleep(1)


def get() -> None:
    """
    Print CPU and OS data.
    """
    r = requests.get(GET_DATA_ADDRESS)
    pprint.pprint(r.json())


@argh.arg('repo', choices=['node-hello', 'nodejs-sample'])
@retry(wait_func=timer)
def clone(repo: str) -> None:
    """
    Clone and build project from given repo.
    """
    payload = {'repo': repo}
    r = requests.get(CLONE_ADDRESS, params=payload)
    if r.status_code != 200:
        response_message = r.json()
        print(f'{response_message.get("type")}: {response_message.get("message")}', end='\n')
        raise
    print("Cloning and building was successful")


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
