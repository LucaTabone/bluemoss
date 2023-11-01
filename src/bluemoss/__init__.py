# -*- coding: utf-8 -*-

__title__ = 'bluemoss'
__author__ = 'LucaTabone'
__license__ = 'APACHE'
__copyright__ = 'Copyright 2023-2023 LucaTabone'
__version__ = '0.1.25'

from .classes import (
    BlueMoss,
    Node,
    Root,
    Range,
    Ex,
    InvalidTargetTypeException,
    InvalidKeysForTargetException,
    JsonifyWithTag,
    Jsonify,
    InvalidXpathException,
    PartialKeysException,
    EqualIndicesException,
    MissingTargetKeysException,
)
from .extract import extract
