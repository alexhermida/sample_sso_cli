from unittest.mock import Mock, patch

import pytest
from requests.exceptions import HTTPError

from auth import request_device_code


def test_request_device_code():
    post_response = {
        "device_code": "<<device>>",
        "user_code": "0000-1111",
        "verification_uri": "<<url>>/activate",
        "expires_in": 900,
        "interval": 5,
        "verification_uri_complete": "<<url>>/activate?user_code=0000-1111",
    }

    with patch("auth.requests") as mock_requests:
        mock_data = Mock(return_value=post_response)
        mock_requests.post.return_value.json = mock_data

        device_response_code = request_device_code()

        assert device_response_code.device_code == post_response["device_code"]


def test_request_device_code_fail():
    with patch("auth.requests") as mock_requests:
        mock_response = Mock(status_code=403)
        mock_response.raise_for_status.side_effect = HTTPError()

        mock_requests.post.return_value = mock_response

        with pytest.raises(HTTPError):
            request_device_code()
