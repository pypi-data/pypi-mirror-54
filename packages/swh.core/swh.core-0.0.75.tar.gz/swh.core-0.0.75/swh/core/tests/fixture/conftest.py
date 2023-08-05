# Copyright (C) 2019  The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

import pytest

from os import path


DATADIR = path.join(path.abspath(path.dirname(__file__)), 'data')


@pytest.fixture
def datadir():
    return DATADIR
