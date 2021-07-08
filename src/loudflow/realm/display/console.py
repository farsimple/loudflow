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
from pathlib import Path
from typing import Any, Dict, Optional

from loguru import logger
from pydispatch import dispatcher
import tcod

from loudflow.common.decorators import trace
from loudflow.realm.action.move import Move
from loudflow.realm.display.change import Change
from loudflow.realm.display.display import Display, DisplayConfiguration
from loudflow.realm.event.action_event import ActionEvent
from loudflow.realm.world.world import World


class Console(Display):
    """Console display class.

    The display in which the world and its occupants maty be viewed.

    Attributes:
        config: World configuration data.

    """

    @trace()
    def __init__(self, world: World, config: ConsoleConfiguration) -> None:
        logger.info("Constructing console...")
        super().__init__(world, config)
        path = Path(__file__).parent / config.tileset
        self.tileset = tcod.tileset.load_tilesheet(path, 32, 8, tcod.tileset.CHARMAP_TCOD)
        self.manual_agent = world.things.get(config.manual_agent, None)
        if self.manual_agent is None:
            message = "Thing [{}] cannot be found in world [{}].".format(config.manual_agent, world.id)
            logger.error(message)
            raise ValueError(message)
        self.context = tcod.context.new(
            columns=self.world.width,
            rows=self.world.height,
            tileset=self.tileset,
            title=self.world.name,
            vsync=True,
        )
        self.view = tcod.Console(self.world.width, self.world.height, order="F")
        self.view.print(x=self.manual_agent.x, y=self.manual_agent.y, string=self.manual_agent.symbol)

    @trace()
    def event_handler(self, event: tcod.event.T) -> None:
        """Handle display events.

        Args:
            event: Display event.

        """
        if event.type == "QUIT":
            self.context.close()
            raise SystemExit()
        if self.manual_agent is not None:
            if event.type == "KEYDOWN":
                key = event.sym
                if key == tcod.event.K_UP:
                    dispatcher.send(
                        signal=ActionEvent.__name__, event=ActionEvent(action=Move(self.manual_agent.id, None, 0, -1))
                    )
                elif key == tcod.event.K_DOWN:
                    dispatcher.send(
                        signal=ActionEvent.__name__, event=ActionEvent(action=Move(self.manual_agent.id, None, 0, 1))
                    )
                elif key == tcod.event.K_LEFT:
                    dispatcher.send(
                        signal=ActionEvent.__name__, event=ActionEvent(action=Move(self.manual_agent.id, None, -1, 0))
                    )
                elif key == tcod.event.K_RIGHT:
                    dispatcher.send(
                        signal=ActionEvent.__name__, event=ActionEvent(action=Move(self.manual_agent.id, None, 1, 0))
                    )
                elif key == tcod.event.K_ESCAPE:
                    pass

    @trace()
    def show(self) -> None:
        """Show world in the display."""
        self.context.present(self.view)
        while True:
            for event in tcod.event.wait():
                self.context.convert_event(event)
                self.event_handler(event)

    @trace()
    def update(self, change: Change) -> None:
        """Update display.

        Args:
            change: Change.

        """
        self.view.clear()
        thing = self.world.things.get(change.thing_id, None)
        if thing is not None:
            self.view.print(x=change.x, y=change.y, string=thing.symbol)
        else:
            message = "Display cannot be updated because thing [{}] cannot be found in world [{}].".format(
                change.thing_id, self.world.id
            )
            logger.warning(message)
        self.context.present(self.view)


@dataclass(frozen=True)
class ConsoleConfiguration(DisplayConfiguration):
    """Console configuration class.

    Immutable dataclass containing ConsoleConfiguration data.

    Attributes:
    tileset: Name of file containing tileset.
    manual_agent: True if display is user interactive, otherwise False.

    """

    tileset: str = "dejavu10x10_gs_tc.png"
    manual_agent: Optional[str] = None

    def __post_init__(self) -> None:
        if self.tileset is None:
            message = "Missing required attribute [tileset: str] in DisplayConfiguration."
            logger.error(message)
            raise ValueError(message)
        if not isinstance(self.tileset, str):
            message = "Invalid type for attribute [tileset: str] in DisplayConfiguration."
            logger.error(message)
            raise ValueError(message)
        if self.manual_agent is not None and not isinstance(self.manual_agent, str):
            message = "Invalid type for attribute [manual_agent: str] in DisplayConfiguration."
            logger.error(message)
            raise ValueError(message)

    @staticmethod
    @trace()
    def build(config: Dict) -> ConsoleConfiguration:
        """Build ConsoleConfiguration from dictionary of configuration data.

        Args:
            config: Dictionary containing configuration data.

        Returns:
            An instance of `loudflow.realm.display.console.ConsoleConfiguration`.
        """
        if config is None:
            message = "Missing required argument [config: Dict] in [ConsoleConfiguration.build] method call."
            logger.error(message)
            raise ValueError(message)
        if not isinstance(config, Dict):
            message = "Invalid argument type: [config: Dict] must be Dict in [ConsoleConfiguration.build] method call."
            logger.error(message)
            raise TypeError(message)
        # noinspection PyArgumentList
        # TODO: Remove noinspection after pycharm bug is fixed for incorrect unexpected argument warning for dataclasses
        return ConsoleConfiguration(tileset=config.get("tileset", None), manual_agent=config.get("manual_agent", None))

    @trace()
    def copy(self, **attributes: Any) -> ConsoleConfiguration:
        """
        Copy ConsoleConfiguration state while replacing attributes with new values, and return new immutable instance.

        Args:
            **attributes: New configuration attributes.

        Returns:
            An instance of `loudflow.realm.display.console.ConsoleConfiguration`.
        """
        tileset = attributes.get("tileset", None) if "tileset" in attributes.keys() else self.tileset
        manual_agent = (
            attributes.get("manual_agent", None) if "manual_agent" in attributes.keys() else self.manual_agent
        )
        # noinspection PyArgumentList
        # TODO: Remove noinspection after pycharm bug is fixed for incorrect unexpected argument warning for dataclasses
        return ConsoleConfiguration(tileset=tileset, manual_agent=manual_agent)
