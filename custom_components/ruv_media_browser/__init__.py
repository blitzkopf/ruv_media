"""Custom integration to integrate ruv_media_browser with Home Assistant.

For more details about this integration, please refer to
https://github.com/blitzkopf/ruv_media_browser
"""
from __future__ import annotations
from typing import TYPE_CHECKING


from .coordinator import RUVMediaDataUpdateCoordinator
# from .const import DOMAIN
# from .api import RUVMediaBrowserApiClient
from .data import RUVMediaBrowserData

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import __version__

from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.loader import async_get_loaded_integration

from ruvmedia import RUVClient

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

    from .data import RUVMediaBrowserConfigEntry

PLATFORMS: list[Platform] = [
]


# https://developers.home-assistant.io/docs/config_entries_index/#setting-up-an-entry
async def async_setup_entry(
    hass: HomeAssistant, entry: RUVMediaBrowserConfigEntry
) -> bool:
    """Set up RÚV Media Browser from a config entry.

    This integration doesn't set up any entities, as it provides a media source
    only.
    """
    coordinator = RUVMediaDataUpdateCoordinator(
        hass=hass,
    )
    entry.runtime_data = RUVMediaBrowserData(
        client=RUVClient(session=async_get_clientsession(hass),
                         user_agent=f"HomeAssistant/{__version__}"),
        integration=async_get_loaded_integration(hass, entry.domain),
        coordinator=coordinator,
    )

    # https://developers.home-assistant.io/docs/integration_fetching_data#coordinated-single-api-poll-for-data-for-all-entities
    await coordinator.async_config_entry_first_refresh()

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    return True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: RUVMediaBrowserConfigEntry,
) -> bool:
    """Handle removal of an entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


async def async_reload_entry(
    hass: HomeAssistant,
    entry: RUVMediaBrowserConfigEntry,
) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
