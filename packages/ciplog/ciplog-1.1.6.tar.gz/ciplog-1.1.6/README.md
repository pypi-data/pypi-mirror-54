# CipLog

CipLog is an easy Python package that used for you write your logs.

CipLog has three types of log, **info**, **warning** and **error**

CipLog supports python 3+.

# Examples

## Install

> Under your virtualenv do:  

```
$ pip install ciplog
```

## Getting Started

You can set a service name and a log path or use default.
````python
from ciplog.v2 import NewCipLog

log = NewCipLog(service_name='news-api', log_path='/your/log/path')

````

### Info
```python
from ciplog.v2 import NewCipLog

log = NewCipLog(service_name='news-api', log_path='/your/log/path')

log.info(class_name='class_name', method='news', message='news that successfully registered.')
```

### Warning
```python
from ciplog.v2 import NewCipLog

log = NewCipLog(service_name='news-api', log_path='/your/log/path')

log.warning(code='AB456*', class_name='class_name', method='news', message='The unicode is not defined.')

```

### Error
```python
from ciplog.v2 import NewCipLog

log = NewCipLog(service_name='news-api', log_path='/your/log/path')

log.error(code='UX3023', class_name='class_name', method='news', data='obj of the function', message='The unicode is not defined.')

```

## Upload Package
```bash
$ python3 setup.py sdist upload
```


## Release History
* 1.1.6:
    * ADD: Adding 'http_status' as optional parameter 
* 1.1.5:
    * ADD: New format to logs
* 1.1.0:
    * ADD: New format to logs
* 1.0.8:
    * ADD: Service version to the logs
* 1.0.7:
    * REMOVE: Status code verification. 
* 1.0.6:
    * ADD: status code 500.
    * CHANGE: command line for upload package.
* 1.0.5:
    * CHANGE: write with json in file.
    * ADD: status code 400.
* 1.0.4:
    * CHANGE: add error dict.
    * CHANGE: add release history and upload package in README.
* 1.0.3
    * FIX: typing correct service name.
* 1.0.2
    * ADD: add validate_status_http().
    * ADD: add create_folder().
* 1.0.1
    * CHANGE: log format.
* 1.0.0
  * start of the projects with basic configurations.
