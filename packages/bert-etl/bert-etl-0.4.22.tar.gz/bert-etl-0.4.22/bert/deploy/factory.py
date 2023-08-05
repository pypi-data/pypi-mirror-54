#!/usr/env/bin python

import argparse
import enum
import functools
import importlib
import inspect
import logging
import multiprocessing
import os
import signal
import time
import typing
import types

from datetime import datetime

from bert import utils as bert_utils
from bert.deploy import utils as bert_deploy_utils

logger = logging.getLogger(__name__)

STOP_DAEMON: bool = False
class Service(enum.Enum):
    AWSLambda: str = 'aws-lambda'

def capture_options() -> typing.Any:
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--service', default=Service.AWSLambda, type=Service)
    parser.add_argument('-u', '--undeploy', action="store_true", default=False)
    parser.add_argument('-i', '--invoke', action="store_true", default=False)
    parser.add_argument('-m', '--module-name', default='bert')
    parser.add_argument('-f', '--flush', default=False, action="store_true")
    parser.add_argument('-d', '--dry-run', default=False, action="store_true", help="Create the lambda functions and output ./lambdas without deploying to AWS")
    return parser.parse_args()

def deploy_service(options) -> None:
    jobs: typing.Dict[str, typing.Any] = bert_utils.scan_jobs(options)
    jobs: typing.Dict[str, typing.Any] = bert_utils.map_jobs(jobs)

    if options.service == Service.AWSLambda:
        if options.invoke:
            import boto3
            job_name: str = [job for job in jobs.keys()][0]
            client = boto3.client('lambda')
            logger.info(f'Invoking Job[{job_name}]')
            client.invoke(
                FunctionName=job_name,
                InvocationType='Event')
            import sys; sys.exit(0)

        bert_deploy_utils.build_project(jobs)
        bert_deploy_utils.build_lambda_handlers(jobs)
        bert_deploy_utils.build_archives(jobs)
        bert_deploy_utils.create_roles(jobs)
        bert_deploy_utils.scan_dynamodb_tables(jobs)
        bert_deploy_utils.destroy_lambda_to_table_bindings(jobs)
        bert_deploy_utils.destroy_lambdas(jobs)
        bert_deploy_utils.create_lambdas(jobs)
        bert_deploy_utils.create_dynamodb_tables(jobs)
        bert_deploy_utils.create_reporting_dynamodb_table()
        bert_deploy_utils.bind_lambdas_to_tables(jobs)
        bert_deploy_utils.bind_lambdas_to_events(jobs)

    else:
        raise NotImplementedError(options.service)

def run_from_cli():
    import sys, os
    sys.path.append(os.getcwd())
    options = capture_options()
    deploy_service(options)

if __name__ in ['__main__']:
    run_from_cli()

