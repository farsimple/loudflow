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

from dataclasses import dataclass
from typing import Any, Dict, TypeVar

import tcod

World = TypeVar("World")
Change = TypeVar("Change")

class Console:
    def __init__(self, world: World, config: ConsoleConfiguration) -> None:
        self.id = ...
        self.world = ...
        self.config = ...
        self.tileset = ...
        self.player = ...
        self.context = ...
        self.view = ...
        ...
    def event_handler(self, event: tcod.event.T) -> None: ...
    def show(self) -> None: ...
    def update(self, change: Change) -> None: ...
    def _render(self) -> None: ...

@dataclass(frozen=True)
class ConsoleConfiguration:
    tileset: str = ...
    player: str = ...
    @staticmethod
    def build(config: Dict) -> ConsoleConfiguration: ...
    def copy(self, **attributes: Any) -> ConsoleConfiguration: ...
