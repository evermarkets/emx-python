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

import requests
from emx.utils import EmxApiException, handle_result, generate_signature, get_timestamp


class RestApi():
    """ Maintains a single session between EMX and your box.
    Api key-secret key pair is optional, but private
    queries will not be possible for authenticated requests (please see EMX API doc)

    .. note::
       No query rate limiting is performed.
    """

    def __init__(self, api_key='', key_secret='', uri='http://api.testnet.emx.com'):
        """ Create an object with authentication information.

        :param api_key: (optional) key identifier for queries to the API
        :type api_key: str
        :param key_secret: (optional) actual private key used to sign messages
        :type key_secret: str
        :returns: None
        """

        self.session = requests.Session()

        self.uri = uri
        self._api_key = api_key
        self._api_secret = key_secret

        self._headers = {
                         'content-type': 'application/json'
                        }

    def close(self):
        """ Close an existing connection

        :returns: None
        """
        self.session.close()

    @handle_result
    def get_account(self):
        """
        Get a list of all trader accounts for the current user.

        :returns: {"accounts": [ {"trader_id": "string", "alias": "string"}]}
        :raises: Exception if requests.Response is not successful
        """

        endpoint = "/v1/accounts"
        url = self.uri + endpoint

        timestamp = get_timestamp()
        signature = generate_signature(self._api_secret, timestamp, "GET", endpoint, "")

        self._headers['EMX-ACCESS-KEY'] = self._api_key
        self._headers['EMX-ACCESS-SIG'] = signature.decode().strip()
        self._headers['EMX-ACCESS-TIMESTAMP'] = str(timestamp)

        result = self.session.get(url=url, params="", headers=self._headers)
        if result.status_code != 200:
            raise EmxApiException("Request failed. Reason: {}".format(result.text))
        return result

    # param start_time required but according to docs it is optional
    @handle_result
    def get_account_rank(self, start_time):
        """Get a ranking of trading accounts by % change in net liquidation value since a given date.

        :returns: {"ranking": [{"alias": "string","percent_change_net_liquidation_value": "string"}]}
        :raises: Exception if requests.Response is not successful
        """

        endpoint = "/v1/accounts/rank"
        url = self.uri + endpoint
        body = {"start_time": start_time}
        result = self.session.get(url=url, params=body)
        if result.status_code != 200:
            raise EmxApiException("Request failed. Reason: {}".format(result.text))
        return result

    @handle_result
    def get_balances(self, trader_id):
        """Get trading account info including balances, margin requirements, and net liquidation value.

        :returns: {
                    "balance": "string",
                    "initial_margin_required": "string",
                    "maintenance_margin_required": "string",
                    "unrealized_profit": "string",
                    "net_liquidation_value": "string",
                    "available_funds": "string",
                    "excess_liquidity": "string",
                    "holds": "string"
                  }
        :raises: Exception if requests.Response is not successful
        """

        endpoint = "/v1/accounts/{}".format(trader_id)
        url = self.uri + endpoint

        body = {
            "trader_id": trader_id,
        }
        timestamp = get_timestamp()
        signature = generate_signature(self._api_secret, timestamp, "GET", endpoint, body)

        self._headers['EMX-ACCESS-KEY'] = self._api_key
        self._headers['EMX-ACCESS-SIG'] = signature.decode().strip()
        self._headers['EMX-ACCESS-TIMESTAMP'] = str(timestamp)
        result = self.session.get(url=url, json=body, headers=self._headers)
        if result.status_code != 200:
            raise EmxApiException("Request failed. Reason: {}".format(result.text))
        return result

    # Why should be authorized with Bearer Token
    @handle_result
    def get_account_alias(self, trader_id):
        """Get trading account alias for a given account.

        :param trader_id: trader id
        :returns: {"key":"string", "secret":"string"}
        :raises: Exception if requests.Response is not successful
        """

        endpoint = "/v1/accounts/{}/alias".format(trader_id)
        url = self.uri + endpoint

        body = {
            "trader_id": trader_id,
        }
        timestamp = get_timestamp()
        signature = generate_signature(self._api_secret, timestamp, "GET", endpoint, body)

        self._headers['EMX-ACCESS-KEY'] = self._api_key
        self._headers['EMX-ACCESS-SIG'] = signature.decode().strip()
        self._headers['EMX-ACCESS-TIMESTAMP'] = str(timestamp)
        result = self.session.get(url=url, json=body, headers=self._headers)
        if result.status_code != 200:
            raise EmxApiException("Request failed. Reason: {}".format(result.text))
        return result

    @handle_result
    def update_account_alias(self, trader_id):
        """Get your account info including balances, margin requirements, and net liquidation value.

        :returns:
        :raises: Exception if requests.Response is not successful
        """

        endpoint = "/v1/accounts/{}/alias".format(trader_id)
        url = self.uri + endpoint

        body = {
            "trader_id": trader_id,
        }
        timestamp = get_timestamp()
        signature = generate_signature(self._api_secret, timestamp, "GET", endpoint, body)

        self._headers['EMX-ACCESS-KEY'] = self._api_key
        self._headers['EMX-ACCESS-SIG'] = signature.decode().strip()
        self._headers['EMX-ACCESS-TIMESTAMP'] = str(timestamp)
        result = self.session.put(url=url, json=body, headers=self._headers)
        if result.status_code != 200:
            raise EmxApiException("Request failed. Reason: {}".format(result.text))
        return result

    @handle_result
    def list_fills(self, contract_code="", order_id="", before="", after=""):
        """Returns all fills for the current trading account - in descending chronological order.

        :returns:
        :raises: Exception if requests.Response is not successful
        """

        endpoint = "/v1/fills"
        url = self.uri + endpoint

        body = {
            "contract_code": contract_code,
            "order_id": order_id,
            "before": before,
            "after": after
        }
        timestamp = get_timestamp()
        signature = generate_signature(self._api_secret, timestamp, "GET", endpoint, body)

        self._headers['EMX-ACCESS-KEY'] = self._api_key
        self._headers['EMX-ACCESS-SIG'] = signature.decode().strip()
        self._headers['EMX-ACCESS-TIMESTAMP'] = str(timestamp)
        result = self.session.get(url=url, json=body, headers=self._headers)
        if result.status_code != 200:
            raise EmxApiException("Request failed. Reason: {}".format(result.text))
        return result

    @handle_result
    def list_keys(self):
        """Get a list of all API keys (but not secrets). Secrets are only returned at the time of key creation.

        :returns: {"key":"string", "secret":"string"}
        :raises: Exception if requests.Response is not successful
        """

        endpoint = "/v1/keys"
        url = self.uri + endpoint

        timestamp = get_timestamp()
        signature = generate_signature(self._api_secret, timestamp, "GET", endpoint, "")

        self._headers['EMX-ACCESS-KEY'] = self._api_key
        self._headers['EMX-ACCESS-SIG'] = signature.decode().strip()
        self._headers['EMX-ACCESS-TIMESTAMP'] = str(timestamp)
        result = self.session.get(url=url, params="", headers=self._headers)
        if result.status_code != 200:
            raise EmxApiException("Request failed. Reason: {}".format(result.text))
        return result

    @handle_result
    def create_key(self):
        """Mint a new API key

        :returns: {"key":"string", "secret":"string"}
        :raises: Exception if requests.Response is not successful
        """

        endpoint = "/v1/keys"
        url = self.uri + endpoint

        timestamp = get_timestamp()
        signature = generate_signature(self._api_secret, timestamp, "POST", endpoint, "")

        self._headers['EMX-ACCESS-KEY'] = self._api_key
        self._headers['EMX-ACCESS-SIG'] = signature.decode().strip()
        self._headers['EMX-ACCESS-TIMESTAMP'] = str(timestamp)
        result = self.session.post(url=url, params="", headers=self._headers)
        if result.status_code != 200:
            raise EmxApiException("Request failed. Reason: {}".format(result.text))
        return result

    @handle_result
    def delete_key(self, key):
        """Revoke an existing API key.

        :param key: an api key to delete
        :returns: {"key":"string","message":"Key revoked."}
        :raises: Exception if requests.Response is not successful
        """

        endpoint = "/v1/keys/{}".format(key)
        url = self.uri + endpoint

        timestamp = get_timestamp()
        signature = generate_signature(self._api_secret, timestamp, "DELETE", endpoint, "")

        self._headers['EMX-ACCESS-KEY'] = self._api_key
        self._headers['EMX-ACCESS-SIG'] = signature.decode().strip()
        self._headers['EMX-ACCESS-TIMESTAMP'] = str(timestamp)
        result = self.session.delete(url=url, params="", headers=self._headers)
        if result.status_code != 200:
            raise EmxApiException("Request failed. Reason: {}".format(result.text))
        return result

    @handle_result
    def list_orders(self, contract_code="", status="", before="", after=""):
        """Returns orders for the current trading account - in descending chronological order.

        :returns: {
                      "orders": [
                                    {
                                        "order_id": "string",
                                        "client_id": "string",
                                        "contract_code": "string",
                                        "type": "market",
                                        "side": "buy",
                                        "size": "string",
                                        "price": "string",
                                        "average_fill_price": "string"
                                    }
                                ]
                }
        :raises: Exception if requests.Response is not successful
        """

        endpoint = "/v1/orders"
        url = self.uri + endpoint

        body = {
            "contract_code": contract_code,
            "status": status,
            "before": before,
            "after": after
        }
        timestamp = get_timestamp()
        signature = generate_signature(self._api_secret, timestamp,
                                       "GET", endpoint, body)

        self._headers['EMX-ACCESS-KEY'] = self._api_key
        self._headers['EMX-ACCESS-SIG'] = signature.decode().strip()
        self._headers['EMX-ACCESS-TIMESTAMP'] = str(timestamp)
        result = self.session.get(url=url, json=body, headers=self._headers)
        if result.status_code != 200:
            raise EmxApiException("Request failed. Reason: {}".format(result.text))
        return result

    @handle_result
    def create_new_order(self, contract_code, order_type,
                         order_side, size, client_id="", price=""):
        if order_type != "market" and price is None:
            raise Exception("Specify the price, since order type is not market")

        body = {
          "client_id": client_id,
          "contract_code": contract_code,
          "type": order_type,
          "side": order_side,
          "size": size,
          "price": price,
        }

        endpoint = "/v1/orders"
        url = self.uri + endpoint
        timestamp = get_timestamp()
        signature = generate_signature(self._api_secret, timestamp,
                                       "POST", endpoint, body)

        self._headers['EMX-ACCESS-KEY'] = self._api_key
        self._headers['EMX-ACCESS-SIG'] = signature.decode().strip()
        self._headers['EMX-ACCESS-TIMESTAMP'] = str(timestamp)
        result = self.session.post(url=url, json=body, headers=self._headers)
        if result.status_code != 200:
            raise EmxApiException("Request failed. Reason: {}".format(result.text))
        return result

    @handle_result
    def get_contracts(self):
        endpoint = "/v1/contracts"
        self._headers = {
                         'content-type': 'application/json'
                        }

        url = self.uri + endpoint
        body_str = "{}"
        result = self.session.get(url=url, params=body_str, headers=self._headers)
        if result.status_code != 200:
            raise EmxApiException("Request failed. Reason: {}".format(result.text))
        return result

    def get_specific_contract(self, contract_code):
        endpoint = "/v1/contracts/{}".format(contract_code)
        self._headers = {
                         'content-type': 'application/json'
                        }

        url = self.uri + endpoint
        body_str = "{}"
        result = self.session.get(url=url, params=body_str, headers=self._headers)
        if result.status_code != 200:
            raise EmxApiException("Request failed. Reason: {}".format(result.text))
        return result
