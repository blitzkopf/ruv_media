"""DataUpdateCoordinator for ruv_media_browser."""
from __future__ import annotations

from datetime import timedelta
from typing import TYPE_CHECKING


from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

# from .api import (
#     RUVMediaBrowserApiClient,
#     RUVMediaBrowserApiClientAuthenticationError,
#     RUVMediaBrowserApiClientError,
# )
from .const import DOMAIN, LOGGER
if TYPE_CHECKING:

    from .data import RUVMediaBrowserConfigEntry


# https://developers.home-assistant.io/docs/integration_fetching_data#coordinated-single-api-poll-for-data-for-all-entities
class RUVMediaDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""

    config_entry: RUVMediaBrowserConfigEntry

    def __init__(
        self,
        hass: HomeAssistant,
        # ruv_client: RUVMediaBrowserApiClient,
    ) -> None:
        """Initialize."""
        # self.client = ruv_client
        super().__init__(
            hass=hass,
            logger=LOGGER,
            name=DOMAIN,
            update_interval=timedelta(minutes=5),
        )

    async def _async_update_data(self):
        """Update data via library."""
        try:
            return await self.config_entry.runtime_data.client.async_get_data()
        except Exception as exception:
            raise UpdateFailed(exception) from exception
#        except RUVMediaBrowserApiClientError as exception:
#            raise UpdateFailed(exception) from exception
