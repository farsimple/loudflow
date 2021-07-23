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

from loudflow.realm.world.world import WorldConfiguration


@dataclass(frozen=True)
class DummyWorldConfiguration(WorldConfiguration):
    def __post_init__(self) -> None:
        super().__post_init__()

    @staticmethod
    def build(config: Dict) -> DummyWorldConfiguration:
        # noinspection PyArgumentList
        # TODO: Remove noinspection after pycharm bug is fixed for incorrect unexpected argument warning for dataclasses
        return DummyWorldConfiguration(name="test", width=80, height=50)

    def copy(self, **attributes: Any) -> DummyWorldConfiguration:
        # noinspection PyArgumentList
        # TODO: Remove noinspection after pycharm bug is fixed for incorrect unexpected argument warning for dataclasses
        return DummyWorldConfiguration(name="test", width=80, height=50)


def test_constructor() -> None:
    name = "test"
    # noinspection PyArgumentList
    # TODO: Remove noinspection after pycharm bug is fixed for incorrect unexpected argument warning for dataclasses
    config = DummyWorldConfiguration(name="test", width=80, height=50)
    assert config.name == name
