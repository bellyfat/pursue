# -*- coding: utf-8 -*-

import sys
import argparse

from finch import Session
from tornado import httpclient, ioloop

from . import Containers, Objects, Object, OpenStackAuth


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('command')
    parser.add_argument('container', nargs='?')
    parser.add_argument('path', nargs='?')
    parser.add_argument('--account-name', required=True)
    parser.add_argument('--auth-token', required=True)

    return parser.parse_args()


if __name__ == '__main__':
    args = _parse_args()

    session = Session(httpclient.AsyncHTTPClient(), auth=OpenStackAuth(token=args.auth_token))

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

    if args.command == 'list':
        if args.container is None:
            containers = Containers(args.account_name, session)
            containers.all(on_results)
        else:
            objects = Objects(args.account_name, args.container, session)
            objects.all(on_results)
    elif args.command == 'upload':
        if args.container is None or args.path is None:
            print 'You should specify a container name and file path'
            sys.exit(1)

        objects = Objects(args.account_name, args.container, session)
        objects.add(Object.from_path(args.path), on_uploaded)

    ioloop.IOLoop.instance().start()
