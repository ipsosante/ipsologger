# ipsologger

## Introduction

ipsologger aimed to facilated json logging for gunicorn and django.

it contains: 
 
  * a custom formatter based from pythonjsonlogger to add custom fields used by us.
  
  * a declaration of dictconfig use for gunicorn
  
  * an override of gunicorn logger (based on jslog4kube)

ipsologger produce for gunicorn log messages like that:

 ```
 {"@timestamp": "2018-12-07T09:14:07.333021+00:00", "@hostname": "jessie", "@tag": "gunicorn_access", "asctime": "2018-12-07T09:14:07,007", "message": "(access record)", "name": "gunicorn.access", "created": 1544174047.3323653, "filename": "glogging.py", "module": "glogging", "funcName": "access", "lineno": 353, "msecs": 332.3652744293213, "pathname": "/var/www/vagrant.ipsosante.fr/lib/python3.4/site-packages/gunicorn/glogging.py", "process": 15744, "processName": "MainProcess", "relativeCreated": 25997.59030342102, "thread": 140258425861888, "threadName": "MainThread", "levelname": "INFO", "access": {"request-time": "0.510723", "protocol": "HTTP/1.0", "remote": "10.0.2.2", "response-length": "2543", "referrer": "http://localhost.ipso.fr:18080/fr/", "query": "next=/fr/?edit", "status": "200", "method": "GET", "url-path": "/fr/admin/login/", "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36", "username": "-"}}
{"@timestamp": "2018-12-07T09:14:29.941342+00:00", "@hostname": "jessie", "@tag": "gunicorn_access", "asctime": "2018-12-07T09:14:29,007", "message": "(access record)", "name": "gunicorn.access", "created": 1544174069.9409451, "filename": "glogging.py", "module": "glogging", "funcName": "access", "lineno": 353, "msecs": 940.9451484680176, "pathname": "/var/www/vagrant.ipsosante.fr/lib/python3.4/site-packages/gunicorn/glogging.py", "process": 15744, "processName": "MainProcess", "relativeCreated": 48606.17017745972, "thread": 140258425861888, "threadName": "MainThread", "levelname": "INFO", "access": {"request-time": "0.100269", "protocol": "HTTP/1.0", "remote": "10.0.2.2", "response-length": "88", "referrer": "-", "query": "next=/fr/?edit", "status": "404", "method": "GET", "url-path": "/fr/admin/logn/", "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36", "username": "-"}}
```

## Install

In order to work you must install via pip tool those requirements:

```shell
$ pip install python-json-logger==0.1.0
$ pip install git+http://github.com/halkeye/jslog4kube@patch-1#egg=jslog4kube==1.0.4-patch1
```

## Gunicorn

1. Create a gunicorn.conf

```
access_log_format = 'remote!%({X-Forwarded-For}i)s|method!%(m)s|url-path!%(U)s|query!%(q)s|username!%(u)s|protocol!%(H)s|status!%(s)s|response-length!%(b)s|referrer!%(f)s|\
user-agent!%(a)s|request-time!%(L)s'
accesslog = '-'
logger_class = 'ipsologger.gunicorn.GunicornLogger'
```

access_log_format is used by GunicornLogger to produce json for access file.

2. Start gunicorn with this new configuration

```shell
$ bin/gunicorn --config=<path to gunicorn.conf>
```
