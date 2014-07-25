# -*- coding: utf-8 -*-

"""Pursue - OpenStack Object Storage client

Usage:
    pursue [options] list [<container>]
    pursue [options] upload <container> <path>
    pursue [options] download <container> <object>

Options:
    -h --help   Shows these lines.
    --account-name <account_name>
    --auth-token <auth_token>
"""

import sys
from functools import partial

from finch import Session
from tornado import httpclient, ioloop
from docopt import docopt

from . import Containers, Objects, Object, OpenStackAuth


def main():
    args = _parse_args()

    session = Session(httpclient.AsyncHTTPClient(), auth=OpenStackAuth(token=args['--auth-token']))

    account_name = args['--account-name']
    container = args['<container>']

    if args['list']:
        if container is None:
            containers = Containers(account_name, session)
            containers.all(_on_results)
        else:
            objects = Objects(account_name, container, session)
            objects.all(_on_results)

    elif args['upload']:
        objects = Objects(account_name, container, session)
        objects.add(Object.from_path(args['<path>']), _on_uploaded)

    elif args['download']:
        obj = args['<object>']

        objects = Objects(account_name, container, session)
        objects.get(obj, partial(_on_downloaded, obj))

    ioloop.IOLoop.instance().start()


def _on_results(results, error):
    ioloop.IOLoop.instance().stop()

    if error:
        raise error

    for result in results:
        print result.name


def _on_uploaded(result, error):
    ioloop.IOLoop.instance().stop()

    if error:
        raise error


def _on_downloaded(name, result, error):
    ioloop.IOLoop.instance().stop()

    if error:
        raise error

    result.to_path(name)


def _parse_args():
    return docopt(__doc__)
