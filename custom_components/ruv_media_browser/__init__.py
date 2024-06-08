"""Custom integration to integrate ruv_media_browser with Home Assistant.

For more details about this integration, please refer to
https://github.com/blitzkopf/ruv_media_browser
"""
from __future__ import annotations
from .coordinator import RUVMediaDataUpdateCoordinator
from .const import DOMAIN
from .api import RUVMediaBrowserApiClient

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME, Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

type RUVMediaBrowserConfigEntry = ConfigEntry[{}]


PLATFORMS: list[Platform] = [
    Platform.SENSOR,
    Platform.BINARY_SENSOR,
    Platform.SWITCH,
]


# https://developers.home-assistant.io/docs/config_entries_index/#setting-up-an-entry
async def async_setup_entry(
    hass: HomeAssistant, entry: RUVMediaBrowserConfigEntry
) -> bool:
    """Set up RÚV Media Browser from a config entry.

    This integration doesn't set up any entities, as it provides a media source
    only.
    """
    # session = async_get_clientsession(hass)
    # radios = RadioBrowser(
    #     session=session, user_agent=f"HomeAssistant/{__version__}")

    # try:
    #     await radios.stats()
    # except (DNSError, RadioBrowserError) as err:
    #     raise ConfigEntryNotReady(
    #         "Could not connect to Radio Browser API") from err

    # entry.runtime_data = radios
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return True
