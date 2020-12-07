# -*- coding: utf-8 -*-
"""Modzy Python API Client."""

import logging

from .client import ApiClient  # noqa

__version__ = '0.5.2'

logging.getLogger(__name__).addHandler(logging.NullHandler())
