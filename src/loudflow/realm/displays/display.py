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
from typing import Any, Dict, Union
from uuid import uuid4

from loguru import logger
from rx.core import Observer
from rx.operators import filter

from loudflow.common.decorators import timer, trace
from loudflow.realm.events.action_event import ActionFailed, ActionSucceeded
from loudflow.realm.worlds.world import World


class Display(Observer):
    """Base displays class.

    The displays in which the worlds and its occupants may be viewed.

    Attributes:
        world: World
        config: World configuration data.

    """

    @trace()
    def __init__(self, world: World, config: DisplayConfiguration) -> None:
        logger.info("Constructing displays...")
        super().__init__()
        self.id = str(uuid4())
        self.world = world
        self.config = config
        self.subscription = None

    @abstractmethod
    def event_handler(self, event: Any) -> None:
        """Handle displays events.

        Args:
            event: Display events.

        """
        pass

    @abstractmethod
    def show(self) -> None:
        """Show worlds in the displays."""
        pipe = self.world.events.pipe(
            filter(lambda event: isinstance(event, ActionSucceeded) or isinstance(event, ActionFailed))
        )
        self.subscription = pipe.subscribe(self)

    @abstractmethod
    def update(self) -> None:
        """Update displays."""
        pass

    @trace()
    @timer()
    def on_next(self, event: Union[ActionFailed, ActionSucceeded]) -> None:
        """Handles update events.

        Args:
            event: Update events.

        """
        self.update()


@dataclass(frozen=True)  # type: ignore
class DisplayConfiguration(ABC):
    """Display configuration class.

    Immutable dataclass containing DisplayConfiguration data.
    """

    @staticmethod
    @abstractmethod
    def build(config: Dict) -> DisplayConfiguration:
        """Build DisplayConfiguration from dictionary of configuration data.

        Args:
            config: Dictionary containing configuration data.

        Returns:
            An instance of `loudflow.realm.displays.displays.DisplayConfiguration`.
        """
        pass

    @abstractmethod
    def copy(self, **attributes: Any) -> DisplayConfiguration:
        """
        Copy DisplayConfiguration state while replacing attributes with new values, and return new immutable instance.

        Args:
            **attributes: New configuration attributes.

        Returns:
            An instance of `loudflow.realm.displays.displays.DisplayConfiguration`.
        """
        pass
