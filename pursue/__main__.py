# -*- coding: utf-8 -*-

import argparse

from finch import Session
from tornado import httpclient, ioloop

from . import Containers, Files, OpenStackAuth


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('command')
    parser.add_argument('name', nargs='?')
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

    if args.command == 'list':
        if args.name is None:
            containers = Containers(args.account_name, session)
            containers.all(on_results)
        else:
            files = Files(args.account_name, args.name, session)
            files.all(on_results)

    ioloop.IOLoop.instance().start()
