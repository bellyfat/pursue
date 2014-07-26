# -*- coding: utf-8 -*-

"""Pursue - OpenStack Object Storage client

Usage:
    pursue [options] list [<container>]
    pursue [options] upload <container> <path>
    pursue [options] download <container> <object>
    pursue [options] delete <container> [<object>]
    pursue [options] keygen <path>

Options:
    -h --help   Shows these lines.
    --account-name <account_name>
    --auth-token <auth_token>
    --secret <path>
"""

from functools import partial

from cryptography.fernet import Fernet as encrypt_service
from finch import Session
from tornado import httpclient, ioloop
from docopt import docopt

from . import Containers, Container, Objects, Object, OpenStackAuth

DEFAULT_TIMEOUT = 60*3


def main():
    args = _parse_args()

    session = Session(
        httpclient.AsyncHTTPClient(
            defaults={'request_timeout': DEFAULT_TIMEOUT}),
        auth=OpenStackAuth(token=args['--auth-token']))

    account_name = args['--account-name']
    container = args['<container>']

    secret_key = None
    if args['--secret']:
        with open(args['--secret']) as secret_file:
            secret_key = secret_file.read()

    if args['list']:
        if container is None:
            containers = Containers(account_name, session)
            containers.all(_on_results)
        else:
            objects = Objects(account_name, container, session)
            objects.all(_on_results)

        ioloop.IOLoop.instance().start()

    elif args['upload']:
        objects = Objects(account_name, container, session)
        obj = Object.from_path(args['<path>'])

        if secret_key is not None:
            obj.blob = encrypt_service(secret_key).encrypt(obj.blob)

        objects.add(obj, _on_uploaded)
        ioloop.IOLoop.instance().start()

    elif args['download']:
        obj = args['<object>']
        objects = Objects(account_name, container, session)
        objects.get(obj, partial(_on_downloaded, obj, secret_key))
        ioloop.IOLoop.instance().start()

    elif args['delete']:
        obj = args['<object>']

        if obj is None:
            containers = Containers(account_name, session)
            containers.delete(Container(name=container), _on_deleted)
        else:
            objects = Objects(account_name, container, session)
            objects.delete(Object(name=obj), _on_deleted)

        ioloop.IOLoop.instance().start()

    elif args['keygen']:
        with open(args['<path>'], 'w') as output:
            output.write(encrypt_service.generate_key())


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

def _on_deleted(error):
    ioloop.IOLoop.instance().stop()

    if error:
        raise error


def _on_downloaded(name, secret_key, result, error):
    ioloop.IOLoop.instance().stop()

    if error:
        raise error

    if secret_key is not None:
        result.blob = encrypt_service(secret_key).decrypt(result.blob)

    result.to_path(name)


def _parse_args():
    return docopt(__doc__)
