"""Custom types for integration_blueprint."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING
from ruvmedia import RUVClient

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.loader import Integration

    from .coordinator import RUVMediaDataUpdateCoordinator


type RUVMediaBrowserConfigEntry = ConfigEntry[RUVMediaBrowserData]


@dataclass
class RUVMediaBrowserData:
    """Data for the RÚV Media Browser integration."""

    coordinator: RUVMediaDataUpdateCoordinator
    integration: Integration
    client: RUVClient
