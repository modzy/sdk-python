# -*- coding: utf-8 -*-

import pathlib
from base64 import b64encode
import logging
logger = logging.getLogger(__name__)


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
    logger.debug(f"file_to_chunks({type(file_like)} :: {file_like}, {chunk_size}) :: splitting ")
    file = None
    if not hasattr(file_like, 'read'):
        if hasattr(file_like, '__fspath__'):  # os.PathLike
            path = file_like.__fspath__()
        elif isinstance(file_like, pathlib.Path):  # Python 3.4-3.5
            path = str(file_like)
        else:
            path = file_like
        file = open(path, 'rb')
    else:
        file = file_like

    if hasattr(file, 'seekable') and file.seekable():
        file.seek(0)

    i = 0
    while True:
        chunk = file.read(chunk_size)
        logger.debug(f"file_to_chunks({type(file)}, {chunk_size}) :: chunk [{i}:{i + chunk_size}]")
        i += 1
        if not chunk:
            break
        if not isinstance(chunk, bytes):
            raise TypeError("the file object's 'read' function must return bytes not {}; "
                            "files should be opened using binary mode 'rb'"
                            .format(type(chunk).__name__))
        yield chunk

    if file and hasattr(file, 'close'):
        file.close()


def bytes_to_chunks(byte_array, chunk_size):
    logger.debug(f"bytes_to_chunks({len(byte_array)}, {chunk_size}) :: splitting")
    for i in range(0, len(byte_array), chunk_size):
        logger.debug(f"bytes_to_chunks({len(byte_array)}, {chunk_size}) :: slice [{i}:{i+chunk_size}]")
        yield byte_array[i:i + chunk_size]
