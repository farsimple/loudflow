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

from dataclasses import dataclass, field
from typing import Any, Dict, Set, Tuple
from uuid import uuid4

from loguru import logger

from loudflow.common.decorators import trace


class Thing:
    """Thing class.

    Things populating the worlds.

    Attributes:
        config: Thing configuration data.

    """

    @trace()
    def __init__(self, config: ThingConfiguration) -> None:
        self.id = str(uuid4())
        self.kind = config.kind
        self.name = config.name
        self.x = config.x
        self.y = config.y
        self.char = config.char
        self.color = config.color
        self.can_move = config.can_move
        self.can_be_destroyed = config.can_be_destroyed
        self.can_destroy = config.can_destroy

    @trace()
    def is_destroyed_by(self, thing: Thing) -> bool:
        """Can thing be destroyed by thing?

        Args:
            thing: Target thing to destroy.

        Returns:
            True if thing can destroy target thing.
        """
        if thing is None:
            message = "Missing required argument [thing: Thing] in Thing.is_destroyed_by method."
            logger.error(message)
            raise ValueError(message)
        if not isinstance(thing, Thing):
            message = "Invalid type for argument [thing: Thing] in Thing.is_destroyed_by method."
            logger.error(message)
            raise ValueError(message)
        return self.can_be_destroyed and self.kind.lower() in {value.lower() for value in thing.can_destroy}

    @trace()
    def destroys(self, thing: Thing) -> bool:
        """Can thing destroy thing?

        Args:
            thing: Target thing to destroy.

        Returns:
            True if thing can destroy target thing.
        """
        if thing is None:
            message = "Missing required argument [thing: Thing] in Thing.destroys method."
            logger.error(message)
            raise ValueError(message)
        if not isinstance(thing, Thing):
            message = "Invalid type for argument [thing: Thing] in Thing.destroys method."
            logger.error(message)
            raise ValueError(message)
        return thing.can_be_destroyed and thing.kind.lower() in {value.lower() for value in self.can_destroy}

    @trace()
    def pushes(self, thing: Thing) -> bool:
        """Can self push thing?

        Args:
            thing: Thing to be pushed.

        Returns:
            True if thing can be pushed.
        """
        if thing is None:
            message = "Missing required argument [thing: Thing] in Thing.pushes method."
            logger.error(message)
            raise ValueError(message)
        if not isinstance(thing, Thing):
            message = "Invalid type for argument [thing: Thing] in Thing.pushes method."
            logger.error(message)
            raise ValueError(message)
        if not self.can_move:
            return False
        elif not thing.can_move:
            return False
        elif self.destroys(thing) or self.is_destroyed_by(thing):
            return False
        return True


