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
from pydispatch import dispatcher

from loudflow.common.decorators import timer, trace
from loudflow.realm.display.change import Change
from loudflow.realm.event.action_event import ActionDoneEvent, ActionEvent
from loudflow.realm.event.update_event import UpdateEvent
from loudflow.realm.thing.thing import Thing


class World:
    """World class.

    The world in which the agent(s) act.

    Attributes:
        config: World configuration data.

    """

    @trace()
    def __init__(self, config: WorldConfiguration) -> None:
        logger.info("Constructing world...")
        self.id = str(uuid4())
        self.config = config
        self.name = config.name
        self.width = config.width
        self.height = config.height
        self.things: Dict[str, Thing] = {}
        dispatcher.connect(self.action_handler, signal=ActionEvent.__name__, sender=dispatcher.Any)

    @trace()
    def add(self, thing: Thing) -> None:
        """Add thing to world.

        Args:
            thing: Thing.

        """
        self.things[thing.id] = thing

    @trace()
    def remove(self, thing_id: str) -> None:
        """Remove thing from world.

        Args:
            thing_id: Thing identifier.

        """
        del self.things[thing_id]

    @trace()
    @timer()
    def action_handler(self, signal: Any, sender: Any, event: ActionEvent) -> None:
        """Handles action events.

        Args:
            signal: Action event signal.
            sender: Action event sender.
            event: Action event.

        """
        if event.action.__class__.__name__ == "Move":
            thing = self.things.get(event.action.actor, None)
            if thing is None:
                message = "Cannot find thing [{}] in world [{}].".format(event.action.actor, self.id)
                logger.error(message)
                raise ValueError(message)
            thing.x += event.action.x
            thing.y += event.action.y
            dispatcher.send(signal=ActionDoneEvent.__name__, event=ActionDoneEvent(event.id))
            change = Change(thing.id, thing.x, thing.y)
            dispatcher.send(signal=UpdateEvent.__name__, event=UpdateEvent(change=change))
        else:
            message = "Invalid action specified in action event."
            logger.error(message)
            raise ValueError(message)


@dataclass(frozen=True)
class WorldConfiguration:
    """World configuration class.

    Immutable dataclass containing world configuration data.

    Attributes:
    name: World name.
    width: Width of 2D world as number of tiles in horizontal direction.
    height: Height of 2D world as number of tiles in horizontal direction.

    """

    name: str
    width: int = 80
    height: int = 50

    def __post_init__(self) -> None:
        if self.name is None:
            message = "Missing required attribute [name: str] in WorldConfiguration."
            logger.error(message)
            raise ValueError(message)
        if not isinstance(self.name, str):
            message = "Invalid type for attribute [name: str] in WorldConfiguration."
            logger.error(message)
            raise ValueError(message)
        if self.width is None:
            object.__setattr__(self, "width", 80)
        if not isinstance(self.width, int):
            message = "Invalid type for attribute [width: int] in WorldConfiguration."
            logger.error(message)
            raise ValueError(message)
        if self.height is None:
            object.__setattr__(self, "height", 50)
        if not isinstance(self.height, int):
            message = "Invalid type for attribute [height: int] in WorldConfiguration."
            logger.error(message)
            raise ValueError(message)

    @staticmethod
    @trace()
    def build(config: Dict) -> WorldConfiguration:
        """Build WorldConfiguration from dictionary of configuration data.

        Args:
            config: Dictionary containing configuration data.

        Returns:
            An instance of `loudflow.realm.world.world.WorldConfiguration`.
        """
        if config is None:
            message = "Missing required argument [config: Dict] in [WorldConfiguration.build] method call."
            logger.error(message)
            raise ValueError(message)
        if not isinstance(config, Dict):
            message = "Invalid argument type: [config: Dict] must be Dict in [WorldConfiguration.build] method call."
            logger.error(message)
            raise TypeError(message)
        # noinspection PyArgumentList
        # TODO: Remove noinspection after pycharm bug is fixed for incorrect unexpected argument warning for dataclasses
        return WorldConfiguration(
            name=config.get("name", None), width=config.get("width", None), height=config.get("height", None)
        )

    @trace()
    def copy(self, **attributes: Any) -> WorldConfiguration:
        """Copy WorldConfiguration state while replacing attributes with new values, and return new immutable instance.

        Args:
            **attributes: New configuration attributes.

        Returns:
            An instance of `loudflow.realm.world.world.WorldConfiguration`.
        """
        name = attributes.get("name", None) if "name" in attributes.keys() else self.name
        width = attributes.get("width", None) if "width" in attributes.keys() else self.width
        height = attributes.get("height", None) if "height" in attributes.keys() else self.height
        # noinspection PyArgumentList
        # TODO: Remove noinspection after pycharm bug is fixed for incorrect unexpected argument warning for dataclasses
        return WorldConfiguration(name=name, width=width, height=height)
