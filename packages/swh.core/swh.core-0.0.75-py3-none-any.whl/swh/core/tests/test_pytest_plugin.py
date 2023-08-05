# Copyright (C) 2019  The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

import requests

from os import path

from swh.core.pytest_plugin import requests_mock_datadir_factory


def test_get_response_cb_with_visits_nominal(requests_mock_datadir_visits):
    response = requests.get('https://example.com/file.json')
    assert response.ok
    assert response.json() == {'hello': 'you'}

    response = requests.get('http://example.com/something.json')
    assert response.ok
    assert response.json() == "something"

    response = requests.get('https://example.com/file.json')
    assert response.ok
    assert response.json() == {'hello': 'world'}

    response = requests.get('https://example.com/file.json')
    assert not response.ok
    assert response.status_code == 404


def test_get_response_cb_with_visits(requests_mock_datadir_visits):
    response = requests.get('https://example.com/file.json')
    assert response.ok
    assert response.json() == {'hello': 'you'}

    response = requests.get('https://example.com/other.json')
    assert response.ok
    assert response.json() == "foobar"

    response = requests.get('https://example.com/file.json')
    assert response.ok
    assert response.json() == {'hello': 'world'}

    response = requests.get('https://example.com/other.json')
    assert not response.ok
    assert response.status_code == 404

    response = requests.get('https://example.com/file.json')
    assert not response.ok
    assert response.status_code == 404


def test_get_response_cb_no_visit(requests_mock_datadir):
    response = requests.get('https://example.com/file.json')
    assert response.ok
    assert response.json() == {'hello': 'you'}

    response = requests.get('https://example.com/file.json')
    assert response.ok
    assert response.json() == {'hello': 'you'}


def test_get_response_cb_query_params(requests_mock_datadir):
    response = requests.get('https://example.com/file.json?toto=42')
    assert not response.ok
    assert response.status_code == 404

    response = requests.get(
        'https://example.com/file.json?name=doe&firstname=jane')
    assert response.ok
    assert response.json() == {'hello': 'jane doe'}


requests_mock_datadir_ignore = requests_mock_datadir_factory(
    ignore_urls=['https://example.com/file.json'],
    has_multi_visit=False,
)


def test_get_response_cb_ignore_url(requests_mock_datadir_ignore):
    response = requests.get('https://example.com/file.json')
    assert not response.ok
    assert response.status_code == 404


requests_mock_datadir_ignore_and_visit = requests_mock_datadir_factory(
    ignore_urls=['https://example.com/file.json'],
    has_multi_visit=True,
)


def test_get_response_cb_ignore_url_with_visit(
        requests_mock_datadir_ignore_and_visit):
    response = requests.get('https://example.com/file.json')
    assert not response.ok
    assert response.status_code == 404

    response = requests.get('https://example.com/file.json')
    assert not response.ok
    assert response.status_code == 404


def test_data_dir(datadir):
    expected_datadir = path.join(path.abspath(path.dirname(__file__)), 'data')
    assert datadir == expected_datadir
