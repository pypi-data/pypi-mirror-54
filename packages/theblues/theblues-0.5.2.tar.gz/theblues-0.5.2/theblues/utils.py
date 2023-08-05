import collections
import json
try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

import requests
from requests.exceptions import HTTPError

from theblues.errors import (
    log,
    ServerError,
    timeout_error,
)


API_URL = 'https://api.jujucharms.com/charmstore/v5'
DEFAULT_TIMEOUT = 3.05
_error_message = 'Error during request: {url} message: {message}'


def _server_error_message(url, message):
    """Log and return a server error message."""
    msg = _error_message.format(url=url, message=message)
    log.error(msg)
    return msg


def make_request(
        url, method='GET', query=None, body=None, auth=None, timeout=10,
        client=None, macaroons=None):
    """Make a request with the provided data.

    @param url The url to make the request to.
    @param method The HTTP request method (defaulting to "GET").
    @param query A dict of the query key and values.
    @param body The optional body as a string or as a JSON decoded dict.
    @param auth The optional username and password as a tuple,
    not used if client is not None
    @param timeout The request timeout in seconds, defaulting to 10 seconds.
    @param client (httpbakery.Client) holds a context for making http
    requests with macaroons.
    @param macaroons Optional JSON serialized, base64 encoded macaroons to be
        included in the request header.

    POST/PUT request bodies are assumed to be in JSON format.
    Return the response content as a JSON decoded object, or an empty dict.
    Raise a ServerError if a problem occurs in the request/response process.
    Raise a ValueError if invalid parameters are provided.
    """
    headers = {}
    kwargs = {'timeout': timeout, 'headers': headers}
    # Handle the request body.
    if body is not None:
        if isinstance(body, collections.Mapping):
            body = json.dumps(body)
        kwargs['data'] = body
    # Handle request methods.
    if method in ('GET', 'HEAD'):
        if query:
            url = '{}?{}'.format(url, urlencode(query, True))
    elif method in ('DELETE', 'PATCH', 'POST', 'PUT'):
        headers['Content-Type'] = 'application/json'
    else:
        raise ValueError('invalid method {}'.format(method))
    if macaroons is not None:
        headers['Macaroons'] = macaroons

    kwargs['auth'] = auth if client is None else client.auth()

    api_method = getattr(requests, method.lower())
    # Perform the request.
    try:
        response = api_method(url, **kwargs)
    except requests.exceptions.Timeout:
        raise timeout_error(url, timeout)
    except Exception as err:
        msg = _server_error_message(url, err)
        raise ServerError(msg)
    # Handle error responses.
    try:
        response.raise_for_status()
    except HTTPError as err:
        msg = _server_error_message(url, err.response.text)
        raise ServerError(err.response.status_code, msg)
    except requests.exceptions.RequestException as err:
        msg = _server_error_message(url, err.message)
        raise ServerError(msg)
    # Some requests just result in a status with no response body.
    if not response.content:
        return {}
    # Assume the response body is a JSON encoded string.
    try:
        return response.json()
    except Exception as err:
        msg = 'Error decoding JSON response: {} message: {}'.format(url, err)
        log.error(msg)
        raise ServerError(msg)


def ensure_trailing_slash(url):
    """Returns a url with a trailing slash

    @param url The url to ensure has a trailing slash
    """
    if not(url.endswith('/')):
        url += '/'
    return url
