import sys, os, json, time
from random import randint
import argparse

import parsl
print(parsl.__version__, flush = True)

import parsl_utils
from parsl_utils.config import config,exec_conf
from parsl_utils.data_provider import PWFile

from workflow_apps import *

def read_args():
    parser=argparse.ArgumentParser()
    parsed, unknown = parser.parse_known_args()
    for arg in unknown:
        if arg.startswith(("-", "--")):
            parser.add_argument(arg)
    pwargs=vars(parser.parse_args())
    print(pwargs)
    return pwargs

if __name__ == '__main__':
    args = read_args()
    job_number = args['job_number']

    print('Loading Parsl Config', flush = True)
    parsl.load(config)

    print('\n\n\nHELLO PYTHON APP:', flush = True)
    fut_1 = hello_python_app_1(name = args['name'])


    print('\n\n\nHELLO BASH APP:', flush = True)
    print('\n\nmyexecutor_1:', flush = True)
    fut_2 = hello_bash_app_1(
        fut_1,
        run_dir = exec_conf['myexecutor_1']['RUN_DIR'],
        inputs = [ 
            PWFile(
                url = 'file://usercontainer/{cwd}/hello_srun.in'.format(cwd = os.getcwd()),
                local_path = '{remote_dir}/inputs/hello_srun.in'.format(remote_dir =  exec_conf['myexecutor_1']['RUN_DIR'])
            )
        ],
        outputs = [
            PWFile(
                url = 'file://usercontainer/{cwd}/outputs/hello_srun-1.out'.format(cwd = os.getcwd()),
                local_path = '{remote_dir}/hello_srun-1.out'.format(remote_dir =  exec_conf['myexecutor_1']['RUN_DIR'])
            )
        ],
        stdout = os.path.join(exec_conf['myexecutor_1']['RUN_DIR'], 'std.out'),
        stderr = os.path.join(exec_conf['myexecutor_1']['RUN_DIR'], 'std.err')
    )

    if args['test_gsutil'] == 'True':
        print('\n\n\nHELLO BASH APP WITH GSUTIL:', flush = True)
        print('\n\nmyexecutor_1:', flush = True)
        fut_3 = hello_bash_app_1(
            fut_2,
            run_dir = exec_conf['myexecutor_1']['RUN_DIR'],
            inputs = [ 
                PWFile(
                    url = 'gs://bucket/demoworkflows/parsl_demo/hello.in',
                    local_path = '{remote_dir}/hello.in'.format(remote_dir =  exec_conf['myexecutor_1']['RUN_DIR'])
                )
            ],
            outputs = [
                PWFile(
                    url = 'gs://bucket/demoworkflows/parsl_demo/hello.out',
                    local_path = '{remote_dir}/hello.out'.format(remote_dir =  exec_conf['myexecutor_1']['RUN_DIR'])
                )
            ],
            stdout = os.path.join(exec_conf['myexecutor_1']['RUN_DIR'], 'std-gs.out'),
            stderr = os.path.join(exec_conf['myexecutor_1']['RUN_DIR'], 'std-gs.err')
        )
        fut_3.result()
    else:
        fut_2.result()

