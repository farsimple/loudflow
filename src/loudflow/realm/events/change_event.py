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

from loudflow.realm.changes.change import Change
from loudflow.realm.events.event import Event


@dataclass(frozen=True)
class ChangeEvent(Event):
    """Change event class.

    Immutable dataclass for change event.

    Attributes:
    change: Change.

    """

    change: Change

    def __post_init__(self) -> None:
        super().__post_init__()
        if self.change is None:
            message = "Missing required attribute [changes: Change] in ChangeEvent."
            logger.error(message)
            raise ValueError(message)
        if not isinstance(self.change, Change):
            message = "Invalid type for attribute [changes: Change] in ChangeEvent."
            logger.error(message)
            raise ValueError(message)


@dataclass(frozen=True)
class ChangeSucceeded(Event):
    """Change success event class.

    Immutable dataclass for change succeeded event.

    Attributes:
    change_event_id: Change event identifier.

    """

    change_event_id: str

    def __post_init__(self) -> None:
        super().__post_init__()
        if self.change_event_id is None:
            message = "Missing required attribute [change_event_id: str] in ChangeSucceeded."
            logger.error(message)
            raise ValueError(message)
        if not isinstance(self.change_event_id, str):
            message = "Invalid type for attribute [change_event_id: str] in ChangeSucceeded."
            logger.error(message)
            raise ValueError(message)


@dataclass(frozen=True)
class ChangeFailed(Event):
    """Change failed event class.

    Immutable dataclass for change failed event.

    Attributes:
    change_event_id: Change event identifier.

    """

    change_event_id: str

    def __post_init__(self) -> None:
        super().__post_init__()
        if self.change_event_id is None:
            message = "Missing required attribute [change_event_id: str] in ChangeFailed."
            logger.error(message)
            raise ValueError(message)
        if not isinstance(self.change_event_id, str):
            message = "Invalid type for attribute [change_event_id: str] in ChangeFailed."
            logger.error(message)
            raise ValueError(message)
