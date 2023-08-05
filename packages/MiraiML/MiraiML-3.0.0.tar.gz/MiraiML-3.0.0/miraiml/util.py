"""
:mod:`miraiml.util` provides utility functions that are used by higher level
modules.
"""

from threading import Thread
import random as rnd
import pickle
import string
import math


def load(path):
    """
    A clean `pickle.load` wrapper for binary files.

    :type path: string
    :param path: The path of the binary file to be loaded.

    :rtype: object
    :returns: The loaded object.
    """
    return pickle.load(open(path, 'rb'))


def dump(obj, path):
    """
    Optimizes the process of writing objects on disc by triggering a thread.

    :type obj: object
    :param obj: The object to be dumped to the binary file.

    :type path: string
    :param path: The path of the binary file to be written.
    """
    Thread(target=lambda: pickle.dump(obj, open(path, 'wb'))).start()


def sample_random_len(lst):
    """
    Returns a sample of random size from the list ``lst``. The minimum length of
    the returned list is 1.

    :type lst: list
    :param lst: A list containing the elements to be sampled.

    :rtype: sampled_lst: list
    :returns: The randomly sampled elements from ``lst``.
    """
    if len(lst) == 0:
        return []
    return rnd.sample(lst, max(1, math.ceil(rnd.random()*len(lst))))


__valid_filename_chars__ = frozenset('-_.() %s%s' % (string.ascii_letters,
                                                     string.digits))


def is_valid_filename(filename):
    """
    Tells whether a string can be used as a safe file name or not.

    :type filename: str
    :param filename: The file name.

    :rtype: bool
    :returns: Whether ``filename`` is a valid file name or not.
    """
    filename = filename.strip()
    if len(filename) == 0 or '..' in filename or filename == '.':
        return False
    for char in filename:
        if char not in __valid_filename_chars__:
            return False
    return True


__valid_pipeline_chars__ = frozenset('_%s%s' % (string.ascii_letters,
                                                string.digits))


def is_valid_pipeline_name(pipeline_name):
    """
    Tells whether a string can be used to compose pipelines or not.

    :type pipeline_name: str
    :param pipeline_name: The file name.

    :rtype: bool
    :returns: Whether ``pipeline_name`` is a valid name or not.
    """
    if len(pipeline_name) == 0 or '__' in pipeline_name \
            or pipeline_name[0] in string.digits:
        return False
    for char in pipeline_name:
        if char not in __valid_pipeline_chars__:
            return False
    return True
