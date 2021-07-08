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

from dataclasses import dataclass
from typing import Any, Optional

from loguru import logger

from loudflow.common.decorators import trace
from loudflow.realm.action.action import Action


@dataclass(frozen=True)
class Move(Action):
    """Move action class.

    Immutable dataclass for move action.

    Attributes:
    x: Incremental movement in x-direction.
    y: Incremental movement in y-direction.

    """

    actor: str
    target: Optional[str]
    x: int
    y: int

    def __post_init__(self) -> None:
        super().__post_init__()
        object.__setattr__(self, "target", None)
        if self.x is None:
            message = "Missing required attribute [x: int] in Move."
            logger.error(message)
            raise ValueError(message)
        if not isinstance(self.x, int):
            message = "Invalid type for attribute [x: int] in Move."
            logger.error(message)
            raise ValueError(message)
        if self.y is None:
            message = "Missing required attribute [y: int] in Move."
            logger.error(message)
            raise ValueError(message)
        if not isinstance(self.y, int):
            message = "Invalid type for attribute [y: int] in Move."
            logger.error(message)
            raise ValueError(message)

    @trace()
    def copy(self, **attributes: Any) -> Move:
        """Copy Move state while replacing attributes with new values, and return new immutable instance.

        Args:
            **attributes: New Move attributes.

        Returns:
            An instance of `loudflow.realm.action.move.Move`.
        """
        actor = attributes.get("actor", None) if "actor" in attributes.keys() else self.actor
        target = attributes.get("target", None) if "target" in attributes.keys() else self.target
        x = attributes.get("x", None) if "x" in attributes.keys() else self.x
        y = attributes.get("y", None) if "y" in attributes.keys() else self.y
        # noinspection PyArgumentList
        # TODO: Remove noinspection after pycharm bug is fixed for incorrect unexpected argument warning for dataclasses
        return Move(actor=actor, target=target, x=x, y=y)
