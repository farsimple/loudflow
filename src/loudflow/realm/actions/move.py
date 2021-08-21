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

from loguru import logger

from loudflow.realm.actions.action import Action


@dataclass(frozen=True)
class Move(Action):
    """Move actions class.

    Immutable dataclass for move actions.

    Attributes:
    x: Incremental movement in x-direction.
    y: Incremental movement in y-direction.

    """

    dx: int
    dy: int

    def __post_init__(self) -> None:
        super().__post_init__()
        if self.dx is None:
            message = "Missing required attribute [dx: int] in Move."
            logger.error(message)
            raise ValueError(message)
        if not isinstance(self.dx, int):
            message = "Invalid type for attribute [dx: int] in Move."
            logger.error(message)
            raise ValueError(message)
        if self.dy is None:
            message = "Missing required attribute [dy: int] in Move."
            logger.error(message)
            raise ValueError(message)
        if not isinstance(self.dy, int):
            message = "Invalid type for attribute [dy: int] in Move."
            logger.error(message)
            raise ValueError(message)
