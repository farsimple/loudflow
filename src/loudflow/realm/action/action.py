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

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Optional

from loguru import logger


@dataclass(frozen=True)  # type: ignore
class Action(ABC):
    """Action class.

    Immutable dataclass describing action.

    Attributes:
    actor: Identifier of thing which is acting.
    target: Identifier of thing which is acted on. Use None, if nothing is acted on.

    """

    actor: str
    target: Optional[str]

    def __post_init__(self) -> None:
        if self.actor is None:
            message = "Missing required attribute [actor: str] in Action."
            logger.error(message)
            raise ValueError(message)
        if not isinstance(self.actor, str):
            message = "Invalid type for attribute [actor: str] in Action."
            logger.error(message)
            raise ValueError(message)
        if self.target is not None and not isinstance(self.target, str):
            message = "Invalid type for attribute [target: str] in Action."
            logger.error(message)
            raise ValueError(message)

    @abstractmethod
    def copy(self, **attributes: Any) -> Action:
        """Copy Action state while replacing attributes with new values, and return new immutable instance.

        Args:
            **attributes: New action attributes.

        Returns:
            An instance of Any.
        """
        pass
