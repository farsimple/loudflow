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
from typing import Any, Dict
from uuid import uuid4

from loguru import logger

from loudflow.common.decorators import trace


class Thing:
    """Thing class.

    Things populating the world.

    Attributes:
        config: Thing configuration data.

    """

    @trace()
    def __init__(self, config: ThingConfiguration) -> None:
        logger.info("Constructing thing...")
        self.id = str(uuid4())
        self.config = config
        self.name = config.name
        self.symbol = config.symbol
        self.x = config.x
        self.y = config.y


@dataclass(frozen=True)
class ThingConfiguration:
    """Thing configuration class.

    Immutable dataclass containing thing configuration data.

    Attributes:
    name: Thing name.
    x: X-coordinate of initial location of thing.
    y: Y-coordinate of initial location of thing.

    """

    name: str
    symbol: str
    x: int
    y: int

    def __post_init__(self) -> None:
        if self.name is None:
            message = "Missing required attribute [name: str] in thing configuration."
            logger.error(message)
            raise ValueError(message)
        if not isinstance(self.name, str):
            message = "Invalid type for attribute [name: str] in thing configuration."
            logger.error(message)
            raise ValueError(message)
        if self.symbol is None:
            message = "Missing required attribute [symbol: str] in thing configuration."
            logger.error(message)
            raise ValueError(message)
        if not isinstance(self.symbol, str):
            message = "Invalid type for attribute [symbol: str] in thing configuration."
            logger.error(message)
            raise ValueError(message)
        if len(self.symbol) > 1:
            message = "Invalid attribute [symbol: str] in thing configuration. Symbol must be a single character."
            logger.error(message)
            raise ValueError(message)
        if self.x is None:
            message = "Missing required attribute [x: int] in thing configuration."
            logger.error(message)
            raise ValueError(message)
        if not isinstance(self.x, int):
            message = "Invalid type for attribute [x: int] in thing configuration."
            logger.error(message)
            raise ValueError(message)
        if self.y is None:
            message = "Missing required attribute [y: int] in thing configuration."
            logger.error(message)
            raise ValueError(message)
        if not isinstance(self.y, int):
            message = "Invalid type for attribute [y: int] in thing configuration."
            logger.error(message)
            raise ValueError(message)

    @staticmethod
    @trace()
    def build(config: Dict) -> ThingConfiguration:
        """Build WorldConfiguration from dictionary of configuration data.

        Args:
            config: Dictionary containing configuration data.

        Returns:
            An instance of :py:class:`loudflow.realm.thing.ThingConfiguration`.
        """
        if config is None:
            message = "Missing required argument [config: Dict] in [ThingConfiguration.build] method call."
            logger.error(message)
            raise ValueError(message)
        if not isinstance(config, Dict):
            message = "Invalid argument type: [config: Dict] must be Dict in [ThingConfiguration.build] method call."
            logger.error(message)
            raise TypeError(message)
        # noinspection PyArgumentList
        # TODO: Remove noinspection after pycharm bug is fixed for incorrect unexpected argument warning for dataclasses
        return ThingConfiguration(
            name=config.get("name", None),
            symbol=config.get("symbol", None),
            x=config.get("x", None),
            y=config.get("y", None),
        )

    @trace()
    def copy(self, **attributes: Any) -> ThingConfiguration:
        """Copy WorldConfiguration state while replacing attributes with new values, and return new immutable instance.

        Args:
            **attributes: New configuration attributes.

        Returns:
            An instance of :py:class:`loudflow.realm.thing.ThingConfiguration`.
        """
        name = attributes.get("name", None) if "name" in attributes.keys() else self.name
        symbol = attributes.get("symbol", None) if "symbol" in attributes.keys() else self.symbol
        x = attributes.get("x", None) if "x" in attributes.keys() else self.x
        y = attributes.get("y", None) if "y" in attributes.keys() else self.y
        # noinspection PyArgumentList
        # TODO: Remove noinspection after pycharm bug is fixed for incorrect unexpected argument warning for dataclasses
        return ThingConfiguration(name=name, symbol=symbol, x=x, y=y)
