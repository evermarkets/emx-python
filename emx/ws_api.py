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

import json
from websocket import create_connection, WebSocketTimeoutException
from emx.utils import EmxApiException, generate_signature, get_timestamp


class WebSocketApi():
    """ Maintains a single session between EMX and your box.
    Api key-secret key pair is optional, but private
    queries will not be possible for authenticated requests (please see EMX API doc)

    .. note::
       No query rate limiting is performed.
    """

    def __init__(self, api_key='', key_secret='', timeout=3, uri="wss://api.testnet.emx.com"):
        self.ws = create_connection(uri)
        self.ws.settimeout(timeout)

        self._api_key = api_key
        self._api_secret = key_secret

    def receive_msg(self):
        try:
            msg = self.ws.recv()
        except WebSocketTimeoutException:
            raise EmxApiException("No messages received")
        except Exception as err:
            raise EmxApiException("Unable to receive msgs. Reason: {}".format(err))
        return msg

    def subscribe(self, symbols, channels):
        """Subscribe to selected channels. EMX response looks like
        {
            "type":"subscriptions",
            "channels":[
                        {
                            "name":"",
                            "contract_codes":[]
                        },
                        {
                            "name":"",
                            "contract_codes":[]
                        }
                       ]
        }

        :param symbols: instrument symbols list
        :param channels: subscription channels list
        :returns: None
        """

        endpoint = "/v1/user/verify"
        timestamp = get_timestamp()
        signature = generate_signature(self._api_secret, timestamp, "GET", endpoint, None)
        msg = {
                "type": "subscribe",
                "contract_codes": symbols,
                "channels": channels,
                "key": self._api_key,
                "sig": signature.decode().strip(),
                "timestamp": timestamp
             }
        try:
            self.ws.send(json.dumps(msg))
        except Exception as err:
            raise EmxApiException("Unable to send request. Reason: {}".format(err))

    def unsubscribe(self, channels):
        """Unsubscribe from selected channels for all contacts. EMX response looks like {"type":"subscriptions","channels":[]}

        :param channels: channels list to unsubscribe from
        :returns: None
        """

        msg = {
            "type": "unsubscribe",
            "contract_codes": [],
            "channels": ["orders"]
        }
        try:
            self.ws.send(json.dumps(msg))
        except Exception as err:
            raise EmxApiException("Unable to send request. Reason: {}".format(err))

    def close(self):
        self.ws.close()
