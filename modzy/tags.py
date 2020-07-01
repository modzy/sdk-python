# -*- coding: utf-8 -*-
"""Classes for interacting with tags."""

import logging

from ._api_object import ApiObject
from .models import Model


class Tags:
    """The `Tags` object.

    This object is used to retreive information about tags from the API.

    Note:
        This class should not be instantiated directly but rather accessed through the `tags`
        attribute of an `ApiClient` instance.
    """

    _base_route = '/models/tags'

    def __init__(self, api_client):
        """Creates a `Tags` instance.

        Args:
            api_client (ApiClient): An `ApiClient` instance.
        """
        self._api_client = api_client
        self.logger = logging.getLogger(__name__)

    def get_all(self):
        """Gets a list of all `Tag` instances.
        Returns:
            List[Tag]: A list of `Tag` instances.
        Raises:
            ApiError: A subclass of ApiError will be raised if the API returns an error status,
                or the client is unable to connect.
        """
        json_list = self._api_client.http.get(self._base_route)
        return list(Tag(json_obj, self._api_client) for json_obj in json_list)

    def get_tags_and_models(self, tag_identifiers):
        """Get a list of all `Tag` instances provided in the `tag_identifiers` argument,
           with all the models that are related to those tags.

        Args:
            tag_identifiers (Union[str, Tag, Sequence[Union[str, Tag]] ]): the tags identifiers

        Returns:
            Tuple[List[Tag], List[Model]]: A tuple containing the list of `Tag` and `Model` instances

        Raises:
            ApiError: A subclass of ApiError will be raised if the API returns an error status,
                or the client is unable to connect.
        """
        try:
            tag_identifiers = Tag._coerce_identifier(tag_identifiers)
        except TypeError:
            tag_identifiers = ','.join(Tag._coerce_identifier(identifier) for identifier in tag_identifiers)
        self.logger.debug("getting tags %s", tag_identifiers)
        url = '{}/{}'.format(self._base_route, tag_identifiers)
        json_obj = self._api_client.http.get(url)
        return (list(Model(json_tag, self._api_client) for json_tag in json_obj.tags),
                list(Model(json_model, self._api_client) for json_model in json_obj.models))


class Tag(ApiObject):
    """A tag object.

    This object contains a parsed copy of the information returned from the server about a certain tag.

    Attributes:
        identifier (str): The tag identifier.

    Note:
        This class should not be instantiated directly. Instead, it is returned by various package
        functions.

        This object is a `dict` subclass that also supports attribute access. Information can be
        accessed through dotted attribute notation using "snake_case" or the original "camelCase" JSON
        key name (``tag.data_type`` or ``tag.dataType``). Alternatively, the original
        "camelCase" JSON key can be used with bracketed key access notation (``tag['dataType']``).
    """

    @classmethod
    def _coerce_identifier(cls, maybe_tag):
        identifier = getattr(maybe_tag, 'identifier', maybe_tag)
        if not isinstance(identifier, str):
            raise TypeError('the identifier must be {} or str, not {}'
                            .format(cls.__name__, type(maybe_tag).__name__))
        return identifier

    def __str__(self):
        return "Tag(identifier='{}',name='{}')".format(self.identifier, self.name)
