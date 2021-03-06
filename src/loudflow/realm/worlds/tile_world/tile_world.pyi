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
from typing import Any, Dict, Optional, TypeVar

ActionEvent = TypeVar("ActionEvent")
Thing = TypeVar("Thing")

class TileWorld:
    def __init__(self, config: TileWorldConfiguration) -> None:
        self.id = ...
        self.config = ...
        self.name = ...
        self.width = ...
        self.height = ...
        self.things = ...
        self.agent = ...
        ...
    def add(self, thing: Thing, replace: bool = True, silent: bool = True) -> bool: ...
    def remove(self, thing_id: str) -> None: ...
    def move(self, thing_id: str, x: int, y: int) -> None: ...
    def on_next(self, event: ActionEvent) -> None: ...
    def _random_name(self, kind: str) -> str: ...

@dataclass(frozen=True)
class TileWorldConfiguration:
    name: str
    width: Optional[int]
    height: Optional[int]
    obstacles: Optional[float]
    holes: Optional[float]
    def __post_init__(self) -> None: ...
    @staticmethod
    def build(config: Dict) -> TileWorldConfiguration: ...
    def copy(self, **attributes: Any) -> TileWorldConfiguration: ...
