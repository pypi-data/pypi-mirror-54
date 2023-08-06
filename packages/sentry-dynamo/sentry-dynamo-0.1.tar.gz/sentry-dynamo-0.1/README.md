# sentry-dynamo
A Sentry Dynamo NodeStorage library

## Installation
`pip install git+ssh://git@github.com/Flipboard/sentry-dynamo.git`

## Configuration

In `sentry.conf.py` set the following:
```python
SENTRY_NODESTORE = 'sentry_dynamo.dynamo.nodestore.backend.DynamoNodeStorage'

SENTRY_NODESTORE_OPTIONS = {
	'region_name': {the aws region where the dynamo table lives},
	'aws_access_key_id': {aws access key id},
	'aws_secret_access_key': {aws secret access key},
	'table_name': {the dynamo table name},
	'primary_key_name': {the primary key of the dynamo table}
}

```

## Development

### Environment Setup

1. Create and enter a virtualenv using your favorite method:
  1. Create a virtualenv for sentry-dynamo: `mkvirtualenv sentry-dynamo`
  2. Enter the virtualenv: `workon sentry-dynamo`
2. Install the project from the directory this project is cloned: `pip install ./sentry-dynamo`

### Tests
The tests require a live Dynamo table to run on. 

1. Before running the tests ensure that the following environment variables are set: 

  ```bash
export REGION_NAME={the aws region where your dev dynamo table lives}
export AWS_ACCESS_KEY_ID={your aws access key id}
export AWS_SECRET_ACCESS_KEY={your aws secret access key}
export TABLE_NAME={your dev dynamo table name}
export PRIMARY_KEY_NAME={the primary key of your dev dynamo table}
```
1. Run the tests: `./src/sentry_dynamo/test/DynamoNodeStorageTest.py`
