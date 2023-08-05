 # SMART PYTHON UTILS

This repository has a library of tools to facilitate development in all smart-development, the first functionality added to was the logger.

- Logger will be different depending on the environment, configuration is a yml, this yaml is in AWS. The service used by AWS is SSM.

## Package contents
| Directory/File | Description |
| --- | --- |
| `aws.py` | Features to use the aws services. |
| `logger.py` | Features to Logger. |
| `tests/` | Contains repo tests. |
| `requirements.txt` | Contains requirments. |
| `README.md` | This guide. |

## Prerequisites
* AWS permissions.
* Use of environment variables.
* yaml in AWS with configuration by APP_NAME.

### Enviroment Variables

 If they do not have a Logger-generic(only console) will be returned.

 - AWS_ACCESS_KEY_ID
 - AWS_SECRET_ACCESS_KEY
 - APP_NAME
 - sc_environment

## Configuration before launch

If you only have permissions on AWS, you will return default configuration.

example of default configuration in SSM with Name default.

```
version: 1
formatters:
 simple:
  format: '%(asctime)s - %(module)s - %(funcName)s - [%(levelname)s] - %(message)s'
handlers:
 console:
  class: logging.StreamHandler
  level: DEBUG
  formatter: simple
  stream: ext://sys.stdout
loggers:
 main:
  level: DEBUG
  handlers: [console]
  propagate: false
root:
 level: INFO
 handlers: [console]

```
If you want to add Sentry. The dsn with the name SENTRY_DSN_app_name must be added in AWS and in configuration-yaml.