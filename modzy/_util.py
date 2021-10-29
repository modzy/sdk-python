# -*- coding: utf-8 -*-

import pathlib
from base64 import b64encode

def encode_data_uri(bytes_like, mimetype='application/octet-stream'):
    encoded = b64encode(bytes_like).decode('ascii')
    data_uri = 'data:{};base64,{}'.format(mimetype, encoded)
    return data_uri


def file_to_bytes(file_like):
    if hasattr(file_like, 'read'):  # File-like object
        if hasattr(file_like, 'seekable') and file_like.seekable():
            file_like.seek(0)
        maybe_bytes = file_like.read()
        if not isinstance(maybe_bytes, bytes):
            raise TypeError("the file object's 'read' function must return bytes not {}; "
                            "files should be opened using binary mode 'rb'"
                            .format(type(maybe_bytes).__name__))
        return maybe_bytes

    # should we just pass the object directly to `open` instead of trying to find the path ourselves?
    # would break pathlib.Path support on Python<3.6, but would be consistent with the Python version...
    if hasattr(file_like, '__fspath__'):  # os.PathLike
        path = file_like.__fspath__()
    elif isinstance(file_like, pathlib.Path):  # Python 3.4-3.5
        path = str(file_like)
    else:
        path = file_like

    with open(path, 'rb') as file:
        return file.read()


def file_to_chunks(file_like, chunk_size):
    file = None
    should_close = False
    if not hasattr(file_like, 'read'):
        if hasattr(file_like, '__fspath__'):  # os.PathLike
            path = file_like.__fspath__()
        elif isinstance(file_like, pathlib.Path):  # Python 3.4-3.5
            path = str(file_like)
        else:
            path = file_like
        file = open(path, 'rb')
        should_close = True
    else:
        file = file_like

    if hasattr(file, 'seekable') and file.seekable():
        file.seek(0)

    while True:
        chunk = file.read(chunk_size)
        if not chunk:
            break
        elif not isinstance(chunk, bytes):
            raise TypeError("the file object's 'read' function must return bytes not {}; "
                            "files should be opened using binary mode 'rb'"
                            .format(type(chunk).__name__))
        else:
            yield chunk

    if should_close:
        file.close()


def bytes_to_chunks(byte_array, chunk_size):
    for i in range(0, len(byte_array), chunk_size):
        yield byte_array[i:i + chunk_size]


def depth(d):
    if d and isinstance(d, dict):
        return max(depth(v) for k, v in d.items()) + 1
    return 0
