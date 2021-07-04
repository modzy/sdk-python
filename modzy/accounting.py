# -*- coding: utf-8 -*-
"""Classes for interacting with results."""

import logging
from typing import List

from ._api_object import ApiObject


class Accounting:
    """The `Accounting` object.

    This object is used to retrieve information about accounting from the API.

    Note:
        This class should not be instantiated directly but rather accessed through the `accounting`
        attribute of an `ApiClient` instance.
    """

    _base_route = '/accounting'

    def __init__(self, api_client):
        """Creates a `Accounting` instance.

        Args:
            api_client (ApiClient): An `ApiClient` instance.
        """
        self._api_client = api_client
        self.logger = logging.getLogger(__name__)

    def list_entitlements(self) -> List[ApiObject]:
        """
        Obtains a detailed list of all the entitlements associated with the current client.

        Returns:
            entitlements: list of ApiObjects containing metadata for each entitlement present
        """
        endpoint = f"{self._base_route}/entitlements"
        entitlements = self._api_client.http.get(endpoint)
        return entitlements

    def has_entitlement(self, entitlement_identifier: str) -> bool:
        """
        Determines if the Modzy client user has the provided endpoint

        Args:
            entitlement_identifier: single identifier that can be found in reference
                https://models.modzy.com/docs/api-reference-guides/authorization

        Returns:
            _has_entitlement: True if the current client has the entitlement, false otherwise
        """
        entitlement_identifiers = [entitlement["identifier"] for entitlement in self.list_entitlements()]
        _has_entitlement = entitlement_identifier in entitlement_identifiers
        self.logger.info(f"Entitlement `{entitlement_identifier}` {'' if _has_entitlement else 'not '}found")
        return _has_entitlement
