#  ********************************************************************************
#
#     ____ ___  ____ _____ ____
#    / __ `__ \/ __ `/ __ `/ _ \    A Multi-Agent
#   / / / / / / /_/ / /_/ /  __/    Framework in Python
#  /_/ /_/ /_/\__,_/\__, /\___/
#                  /____/
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

from loguru import logger

from common.decorators import timer, tracer


class World:
    """World class.

    The world in which the agent(s) act.

    Attributes:
        config: World configuration data.

    """

    @tracer()
    def __init__(self, config: WorldConfiguration) -> None:
        logger.info("Constructing world...")
        self.config = config

    @tracer()
    @timer()
    def hello(self) -> str:
        """Returns hello world string.

        Returns:
            Hello message using world name.

        """
        return "Hello {}!".format(self.config.name)


@dataclass(frozen=True)
class WorldConfiguration:
    """World configuration class.

    Immutable dataclass containing world configuration data.

    Attributes:
    name: World name.

    """

    name: str

    def __post_init__(self) -> None:
        if self.name is None:
            message = "Missing required attribute [name: str] in WorldConfiguration."
            logger.error(message)
            raise ValueError(message)
        if not isinstance(self.name, str):
            message = "Invalid type for attribute [name: str] in WorldConfiguration."
            logger.error(message)
            raise ValueError(message)

    @staticmethod
    @tracer()
    def build(config: Dict) -> WorldConfiguration:
        """Build WorldConfiguration from dictionary of configuration data.

        Args:
            config: Dictionary containing configuration data.

        Returns:
            An instance of :py:class:`mage.realm.WorldConfiguration`.
        """
        if config is None:
            message = "Missing required argument [config: Dict] in [World.build] method call."
            logger.error(message)
            raise ValueError(message)
        if not isinstance(config, Dict):
            message = "Invalid argument type: [config: Dict] must be Dict."
            logger.error(message)
            raise TypeError(message)
        name = config.get("name", None)
        if name is None:
            message = "Missing required field [name: str] in argument [config: Dict]."
            logger.error(message)
            raise ValueError(message)
        if not isinstance(name, str):
            message = "Invalid type for field [name: str] in argument [config: Dict]."
            logger.error(message)
            raise ValueError(message)
        # noinspection PyArgumentList
        # TODO: Remove noinspection after pycharm bug is fixed for incorrect unexpected argument warning for dataclasses
        return WorldConfiguration(name=name)

    @tracer()
    def copy(self, **attributes: Any) -> WorldConfiguration:
        """Copy WorldConfiguration state while replacing attributes with new values, and return new immutable instance.

        Args:
            **attributes: New configuration attributes.

        Returns:
            An instance of :py:class:`mage.realm.WorldConfiguration`.
        """
        name = str(attributes.get("name")) if "name" in attributes.keys() else self.name
        if name is None:
            message = "Value of [name: str] cannot be None."
            logger.error(message)
            raise ValueError(message)
        if not isinstance(name, str):
            message = "Invalid type for field [name: str] in argument [attributes]."
            logger.error(message)
            raise ValueError(message)
        # noinspection PyArgumentList
        # TODO: Remove noinspection after pycharm bug is fixed for incorrect unexpected argument warning for dataclasses
        return WorldConfiguration(name=name)
