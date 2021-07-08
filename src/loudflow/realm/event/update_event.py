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
from loudflow.realm.display.change import Change
from loudflow.realm.event.event import Event


@dataclass(frozen=True)
class UpdateEvent(Event):
    """Update event class.

    Immutable dataclass for update event.

    Attributes:
    change: Change.

    """

    change: Change

    def __post_init__(self) -> None:
        super().__post_init__()
        if self.change is None:
            message = "Missing required attribute [change: Change] in UpdateEvent."
            logger.error(message)
            raise ValueError(message)
        if not isinstance(self.change, Change):
            message = "Invalid type for attribute [change: Change] in UpdateEvent."
            logger.error(message)
            raise ValueError(message)

    @trace()
    def copy(self, **attributes: Any) -> UpdateEvent:
        """Copy UpdateEvent state while replacing attributes with new values, and return new immutable instance.

        Args:
            **attributes: New UpdateEvent attributes.

        Returns:
            An instance of `loudflow.realm.event.update_event.UpdateEvent`.
        """
        change = attributes.get("change", None) if "change" in attributes.keys() else self.change
        # noinspection PyArgumentList
        # TODO: Remove noinspection after pycharm bug is fixed for incorrect unexpected argument warning for dataclasses
        return UpdateEvent(change=change)


@dataclass(frozen=True)
class UpdateDoneEvent(Event):
    """Update done event class.

    Immutable dataclass for update done event.

    Attributes:
    source_id: Source update event identifier.

    """

    source_id: str

    def __post_init__(self) -> None:
        super().__post_init__()
        if self.source_id is None:
            message = "Missing required attribute [source_id: str] in UpdateDoneEvent."
            logger.error(message)
            raise ValueError(message)
        if not isinstance(self.source_id, str):
            message = "Invalid type for attribute [source_id: str] in UpdateDoneEvent."
            logger.error(message)
            raise ValueError(message)

    @trace()
    def copy(self, **attributes: Any) -> UpdateDoneEvent:
        """Copy ActionDone event state while replacing attributes with new values, and return new immutable instance.

        Args:
            **attributes: New action done event attributes.

        Returns:
            An instance of `loudflow.realm.event.update_event.UpdateDoneEvent`.
        """
        source_id = attributes.get("source_id", None) if "source_id" in attributes.keys() else self.source_id
        # noinspection PyArgumentList
        # TODO: Remove noinspection after pycharm bug is fixed for incorrect unexpected argument warning for dataclasses
        return UpdateDoneEvent(source_id=source_id)


@dataclass(frozen=True)
class UpdateFailedEvent(Event):
    """Update failed event class.

    Immutable dataclass for update failed event.

    Attributes:
    source_id: Source update event identifier.

    """

    source_id: str

    def __post_init__(self) -> None:
        super().__post_init__()
        if self.source_id is None:
            message = "Missing required attribute [source_id: str] in UpdateFailedEvent."
            logger.error(message)
            raise ValueError(message)
        if not isinstance(self.source_id, str):
            message = "Invalid type for attribute [source_id: str] in UpdateFailedEvent."
            logger.error(message)
            raise ValueError(message)

    @trace()
    def copy(self, **attributes: Any) -> UpdateFailedEvent:
        """Copy ActionFailed event state while replacing attributes with new values, and return new immutable instance.

        Args:
            **attributes: New action failed event attributes.

        Returns:
            An instance of `loudflow.realm.event.update_event.UpdateFailedEvent`.
        """
        source_id = attributes.get("source_id", None) if "source_id" in attributes.keys() else self.source_id
        # noinspection PyArgumentList
        # TODO: Remove noinspection after pycharm bug is fixed for incorrect unexpected argument warning for dataclasses
        return UpdateFailedEvent(source_id=source_id)
