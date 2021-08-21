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
from loudflow.realm.actions.move import Move
from loudflow.realm.events.action_event import (
    ActionBlocked,
    ActionEvent,
    ActionNotAllowed,
    ActionSucceeded,
    ActorDestroyed,
)
from loudflow.realm.things.thing import Thing


class World(Observer):
    """World class.

    The worlds in which the agent(s) act.

    Attributes:
        config: World configuration data.

    """

    @trace()
    def __init__(self, config: WorldConfiguration) -> None:
        logger.info("Constructing worlds...")
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
        """Add things to worlds.

        Args:
            thing: Thing.
            replace: If True, replace existing tile. If False, log warning.
            silent: If True, do not log warnings.

        Returns:
            True if things is added, False if not.
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
                        "Cannot place things [{}] in worlds [{}] "
                        "because things[{}] is already placed in that location.".format(thing.id, self.id, check.id)
                    )
            return False

    @trace()
    def remove(self, thing_id: str) -> None:
        """Remove things from worlds.

        Args:
            thing_id: Thing identifier.

        """
        del self.things[thing_id]

    @trace()
    def move(self, event: ActionEvent) -> None:
        """Move thing.

        Args:
            event: Action event.

        """
        actor = self.things.get(event.action.actor, None)
        if actor is None:
            message = "Cannot move thing [{}] because it cannot be found in world [{}].".format(
                event.action.actor, self.id
            )
            logger.error(message)
            raise ValueError(message)
        self._do_move(actor, event.action.dx, event.action.dy, event.event_id)

    @trace()
    def _do_move(self, actor: Thing, dx: int, dy: int, event_id: str) -> None:
        if actor.can_move:
            occupant = self.locate(actor.x + dx, actor.y + dy)
            if occupant is None:
                logger.debug("Moving {}[{}].".format(actor.kind, actor.id))
                actor.x += dx
                actor.y += dy
                self.events.on_next(ActionSucceeded(action_event_id=event_id))
            else:
                self._do_move_with_occupant(actor, dx, dy, occupant, event_id)
        else:
            message = "{}[{}] is not movable.".format(actor.kind, actor.id)
            logger.debug(message)
            self.events.on_next(ActionNotAllowed(action_event_id=event_id))

    @trace()
    def _do_move_with_occupant(self, actor: Thing, dx: int, dy: int, occupant: Thing, event_id: str) -> None:
        if actor.pushes(occupant):
            logger.debug("{}[{}] is pushing occupant {}[{}].".format(actor.kind, actor.id, occupant.kind, occupant.id))
            action = ActionEvent(action=Move(actor=occupant.id, dx=dx, dy=dy))
            self.actions.on_next(action)
            logger.debug("Moving {}[{}].".format(actor.kind, actor.id))
            actor.x += dx
            actor.y += dy
            self.events.on_next(ActionSucceeded(action_event_id=event_id))
        elif actor.destroys(occupant) and actor.is_destroyed_by(occupant):
            logger.debug(
                "{}[{}] and {}[{}] destroyed each other.".format(actor.kind, actor.id, occupant.kind, occupant.id)
            )
            self.remove(actor.id)
            self.remove(occupant.id)
            self.events.on_next(ActorDestroyed(action_event_id=event_id, destroyed_by=occupant.id))
        elif actor.destroys(occupant):
            logger.debug("{}[{}] destroyed {}[{}].".format(actor.kind, actor.id, occupant.kind, occupant.id))
            self.remove(occupant.id)
            logger.debug("Moving {}[{}].".format(actor.kind, actor.id))
            actor.x += dx
            actor.y += dy
            self.events.on_next(ActionSucceeded(action_event_id=event_id))
        elif actor.is_destroyed_by(occupant):
            logger.debug("{}[{}] destroyed {}[{}].".format(occupant.kind, occupant.id, actor.kind, actor.id))
            self.remove(actor.id)
            self.events.on_next(ActorDestroyed(action_event_id=event_id, destroyed_by=occupant.id))
        else:
            message = "Cannot move {}[{}] into same location with unmovable and indestructible {}[{}].".format(
                actor.kind, actor.id, occupant.kind, occupant.id
            )
            logger.debug(message)
            self.events.on_next(ActionBlocked(action_event_id=event_id, blocked_by=occupant.id))

    @trace()
    def locate(self, x: int, y: int) -> Optional[Thing]:
        """Locate things in worlds by specified coordinates.

        Args:
            x: X-coordinate for locating things.
            y: Y-coordinate for locating things.

        Returns:
            An instance of `loudflow.realm.things.things.Thing`.
        """
        for thing in self.things.values():
            if thing.x == x and thing.y == y:
                return thing
        return None

    @trace()
    def find_by_name(self, name: str) -> Optional[Thing]:
        """Find things in worlds by name.

        Args:
            name: Name of things.

        Returns:
            An instance of `loudflow.realm.things.things.Thing`.
        """
        for thing in self.things.values():
            if thing.name == name:
                return thing
        return None

    @trace()
    @timer()
    def on_next(self, event: ActionEvent) -> None:
        """Handles actions events.

        Args:
            event: Action events.

        """
        if event.action.__class__.__name__ == "Move":
            self.move(event)
        else:
            message = "Invalid actions specified in actions events."
            logger.error(message)
            raise ValueError(message)


@dataclass(frozen=True)  # type: ignore
class WorldConfiguration:
    """World configuration class.

    Immutable dataclass containing worlds configuration data.

    Attributes:
    name: World name.
    width: Width of 2D worlds as number of tiles in horizontal direction.
    height: Height of 2D worlds as number of tiles in horizontal direction.

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
            An instance of `loudflow.realm.worlds.worlds.WorldConfiguration`.
        """
        pass

    @abstractmethod
    def copy(self, **attributes: Any) -> WorldConfiguration:
        """Copy WorldConfiguration state while replacing attributes with new values, and return new immutable instance.

        Args:
            **attributes: New configuration attributes.

        Returns:
            An instance of `loudflow.realm.worlds.worlds.WorldConfiguration`.
        """
        pass
