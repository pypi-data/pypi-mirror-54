# newsworthy-py: aws_utils

A Python package with utility functions for working with AWS services.



## Install package

`pip install nw_aws_utils`

## Usage

```python3
from aws_utils import env_or_ssm

# Get a parameter from either environment or from AWS SSM
env_or_ssm(env_key="SHARED_SECRET", ssm_key="SHARED_SECRET")
```

## Develop

Run tests:

`make tests` (run all tests)

## Deploy

To Github:

`./new_version.py v=1.0.2 msg="Made some changes"`

The current version is defined in `CURRENT_VERSION.txt`. This file is updated with this make command.

To PyPi:

`./upload_to_pypi.py`

To Github:

`git push origin master`
