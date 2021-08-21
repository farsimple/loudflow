#  ********************************************************************************
#
#      __                ________
#     / /___  __  ______/ / __/ /___ _      __
#    / / __ \/ / / / __  / /_/ / __ \ | /| / /      A Multi-Agent Framework
#   / / /_/ / /_/ / /_/ / __/ / /_/ / |/ |/ /       in Python
#  /_/\____/\__,_/\__,_/_/ /_/\____/|__/|__/
#
#  Copyright (c) 2021-2022 FarSimple Oy.
#
#  The MIT License (MIT)
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software
#  and associated documentation files (the "Software"), to deal in the Software without restriction,
#  including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,
#  and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so,
#  subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included
#  in all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
#  INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
#  WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH
#  THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#  ********************************************************************************

from __future__ import annotations

from enum import Enum
from typing import Optional

from loguru import logger
from wonderwords import RandomWord

_random_word_generator = RandomWord()


class FromStringEnum(Enum):
    @staticmethod
    def default() -> Optional[FromStringEnum]:
        return None

    @classmethod
    def from_string(cls, name: str) -> FromStringEnum:
        """Map string to enum value.

        Returns:
        Enum value.
        """
        for key, value in cls.__members__.items():
            if key == name.upper():
                return value
        default = cls.default()
        if default:
            return default
        else:
            error = ValueError("Name {} does not match any valid {} enum value.".format(name, cls))
            logger.error(repr(error))
            raise error


def random_adjective() -> str:
    """Generate random adjective.

    Returns:
        A random adjective.
    """
    return _random_word_generator.word(include_categories=["adjectives"]).lower().capitalize()
