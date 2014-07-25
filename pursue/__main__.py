# -*- coding: utf-8 -*-

"""Pursue - OpenStack Object Storage client

Usage:
    pursue [options] list [<container>]
    pursue [options] upload <container> <path>

Options:
    -h --help   Shows these lines.
    --account-name <account_name>
    --auth-token <auth_token>
"""

import sys

from finch import Session
from tornado import httpclient, ioloop
from docopt import docopt

from . import Containers, Objects, Object, OpenStackAuth


def _parse_args():
    return docopt(__doc__)


if __name__ == '__main__':
    args = _parse_args()

    session = Session(httpclient.AsyncHTTPClient(), auth=OpenStackAuth(token=args['--auth-token']))

    def on_results(results, error):
        ioloop.IOLoop.instance().stop()

        if error:
            raise error

        for result in results:
            print result


    def on_uploaded(result, error):
        ioloop.IOLoop.instance().stop()

        if error:
            raise error

        print result

    account_name = args['--account-name']
    container = args['<container>']

    if args['list']:
        if container is None:
            containers = Containers(account_name, session)
            containers.all(on_results)
        else:
            objects = Objects(account_name, container, session)
            objects.all(on_results)

    elif args['upload']:
        objects = Objects(account_name, container, session)
        objects.add(Object.from_path(args['<path>']), on_uploaded)

    ioloop.IOLoop.instance().start()
