# -*- coding: utf-8 -*-

import json
import mimetypes
from os.path import basename
from functools import partial

from finch import Collection
from booby import Model, fields


class Object(Model):
    name = fields.String()
    hash = fields.String()
    last_modified = fields.String()
    bytes = fields.Integer()
    content_type = fields.String()
    blob = fields.Field()

    @classmethod
    def from_path(cls, path):
        with open(path, 'rb') as obj:
            blob = obj.read()

        return cls(
            name=basename(path).replace(' ', '_'),
            content_type=mimetypes.guess_type(path)[0],
            blob=blob
        )

    def to_path(self, path):
        with open(path, 'wb') as output:
            output.write(self.blob)

    def decode(self, response):
        if response.request.method == 'GET':
            return {'blob': response.body}
        return {}

    @property
    def url(self):
        return 'https://storage101.iad3.clouddrive.com/v1/{account}/{container}/{name}'


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

    def request_add(self, obj, callback):
        self.client.fetch(
            obj.url.format(account=self.account, container=self.container, name=obj.name),
            method='PUT',
            headers={'Content-Type': obj.content_type or ''},
            body=obj.blob,
            callback=partial(self.on_add, callback, obj))

    def request_delete(self, obj, callback):
        self.client.fetch(
            obj.url.format(account=self.account, container=self.container, name=obj.name),
            method='DELETE',
            callback=partial(self.on_delete, callback))


class Container(Model):
    name = fields.String()

    @property
    def url(self):
        return 'https://storage101.iad3.clouddrive.com/v1/{account}/{container}'


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

    def request_delete(self, obj, callback):
        self.client.fetch(
            obj.url.format(account=self.account, container=obj.name),
            method='DELETE',
            callback=partial(self.on_delete, callback))


class OpenStackAuth(object):
    def __init__(self, token):
        self._token = token

    def __call__(self, request):
        request.headers['x-auth-token'] = self._token