@dataclass(frozen=True)
class ThingConfiguration:
    """Thing configuration class.

    Immutable dataclass containing things configuration data.

    Attributes:
    kind: Kind of things.
    name: Thing name.
    x: X-coordinate of initial location of things.
    y: Y-coordinate of initial location of things.
    char: Character representing things in console.
    color: Color of character representing things in console.
    can_move: True if things is capable of being moved.
    can_be_destroyed: True if things is capable of being destroyed.
    can_destroy: Set of things kinds which things is capable of destroying.

    """

    kind: str
    name: str
    x: int
    y: int
    char: str
    color: Tuple[int, int, int]
    can_move: bool = False
    can_be_destroyed: bool = False
    can_destroy: Set[str] = field(default_factory=lambda: set())

    def __post_init__(self) -> None:
        if self.kind is None:
            message = "Missing required attribute [kind: str] in ThingConfiguration."
            logger.error(message)
            raise ValueError(message)
        if not isinstance(self.kind, str):
            message = "Invalid type for attribute [kind: str] in ThingConfiguration."
            logger.error(message)
            raise ValueError(message)
        if self.name is None:
            message = "Missing required attribute [name: str] in ThingConfiguration."
            logger.error(message)
            raise ValueError(message)
        if not isinstance(self.name, str):
            message = "Invalid type for attribute [name: str] in ThingConfiguration."
            logger.error(message)
            raise ValueError(message)
        if self.x is None:
            message = "Missing required attribute [x: int] in ThingConfiguration."
            logger.error(message)
            raise ValueError(message)
        if not isinstance(self.x, int):
            message = "Invalid type for attribute [x: int] in ThingConfiguration."
            logger.error(message)
            raise ValueError(message)
        if self.y is None:
            message = "Missing required attribute [y: int] in ThingConfiguration."
            logger.error(message)
            raise ValueError(message)
        if not isinstance(self.y, int):
            message = "Invalid type for attribute [y: int] in ThingConfiguration."
            logger.error(message)
            raise ValueError(message)
        if self.char is None:
            message = "Missing required attribute [char: str] in ThingConfiguration."
            logger.error(message)
            raise ValueError(message)
        if not isinstance(self.char, str):
            message = "Invalid type for attribute [char: str] in ThingConfiguration."
            logger.error(message)
            raise ValueError(message)
        if len(self.char) > 1:
            message = "Invalid attribute [char: str] in ThingConfiguration. [char: str] must be a single character."
            logger.error(message)
            raise ValueError(message)
        if self.color is None:
            message = "Missing required attribute [color: Tuple[int, int, int]] in ThingConfiguration."
            logger.error(message)
            raise ValueError(message)
        if not isinstance(self.color, tuple):
            message = "Invalid type for attribute [color: Tuple[int, int, int]] in ThingConfiguration."
            logger.error(message)
            raise ValueError(message)
        if len(self.color) != 3:
            message = (
                "Invalid attribute [color: Tuple[int, int, int]] in ThingConfiguration. "
                "[color: Tuple[int,int, int]] must consist of three integers. "
            )
            logger.error(message)
            raise ValueError(message)
        if not all(isinstance(value, int) for value in self.color):
            message = (
                "Invalid attribute [color: Tuple[int, int, int]] in ThingConfiguration. "
                "[color: Tuple[int, int, int]] values must be integer."
            )
            logger.error(message)
            raise ValueError(message)
        if self.can_move is None:
            object.__setattr__(self, "can_move", False)
        if not isinstance(self.can_move, bool):
            message = "Invalid type for attribute [can_move: bool] in ThingConfiguration."
            logger.error(message)
            raise ValueError(message)
        if self.can_be_destroyed is None:
            object.__setattr__(self, "can_be_destroyed", False)
        if not isinstance(self.can_be_destroyed, bool):
            message = "Invalid type for attribute [can_be_destroyed: bool] in ThingConfiguration."
            logger.error(message)
            raise ValueError(message)
        if self.can_destroy is None:
            object.__setattr__(self, "can_destroy", {})
        if not isinstance(self.can_destroy, set):
            message = "Invalid type for attribute [can_destroy: set[str]] in ThingConfiguration."
            logger.error(message)
            raise ValueError(message)

    @staticmethod
    @trace()
    def build(config: Dict) -> ThingConfiguration:
        """Build ThingConfiguration from dictionary of configuration data.

        Args:
            config: Dictionary containing configuration data.

        Returns:
            An instance of `loudflow.realm.things.ThingConfiguration`.
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
            kind=config.get("kind", None),
            x=config.get("x", None),
            y=config.get("y", None),
            name=config.get("name", None),
            char=config.get("char", None),
            color=config.get("color", None),
            can_move=config.get("can_move", None),
            can_be_destroyed=config.get("can_be_destroyed", None),
            can_destroy=config.get("can_destroy", {}),
        )

    @trace()
    def copy(self, **attributes: Any) -> ThingConfiguration:
        """Copy ThingConfiguration state while replacing attributes with new values, and return new immutable instance.

        Args:
            **attributes: New ThingConfiguration attributes.

        Returns:
            An instance of `loudflow.realm.things.ThingConfiguration`.
        """
        kind = attributes.get("kind", None) if "kind" in attributes.keys() else self.kind
        name = attributes.get("name", None) if "name" in attributes.keys() else self.name
        x = attributes.get("x", None) if "x" in attributes.keys() else self.x
        y = attributes.get("y", None) if "y" in attributes.keys() else self.y
        char = attributes.get("char", None) if "char" in attributes.keys() else self.char
        color = attributes.get("color", None) if "color" in attributes.keys() else self.color
        can_move = attributes.get("can_move", None) if "can_move" in attributes.keys() else self.can_move
        can_be_destroyed = (
            attributes.get("can_be_destroyed", None)
            if "can_be_destroyed" in attributes.keys()
            else self.can_be_destroyed
        )
        can_destroy = attributes.get("can_destroy", None) if "can_destroy" in attributes.keys() else self.can_destroy
        # noinspection PyArgumentList
        # TODO: Remove noinspection after pycharm bug is fixed for incorrect unexpected argument warning for dataclasses
        return ThingConfiguration(
            kind=kind,
            name=name,
            x=x,
            y=y,
            char=char,
            color=color,
            can_move=can_move,
            can_be_destroyed=can_be_destroyed,
            can_destroy=can_destroy,
        )
