import platform
import subprocess

import psutil
from flask import Flask, request, jsonify

from clone import Clone
from settings import REPOSITORIES
from utils import make_error

app = Flask(__name__)
app.config["DEBUG"] = True


@app.route('/api/get_os_and_cpu_data', methods=['GET'])
def get_os_and_cpu_data():
    uname = platform.uname()
    cpu_frequency = psutil.cpu_freq()
    data = {
        'system_data': {
            'system': uname.system,
            'node name': uname.node,
            'release': uname.release,
            'version': uname.version,
            'machine': uname.machine,
            'processor': uname.processor
        },
        'cpu_data': {
            'physical cores': psutil.cpu_count(logical=False),
            'total cores': psutil.cpu_count(logical=True),
            'max frequency': cpu_frequency.max,
            'min frequency': cpu_frequency.min,
            'current frequency': cpu_frequency.current,
            'cores': [{f'Core {i}': f'{per}%'} for i, per in enumerate(psutil.cpu_percent(percpu=True, interval=1))]
        }
    }
    return jsonify(data)


@app.route('/api/clone_repo', methods=['GET'])
def clone_repo():
    repo = request.args.get('repo')
    if repo and repo in REPOSITORIES:
        clone_process = Clone(repo)
        response = jsonify(success=True) if not clone_process.errors else clone_process.errors
        return response


@app.route('/api/remove_repo', methods=['GET'])
def remove_repo():
    repo = request.args.get('repo')
    if repo and repo in REPOSITORIES:
        remove = subprocess.run(f"rm -rf {repo}", shell=True, capture_output=True, text=True, timeout=60)
        if remove.returncode != 0:
            return make_error(500, f'Npm {a} error', remove.stderr)
        return jsonify(success=True)
    else:
        return make_error(400, 'Incorrect repo selected ', '')


if __name__ == '__main__':
    app.run()
