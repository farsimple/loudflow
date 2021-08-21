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
from loudflow.realm.events.event import Event


@dataclass(frozen=True)
class ActionEvent(Event):
    """Action event class.

    Immutable dataclass for action event.

    Attributes:
    action: Action.

    """

    action: Action

    def __post_init__(self) -> None:
        super().__post_init__()
        if self.action is None:
            message = "Missing required attribute [action: Action] in ActionEvent."
            logger.error(message)
            raise ValueError(message)
        if not isinstance(self.action, Action):
            message = "Invalid type for attribute [action: Action] in ActionEvent."
            logger.error(message)
            raise ValueError(message)


@dataclass(frozen=True)
class ActionSucceeded(Event):
    """Action succeeded event class.

    Immutable dataclass for action succeeded event.

    Attributes:
    action_event_id: Action event identifier.

    """

    action_event_id: str

    def __post_init__(self) -> None:
        super().__post_init__()
        if self.action_event_id is None:
            message = "Missing required attribute [action_event_id: str] in ActionSucceeded."
            logger.error(message)
            raise ValueError(message)
        if not isinstance(self.action_event_id, str):
            message = "Invalid type for attribute [action_event_id: str] in ActionSucceeded."
            logger.error(message)
            raise ValueError(message)


@dataclass(frozen=True)
class ActionFailed(Event):
    """Action failed event class.

    Immutable dataclass for action failed event.

    Attributes:
    action_event_id: Source action event identifier.

    """

    action_event_id: str

    def __post_init__(self) -> None:
        super().__post_init__()
        if self.action_event_id is None:
            message = "Missing required attribute [action_event_id: str] in ActionFailed."
            logger.error(message)
            raise ValueError(message)
        if not isinstance(self.action_event_id, str):
            message = "Invalid type for attribute [action_event_id: str] in ActionFailed."
            logger.error(message)
            raise ValueError(message)


# noinspection PyDataclass
# TODO: Remove noinspection after pycharm bug is fixed for incorrect default argument warning for dataclasses
@dataclass(frozen=True)
class ActorDestroyed(ActionFailed):
    """Action failed due to actor destruction.

    Attributes:
    destroyed_by: Identifier of thing which destroyed actor.

    """

    destroyed_by: str

    def __post_init__(self) -> None:
        super().__post_init__()
        if self.destroyed_by is None:
            message = "Missing required attribute [destroyed_by: str] in ActorDestroyed."
            logger.error(message)
            raise ValueError(message)
        if not isinstance(self.destroyed_by, str):
            message = "Invalid type for attribute [destroyed_by: str] in ActorDestroyed."
            logger.error(message)
            raise ValueError(message)


# noinspection PyDataclass
# TODO: Remove noinspection after pycharm bug is fixed for incorrect default argument warning for dataclasses
@dataclass(frozen=True)
class ActionBlocked(ActionFailed):
    """Action failed due to blocking.

    Attributes:
    blocked_by: Identifier of thing which blocked action.

    """

    blocked_by: str

    def __post_init__(self) -> None:
        super().__post_init__()
        if self.blocked_by is None:
            message = "Missing required attribute [blocked_by: str] in ActionBlocked."
            logger.error(message)
            raise ValueError(message)
        if not isinstance(self.blocked_by, str):
            message = "Invalid type for attribute [blocked_by: str] in ActionBlocked."
            logger.error(message)
            raise ValueError(message)


# noinspection PyDataclass
# TODO: Remove noinspection after pycharm bug is fixed for incorrect default argument warning for dataclasses
@dataclass(frozen=True)
class ActionNotAllowed(ActionFailed):
    """Action failed because it is not allowed."""
