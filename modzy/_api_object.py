# -*- coding: utf-8 -*-

import json
import re
from keyword import iskeyword


def to_snake_case(name):
    return re.sub('((?<=[a-z0-9])[A-Z]|(?!^)(?<!_)[A-Z](?=[a-z]))', r'_\1', name).lower()


def is_safe_attribute(name):
    if iskeyword(name):
        return False
    return bool(re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', name))


class ApiObject(dict):
    def __init__(self, json_obj, api_client=None):
        if api_client:
            object.__setattr__(self, '_api_client', api_client)
        super().__init__(json_obj)

    def _find_equivalent_snake_case_key(self, key):
        # TODO: should we worry about duplicates?
        for self_key in self:
            if isinstance(self_key, str):
                snake_cased = to_snake_case(self_key)
                if snake_cased == key:
                    return self_key
        raise AttributeError("'{}' object has no attribute '{}'"
                             .format(self.__class__.__name__, key))

    def __getattr__(self, key):
        if key in self:
            return self[key]
        key = self._find_equivalent_snake_case_key(key)
        return self[key]

    def __setattr__(self, key, value):
        if key in self:
            self[key] = value
            return
        key = self._find_equivalent_snake_case_key(key)
        self[key] = value

    def __delattr__(self, key, value):
        # should we not provide attribute deletion?
        if key in self:
            del self[key]
            return
        key = self._find_equivalent_snake_case_key(key)
        del[key]

    def __dir__(self):
        items = set(super().__dir__())
        for key in self:
            if isinstance(key, str):
                snake_cased = to_snake_case(key)
                if is_safe_attribute(snake_cased):
                    items.add(snake_cased)
        return list(items)

    def __repr__(self):
        json_repr = json.dumps(self, sort_keys=True, indent=2, default=repr)
        return '{}({})'.format(self.__class__.__name__, json_repr)
