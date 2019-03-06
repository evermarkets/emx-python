# API Client for [EMX API](https://docs.emx.com/)

## Description

[EMX API client](https://www.emx.com/) is available in this package.

### Installation

```
pip install emx

```

### Example

```
See examples.py file

or

from emx.rest_api import RestApi
emx_client = RestApi("your_api_key", "your_b64_secret")
result = emx_client.get_account()
print(result)
