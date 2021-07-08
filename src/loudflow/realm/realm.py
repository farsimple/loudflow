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

from typing import Any

from loguru import logger
from pydispatch import dispatcher

from loudflow.common.decorators import timer, trace
from loudflow.realm.display.console import Console, ConsoleConfiguration
from loudflow.realm.event.update_event import UpdateEvent
from loudflow.realm.thing.thing import Thing, ThingConfiguration
from loudflow.realm.world.world import World, WorldConfiguration


class Realm:
    """Realm class.

    The realm in which the agent(s) act.

    Attributes:
        config: World configuration data.

    """

    @trace()
    def __init__(self, config: WorldConfiguration) -> None:
        logger.info("Constructing realm...")
        self.config = config
        self.world = World(config)
        logger.info(self.world.width)
        thing_config = ThingConfiguration("thingy", "A", int(self.world.width / 2), int(self.world.height / 2))
        thing = Thing(thing_config)
        self.world.add(thing)
        display_config = ConsoleConfiguration(manual_agent=thing.id)
        self.display = Console(self.world, display_config)
        dispatcher.connect(self.update_handler, signal=UpdateEvent.__name__, sender=dispatcher.Any)

    @trace()
    def run(self) -> None:
        self.display.show()

    @trace()
    @timer()
    def update_handler(self, signal: Any, sender: Any, event: UpdateEvent) -> None:
        """Handles update events.

        Args:
            signal: Event signal.
            sender: Event sender.
            event: Update event.

        """
        self.display.update(event.change)
