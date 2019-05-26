# This file is part of EMX client python library

# EMX client library is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import time
import json
import hashlib
import hmac
import base64

from functools import wraps


class EmxApiException(Exception):
    pass


def body_to_string(body):
    return json.dumps(body, separators=(',', ':'))


def generate_signature(api_secret, timestamp, http_method, request_path, body):
    if body:
        body = body_to_string(body)
    else:
        body = ''

    message = str(timestamp) + http_method + request_path + body
    try:
        secret = base64.b64decode(api_secret)
    except base64.binascii.Error as err:
        raise EmxApiException("b64decode failed: {}".format(err))

    signature = hmac.new(secret, message.encode(),
                         digestmod=hashlib.sha256).digest()
    return base64.encodestring(signature)


def get_timestamp():
    return int(round(time.time()))


class order_request:
    def __init__(self):
        self.instrument_name = ""
        self.quantity = 0.0
        self.price = 0.0
        self.side = ""  # buy or sell
        self.type = ""  # limit or market
        self.orderid = ""  # optional client id


def handle_result(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if result.status_code < 200 or result.status_code > 300:
            raise EmxApiException("Request failed. Reason: {}".format(result.text))
        return result.text
    return wrapper


def get_sub_params(api_key, api_secret, symbol, channels):
    endpoint = "/v1/user/verify"
    timestamp = get_timestamp()
    signature = generate_signature(api_secret, timestamp,
                                   "GET", endpoint, None)
    msg = {
            "type": "subscribe",
            "contract_codes": [symbol],
            "channels": channels,
            "key": api_key,
            "sig": signature.decode().strip(),
            "timestamp": timestamp
         }
    return msg
