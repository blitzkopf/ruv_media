"""Expose RÚV Media Browser as a media source."""

from __future__ import annotations

# import mimetypes

from ruvmedia import RUVClient

from homeassistant.components.media_player import MediaClass, MediaType
from homeassistant.components.media_source.error import Unresolvable
from homeassistant.components.media_source.models import (
    BrowseMediaSource,
    MediaSource,
    MediaSourceItem,
    PlayMedia,
)
from homeassistant.core import HomeAssistant

from .data import RUVMediaBrowserConfigEntry
from .const import DOMAIN, LOGGER

CODEC_TO_MIMETYPE = {
    "MP3": "audio/mpeg",
    "AAC": "audio/aac",
    "AAC+": "audio/aac",
    "OGG": "application/ogg",
}


async def async_get_media_source(hass: HomeAssistant) -> RUVMediaSource:
    """Set up RÚV Media Browser media source."""
    # RÚV Media browser supports only a single config entry
    entry = hass.config_entries.async_entries(DOMAIN)[0]

    return RUVMediaSource(hass, entry)


class RUVMediaSource(MediaSource):
    """Provide RÚV Live channels and media as media sources."""

    name = "RÚV Media Browser"

    def __init__(self, hass: HomeAssistant, entry: RUVMediaBrowserConfigEntry) -> None:
        """Initialize RUVMediaSource."""
        super().__init__(DOMAIN)
        self.hass = hass
        self.entry = entry

    @property
    def ruv_client(self) -> RUVClient:
        """Return the radio browser."""
        return self.entry.runtime_data.client

    async def async_resolve_media(self, item: MediaSourceItem) -> PlayMedia:
        """Resolve selected Radio station to a streaming URL."""
        client = self.ruv_client
        LOGGER.debug("Resolving media for %s", item)

        media = await client.media(item.identifier)
        if not media:
            raise Unresolvable("Media is no longer available")

        # if not (mime_type := self._async_get_station_mime_type(station)):
        #     raise Unresolvable(
        #         "Could not determine stream type of radio station")

        # # Register "click" with Radio Browser
        # await radios.station_click(uuid=station.uuid)
        LOGGER.debug("Playing media  %s ", media.url)

        return PlayMedia(media.url, "application/x-mpegURL")
        # return PlayMedia("https://ruv-vod.akamaized.net/lokad/5389914T0/5389914T0.m3u8", "video/mpeg")

    async def async_browse_media(
        self,
        item: MediaSourceItem,
    ) -> BrowseMediaSource:
        """Return media."""
        ruv_client = self.ruv_client
        LOGGER.debug("Browsing media for %s", item)
        if item.identifier:

            if item.identifier.startswith("channel"):
                return await self._async_build_live(ruv_client, item)
            if item.identifier.startswith("category"):
                return await self._async_build_categories(ruv_client, item)
            if item.identifier.startswith("program"):
                return await self._async_build_programs(ruv_client, item)

        return BrowseMediaSource(
            domain=DOMAIN,
            identifier=None,
            media_class=MediaClass.CHANNEL,
            media_content_type=MediaType.MUSIC,
            title=self.entry.title,
            can_play=False,
            can_expand=True,
            children_media_class=MediaClass.CHANNEL,
            children=[
                await self._async_build_live(ruv_client, item),
                await self._async_build_categories(ruv_client, item),

                # *await self._async_build_popular(radios, item),
                # *await self._async_build_by_tag(radios, item),
                # *await self._async_build_by_language(radios, item),
                # *await self._async_build_by_country(radios, item),
            ],
        )

    # @callback
    # @staticmethod
    # def _async_get_station_mime_type(station: Station) -> str | None:
    #     """Determine mime type of a radio station."""
    #     mime_type = CODEC_TO_MIMETYPE.get(station.codec)
    #     if not mime_type:
    #         mime_type, _ = mimetypes.guess_type(station.url)
    #     return mime_type

    async def _async_build_live(
        self, ruv_client: RUVClient, item: MediaSourceItem
    ) -> BrowseMediaSource:
        """Handle browsing live channels."""

        if item.identifier:
            channels = await ruv_client.async_get_live_channels()
            children = [
                BrowseMediaSource(
                    domain=DOMAIN,
                    identifier=f"{channel.identifier}",
                    media_class=MediaClass.CHANNEL,
                    media_content_type=MediaType.VIDEO,
                    title=channel.name,
                    can_play=True,
                    can_expand=False,
                    # thumbnail=channel.favicon,
                )
                for channel in channels
            ]
        else:
            children = None

        return BrowseMediaSource(
            domain=DOMAIN,
            identifier=f"channel",
            media_class=MediaClass.DIRECTORY,
            media_content_type=MediaType.VIDEO,
            title="Live Channels",
            can_play=False,
            can_expand=True,
            children_media_class=MediaClass.CHANNEL,
            children=children,
            # thumbnail=channel.favicon,
        )

    async def _async_build_categories(
        self, ruv_client: RUVClient, item: MediaSourceItem
    ) -> BrowseMediaSource:
        """Handle browsing categories."""

        if item.identifier:
            prefix, _, category = (item.identifier or "").partition(".")
            LOGGER.debug("Category: %s", category)
            categories = await ruv_client.async_get_categories(category)
            children = [
                BrowseMediaSource(
                    domain=DOMAIN,
                    identifier=f"{category.identifier}",
                    media_class=MediaClass.CHANNEL,
                    media_content_type=MediaType.VIDEO,
                    title=category.name,
                    can_play=False,
                    can_expand=True,
                    # thumbnail=channel.favicon,
                )
                for category in categories
            ]
        else:
            children = None

        return BrowseMediaSource(
            domain=DOMAIN,
            identifier=f"category",
            media_class=MediaClass.DIRECTORY,
            media_content_type=MediaType.VIDEO,
            title="Categories",
            can_play=False,
            can_expand=True,
            children_media_class=MediaClass.CHANNEL,
            children=children,
            # thumbnail=channel.favicon,
        )

    async def _async_build_programs(
        self, ruv_client: RUVClient, item: MediaSourceItem
    ) -> BrowseMediaSource:
        """Handle browsing categories."""

        if item.identifier:
            prefix, _, program = (item.identifier or "").partition(".")
            LOGGER.debug("Program: %s", program)
            episodes = await ruv_client.async_get_programs(program)
            children = [
                BrowseMediaSource(
                    domain=DOMAIN,
                    identifier=f"{episode.identifier}",
                    media_class=MediaClass.CHANNEL,
                    media_content_type=MediaType.VIDEO,
                    title=episode.name,
                    can_play=True,
                    can_expand=False,
                    # thumbnail=channel.favicon,
                )
                for episode in episodes
            ]
        else:
            children = None

        return BrowseMediaSource(
            domain=DOMAIN,
            identifier=item.identifier,
            media_class=MediaClass.DIRECTORY,
            media_content_type=MediaType.VIDEO,
            title="Episodes",
            can_play=False,
            can_expand=True,
            children_media_class=MediaClass.CHANNEL,
            children=children,
            # thumbnail=channel.favicon,
        )
