# -*- coding: utf-8 -*-

import json
import argparse

from finch import Collection, Session
from booby import Model, fields
from tornado import httpclient, ioloop


class Container(Model):
    name = fields.String()


class Containers(Collection):
    model = Container

    def __init__(self, account, *args, **kwargs):
        self.account = account

        super(Containers, self).__init__(*args, **kwargs)

    @property
    def url(self):
        return 'https://storage101.iad3.clouddrive.com/v1/{account}?format=json'.format(account=self.account)

    def decode(self, response):
        return [{'name': container['name']} for container in json.loads(response.body)]


class OpenStackAuth(object):
    def __init__(self, token):
        self._token = token

    def __call__(self, request):
        request.headers['x-auth-token'] = self._token


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--account-name', required=True)
    parser.add_argument('--auth-token', required=True)

    return parser.parse_args()


if __name__ == '__main__':
    args = _parse_args()

    containers = Containers(args.account_name, Session(httpclient.AsyncHTTPClient(), auth=OpenStackAuth(token=args.auth_token)))

    def on_containers(containers, error):
        ioloop.IOLoop.instance().stop()

        if error:
            raise error

        for container in containers:
            print container

    containers.all(on_containers)

    ioloop.IOLoop.instance().start()
