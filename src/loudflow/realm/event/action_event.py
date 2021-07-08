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
from typing import Any

from loguru import logger

from loudflow.common.decorators import trace

# from loudflow.realm.action.action import Action
from loudflow.realm.event.event import Event


@dataclass(frozen=True)
class ActionEvent(Event):
    """Action event class.

    Immutable dataclass for action event.

    Attributes:
    action: Action.

    """

    action: Any

    def __post_init__(self) -> None:
        super().__post_init__()
        if self.action is None:
            message = "Missing required attribute [action: Action] in ActionEvent."
            logger.error(message)
            raise ValueError(message)
        # if not isinstance(self.action, Action):
        #     message = "Invalid type for attribute [action: Action] in ActionEvent."
        #     logger.error(message)
        #     raise ValueError(message)

    @trace()
    def copy(self, **attributes: Any) -> ActionEvent:
        """Copy Action event state while replacing attributes with new values, and return new immutable instance.

        Args:
            **attributes: New action event attributes.

        Returns:
            An instance of :py:class:`loudflow.realm.event.action_event.ActionEvent`.
        """
        action = attributes.get("action", None) if "action" in attributes.keys() else self.action
        # noinspection PyArgumentList
        # TODO: Remove noinspection after pycharm bug is fixed for incorrect unexpected argument warning for dataclasses
        return ActionEvent(action=action)


@dataclass(frozen=True)
class ActionDoneEvent(Event):
    """Action done event class.

    Immutable dataclass for action done event.

    Attributes:
    source_id: Source action event identifier.

    """

    source_id: str

    def __post_init__(self) -> None:
        super().__post_init__()
        if self.source_id is None:
            message = "Missing required attribute [source_id: str] in ActionDoneEvent."
            logger.error(message)
            raise ValueError(message)
        if not isinstance(self.source_id, str):
            message = "Invalid type for attribute [source_id: str] in ActionDoneEvent."
            logger.error(message)
            raise ValueError(message)

    @trace()
    def copy(self, **attributes: Any) -> ActionDoneEvent:
        """Copy ActionDone event state while replacing attributes with new values, and return new immutable instance.

        Args:
            **attributes: New action done event attributes.

        Returns:
            An instance of :py:class:`loudflow.realm.event.action_event.ActionDoneEvent`.
        """
        source_id = attributes.get("source_id", None) if "source_id" in attributes.keys() else self.source_id
        # noinspection PyArgumentList
        # TODO: Remove noinspection after pycharm bug is fixed for incorrect unexpected argument warning for dataclasses
        return ActionDoneEvent(source_id=source_id)


@dataclass(frozen=True)
class ActionFailedEvent(Event):
    """Action failed event class.

    Immutable dataclass for action failed event.

    Attributes:
    source_id: Source action event identifier.

    """

    source_id: str

    def __post_init__(self) -> None:
        super().__post_init__()
        if self.source_id is None:
            message = "Missing required attribute [source_id: str] in ActionFailedEvent."
            logger.error(message)
            raise ValueError(message)
        if not isinstance(self.source_id, str):
            message = "Invalid type for attribute [source_id: str] in ActionFailedEvent."
            logger.error(message)
            raise ValueError(message)

    @trace()
    def copy(self, **attributes: Any) -> ActionFailedEvent:
        """Copy ActionFailed event state while replacing attributes with new values, and return new immutable instance.

        Args:
            **attributes: New action failed event attributes.

        Returns:
            An instance of :py:class:`loudflow.realm.event.action_event.ActionFailedEvent`.
        """
        source_id = attributes.get("source_id", None) if "source_id" in attributes.keys() else self.source_id
        # noinspection PyArgumentList
        # TODO: Remove noinspection after pycharm bug is fixed for incorrect unexpected argument warning for dataclasses
        return ActionFailedEvent(source_id=source_id)
