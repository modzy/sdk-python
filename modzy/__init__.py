# -*- coding: utf-8 -*-
"""Modzy Python API Client."""

import logging

from .client import ApiClient  # noqa
from .edge.client import EdgeClient
__version__ = '0.7.1'

logging.getLogger(__name__).addHandler(logging.NullHandler())
