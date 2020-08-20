#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `modzy` package."""

from modzy import ApiClient


def test_can_construct_client():
    client = ApiClient('https://example.com', 'my-key')
    assert client is not None

# TODO: actual test suite
