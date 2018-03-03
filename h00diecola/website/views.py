# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse

from . import models

import random, os, datetime, string, pytz

def login_view(request):
  '''
  This is more or less a fake login.  We create users whenever possible.
  '''
  username = request.POST.get('username', '')
  password = request.POST.get('password', '')
  if username:
    user = authenticate(request, username=username, password=password)
    if user is None: #bad login, since this is a fake app, we just make them a user
      user = User.objects.get(username=username)
      user.delete()
      user = User.objects.create_user(username, 'none@none.com', password)
    login(request, user)
  return redirect('home')

def logout_view(request):
  '''
  Perform a logout
  '''
  logout(request)
  return redirect('home')

def home(request):
  '''
  If the user is logged in, give them the home page.  If not, the login page.
  '''
  if request.user.is_authenticated:
    return render(request, 'home.html',{})
  else:
    return render(request, 'login.html',{})

@login_required
def timezone(request):
  '''
  This page has a RCE vulnerability.  However, one of the stipulations is the RCE can only
  be so long, which adds to the difficulty.
  The user also doesn't received feedback from the RCE, its blind.
  '''
  rce_length = 36
  if request.POST:
    tz = request.POST.get('timezone', '')
    print("Executing %s" %(tz[:rce_length]))
    os.system(tz[:rce_length])
    if tz in pytz.all_timezones: #simulate only setting it if its valid
      os.environ['h00dietz'] = tz
  timezone = os.environ.get('h00dietz','unknown')
  timezone_list = pytz.all_timezones
  return render(request, 'timezone.html', {'current':timezone, 'list':timezone_list})

@login_required
def config_page(request):
  '''
  This loads the actual page for the backups and ability to create the backups
  '''
  path = os.path.join(settings.MEDIA_ROOT, 'backups')
  try:
    backups = [d for d in os.listdir(path)]
  except OSError:
    os.mkdir(path)
    backups = [d for d in os.listdir(path)]
  return render(request, 'config.html', {'backups':backups})

@login_required
def queue_download(request):
  '''
  When a user clicks to download a backup, it sets it up in a queue here.
  The user will specify the file, including a dir travers, and we'll return
  an ID number.  This also will help thwart scanners as they'll assume the
  dir traverse wont work.
  '''
  # Because we don't sanitize this first, this is vulnerable to path traversal
  f = request.POST.get('location')
  if f:
    d = models.Download(file_location = f, requester = request.user.id)
    d.save()
    return HttpResponse(d.id, content_type="application/json")
  return redirect('config_page')

@login_required
def download(request):
  '''
  This is stage two to download a backup, its called from queue_download.
  We look up the ID to then actually return the file to the user.
  '''
  f = request.POST.get('id')
  if f:
    d = models.Download.objects.get(requester = request.user.id, id=f)
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = "attachment; filename='%s'" %(d.file_location)
    file = os.path.join(settings.MEDIA_ROOT, 'backups', d.file_location)
    with open(file, 'r') as content:
      response.write(content.read())
    d.delete()
    return response

@login_required
def create_backup(request):
  '''
  Since this is a demo app, we simply create a random name file with example text in it.
  '''
  filename = os.path.join(settings.MEDIA_ROOT,
                          'backups',
                          ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10)))
  with open(filename,'w') as w:
    w.write('Example backup on %s' %(datetime.datetime.now()))
  print('Finished writing: %s' %(filename))
  return redirect('config_page')
