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
from random import randint
from typing import Any, Dict, Optional, Tuple

from loguru import logger
from rx.core.typing import Disposable

from loudflow.common.decorators import trace
from loudflow.realm.thing.thing import Thing, ThingConfiguration
from loudflow.realm.world.world import World, WorldConfiguration


class TileWorld(World):
    """TileWorld class.

    Tile world.

    Attributes:
        config: World configuration data.

    """

    @trace()
    def __init__(self, config: TileWorldConfiguration) -> None:
        logger.info("Constructing tileworld...")
        super().__init__(config)
        player_config = ThingConfiguration("player", "@", (255, 255, 255), int(self.width / 2), int(self.height / 2))
        self.player = Thing(player_config)
        self.add(self.player)
        cell_count = self.width * self.height
        obstacle_count = int(self.config.obstacles * cell_count)
        hole_count = int(self.config.holes * cell_count)
        tile_count = hole_count
        count = obstacle_count
        while count > 0:
            if self._add_random("obstacle", "#", (255, 0, 0)):
                count -= 1
        count = hole_count
        while count > 0:
            if self._add_random("hole", "O", (0, 255, 0)):
                count -= 1
        count = tile_count
        while count > 0:
            if self._add_random("tile", "*", (0, 0, 255)) is not None:
                count -= 1

    @trace()
    def start(self) -> None:
        logger.info("Starting world...")
        self.subscription = self.actions.subscribe(self)

    @trace()
    def stop(self) -> None:
        logger.info("Stopping world...")
        if self.subscription is not None and isinstance(self.subscription, Disposable):
            self.subscription.dispose()

    @trace()
    def destroy(self) -> None:
        logger.info("Destroying world...")
        self.things: Dict[str, Thing] = {}

    @trace()
    def _add_random(self, name: str, char: str, color: Tuple[int, int, int]) -> Thing:
        """Add thing at random location in world.

        Args:
            name: Thing name.
            char: Ascii symbol for thing.

        Returns:
            An instance of `loudflow.realm.thing.thing.Thing`.
        """
        x = randint(0, self.width - 1)
        y = randint(0, self.height - 1)
        thing_config = ThingConfiguration(name, char, color, x, y)
        thing = Thing(thing_config)
        self.add(thing, replace=False, silent=True)
        return thing


@dataclass(frozen=True)
class TileWorldConfiguration(WorldConfiguration):
    """TileWorld configuration class.

    Immutable dataclass containing TileWorldConfiguration data.

    Attributes:
    obstacles: Ratio of obstacles in the world.
    holes: Ratio of holes in the world.

    """

    obstacles: Optional[float]
    holes: Optional[float]

    def __post_init__(self) -> None:
        super().__post_init__()
        if self.obstacles is None:
            object.__setattr__(self, "width", 0.01)
        if not isinstance(self.obstacles, float):
            message = "Invalid type for attribute [obstacles: float] in TileWorldConfiguration."
            logger.error(message)
            raise ValueError(message)
        if self.holes is None:
            object.__setattr__(self, "width", 0.001)
        if not isinstance(self.holes, float):
            message = "Invalid type for attribute [holes: float] in TileWorldConfiguration."
            logger.error(message)
            raise ValueError(message)

    @staticmethod
    @trace()
    def build(config: Dict) -> TileWorldConfiguration:
        """Build TileWorldConfiguration from dictionary of configuration data.

        Args:
            config: Dictionary containing configuration data.

        Returns:
            An instance of `loudflow.realm.world.tile_world.TileWorldConfiguration`.
        """
        if config is None:
            message = "Missing required argument [config: Dict] in [WorldConfiguration.build] method call."
            logger.error(message)
            raise ValueError(message)
        if not isinstance(config, Dict):
            message = "Invalid argument type: [config: Dict] must be Dict in [WorldConfiguration.build] method call."
            logger.error(message)
            raise TypeError(message)
        # noinspection PyArgumentList
        # TODO: Remove noinspection after pycharm bug is fixed for incorrect unexpected argument warning for dataclasses
        return TileWorldConfiguration(
            name=config.get("name", None),
            width=config.get("width", None),
            height=config.get("height", None),
            obstacles=config.get("obstacles", None),
            holes=config.get("holes", None),
        )  # type: ignore

    @trace()
    def copy(self, **attributes: Any) -> TileWorldConfiguration:
        """Copy TileWorldConfiguration state while replacing attributes with new values,
        and return new immutable instance.

        Args:
            **attributes: New configuration attributes.

        Returns:
            An instance of `loudflow.realm.world.tile_world.TileWorldConfiguration`.
        """
        name = attributes.get("name", None) if "name" in attributes.keys() else self.name
        width = attributes.get("width", None) if "width" in attributes.keys() else self.width
        height = attributes.get("height", None) if "height" in attributes.keys() else self.height
        obstacles = attributes.get("obstacles", None) if "obstacles" in attributes.keys() else self.obstacles
        holes = attributes.get("holes", None) if "holes" in attributes.keys() else self.holes
        # noinspection PyArgumentList
        # TODO: Remove noinspection after pycharm bug is fixed for incorrect unexpected argument warning for dataclasses
        return TileWorldConfiguration(
            name=name, width=width, height=height, obstacles=obstacles, holes=holes
        )  # type: ignore
