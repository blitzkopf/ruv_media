"""Adds config flow for RÚV Media Browser."""
from __future__ import annotations

from typing import Any

from homeassistant import config_entries
# from homeassistant.helpers.aiohttp_client import async_create_clientsession

# from .api import (
#     RUVMediaBrowserApiClient,
#     RUVMediaBrowserApiClientAuthenticationError,
#     RUVMediaBrowserApiClientCommunicationError,
#     RUVMediaBrowserApiClientError,
# )
from .const import DOMAIN


class RUVMediaBrowserFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for RÚV Media Browser."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.ConfigFlowResult:
        """Handle the initial step."""
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        if user_input is not None:
            return self.async_create_entry(title="RÚV Media Browser", data={})

        return self.async_show_form(step_id="user")

    async def async_step_onboarding(
        self, data: dict[str, Any] | None = None
    ) -> config_entries.ConfigFlowResult:
        """Handle a flow initialized by onboarding."""
        return self.async_create_entry(title="RÚV Media Browser", data={})
