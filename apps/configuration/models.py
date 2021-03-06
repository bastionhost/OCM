# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from jsonfield import JSONField
import shortuuid


class Schema(models.Model):
    data = JSONField(default={})

    def _get_name(self, data):
        name = ''
        if data['type'] == 'object':
            name += '-'.join(data['properties'].keys())
        elif data['type'] == 'array':
            name += '[{}]'.format(data['items']['type'])
            name += self._get_name(data['items'])
        return '-' + name if name else ''

    def __unicode__(self):
        base_name = '[{}]'.format(self.data['type'])
        return base_name + self._get_name(self.data)


class Configuration(models.Model):
    name = models.CharField(max_length=100, unique=True, default=shortuuid.uuid)
    schema = models.ForeignKey(Schema)
    data = JSONField(null=True, blank=True)
