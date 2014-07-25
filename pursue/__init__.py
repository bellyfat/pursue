# -*- coding: utf-8 -*-

import json

from finch import Collection
from booby import Model, fields


class Object(Model):
    name = fields.String()
    hash = fields.String()
    last_modified = fields.String()
    bytes = fields.Integer()
    content_type = fields.String()


class Objects(Collection):
    model = Object

    def __init__(self, account, container, *args, **kwargs):
        self.account = account
        self.container = container

        super(Objects, self).__init__(*args, **kwargs)

    @property
    def url(self):
        return 'https://storage101.iad3.clouddrive.com/v1/{account}/{container}?format=json'.format(
            account=self.account, container=self.container)


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
