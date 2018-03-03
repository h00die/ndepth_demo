# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import os

#here we fake setting a real timezone
os.environ['h00dietz'] = 'Europe/Moscow'

class Download(models.Model):
  file_location = models.TextField('File to download')
  requester = models.IntegerField('userID of the account requesting to prevent cross account leakage')

