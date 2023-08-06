# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CERN.
# Copyright (C) 2019 Northwestern University.
#
# Invenio-Records-Permissions is free software; you can redistribute it
# and/or modify it under the terms of the MIT License; see LICENSE file for
# more details.

"""Pytest configuration.

See https://pytest-invenio.readthedocs.io/ for documentation on which test
fixtures are available.
"""

from __future__ import absolute_import, print_function

import shutil
import tempfile

import pytest
from flask import Flask
from flask_babelex import Babel
from invenio_access import InvenioAccess
from invenio_accounts import InvenioAccounts
from invenio_db import InvenioDB
from invenio_search import InvenioSearch

from invenio_records_permissions import InvenioRecordsPermissions


@pytest.fixture(scope='module')
def celery_config():
    """Override pytest-invenio fixture.

    TODO: Remove this fixture if you add Celery support.
    """
    return {}


@pytest.fixture(scope='module')
def create_app(instance_path):
    """Application factory fixture."""
    def factory(**config):
        app = Flask('testapp', instance_path=instance_path)
        app.config.update(**config)
        Babel(app)
        InvenioAccess(app)
        InvenioAccounts(app)
        InvenioDB(app)
        InvenioRecordsPermissions(app)
        InvenioSearch(app)
        return app
    return factory
