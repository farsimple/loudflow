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

from abc import abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, Optional
from uuid import uuid4

from loguru import logger
from rx.core import Observer
from rx.subject import Subject

from loudflow.common.decorators import timer, trace
from loudflow.realm.display.change import Change
from loudflow.realm.event.action_event import ActionDoneEvent, ActionEvent
from loudflow.realm.event.update_event import UpdateEvent
from loudflow.realm.thing.thing import Thing


class World(Observer):
    """World class.

    The world in which the agent(s) act.

    Attributes:
        config: World configuration data.

    """

    @trace()
    def __init__(self, config: WorldConfiguration) -> None:
        logger.info("Constructing world...")
        super().__init__()
        self.id = str(uuid4())
        self.config = config
        self.name = config.name
        self.width = config.width
        self.height = config.height
        self.things: Dict[str, Thing] = {}
        self.events = Subject()
        self.actions = Subject()
        self.subscription = None

    @abstractmethod
    def start(self) -> None:
        pass

    @abstractmethod
    def stop(self) -> None:
        pass

    @abstractmethod
    def destroy(self) -> None:
        pass

    @trace()
    def add(self, thing: Thing, replace: bool = True, silent: bool = True) -> bool:
        """Add thing to world.

        Args:
            thing: Thing.
            replace: If True, replace existing tile. If False, log warning.
            silent: If True, do not log warnings.

        Returns:
            True if thing is added, False if not.
        """
        if replace:
            self.things[thing.id] = thing
            return True
        else:
            check = self.things.get(thing.id, None)
            if check is None:
                self.things[thing.id] = thing
                return True
            else:
                if not silent:
                    logger.warning(
                        "Cannot place thing [{}] in world [{}] "
                        "because thing[{}] is already placed in that location.".format(thing.id, self.id, check.id)
                    )
            return False

    @trace()
    def remove(self, thing_id: str) -> None:
        """Remove thing from world.

        Args:
            thing_id: Thing identifier.

        """
        del self.things[thing_id]

    @trace()
    def move(self, thing_id: str, x: int, y: int) -> None:
        """Move thing.

        Args:
            thing_id: Thing identifier.
            x: Incremental movement in x-direction.
            y: Incremental movement in y-direction.

        """
        thing = self.things.get(thing_id, None)
        if thing is None:
            message = "Cannot find thing [{}] in world [{}].".format(thing_id, self.id)
            logger.error(message)
            raise ValueError(message)
        thing.x += x
        thing.y += y
        change = Change(thing.id, thing.x, thing.y)
        self.events.on_next(UpdateEvent(change=change))

    @trace()
    @timer()
    def on_next(self, event: ActionEvent) -> None:
        """Handles action events.

        Args:
            event: Action event.

        """
        if event.action.__class__.__name__ == "Move":
            self.move(event.action.actor, event.action.x, event.action.y)
            self.events.on_next(ActionDoneEvent(event.id))
        else:
            message = "Invalid action specified in action event."
            logger.error(message)
            raise ValueError(message)


@dataclass(frozen=True)  # type: ignore
class WorldConfiguration:
    """World configuration class.

    Immutable dataclass containing world configuration data.

    Attributes:
    name: World name.
    width: Width of 2D world as number of tiles in horizontal direction.
    height: Height of 2D world as number of tiles in horizontal direction.

    """

    name: str
    width: Optional[int]
    height: Optional[int]

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
    @abstractmethod
    def build(config: Dict) -> WorldConfiguration:
        """Build WorldConfiguration from dictionary of configuration data.

        Args:
            config: Dictionary containing configuration data.

        Returns:
            An instance of `loudflow.realm.world.world.WorldConfiguration`.
        """
        pass

    @abstractmethod
    def copy(self, **attributes: Any) -> WorldConfiguration:
        """Copy WorldConfiguration state while replacing attributes with new values, and return new immutable instance.

        Args:
            **attributes: New configuration attributes.

        Returns:
            An instance of `loudflow.realm.world.world.WorldConfiguration`.
        """
        pass
