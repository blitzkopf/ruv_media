"""Expose RÚV Media Browser as a media source."""

from __future__ import annotations

# import mimetypes


from homeassistant.components.media_player import MediaClass, MediaType
# from homeassistant.components.media_source.error import Unresolvable
from homeassistant.components.media_source.models import (
    BrowseMediaSource,
    MediaSource,
    MediaSourceItem,
    PlayMedia,
)
from homeassistant.core import HomeAssistant

from . import RUVMediaBrowserConfigEntry
from .const import DOMAIN

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
    """Provide Radio stations as media sources."""

    name = "Radio Browser"

    def __init__(self, hass: HomeAssistant, entry: RUVMediaBrowserConfigEntry) -> None:
        """Initialize RUVMediaSource."""
        super().__init__(DOMAIN)
        self.hass = hass
        self.entry = entry

    # @property
    # def radios(self) -> RadioBrowser:
    #     """Return the radio browser."""
    #     return self.entry.runtime_data

    async def async_resolve_media(self, item: MediaSourceItem) -> PlayMedia:
        """Resolve selected Radio station to a streaming URL."""
        # radios = self.radios

        # station = await radios.station(uuid=item.identifier)
        # if not station:
        #     raise Unresolvable("Radio station is no longer available")

        # if not (mime_type := self._async_get_station_mime_type(station)):
        #     raise Unresolvable(
        #         "Could not determine stream type of radio station")

        # # Register "click" with Radio Browser
        # await radios.station_click(uuid=station.uuid)

        # return PlayMedia(station.url, mime_type)
        return PlayMedia("https://ruv-vod.akamaized.net/lokad/5389914T0/5389914T0.m3u8", "video/mpeg")

    async def async_browse_media(
        self,
        item: MediaSourceItem,
    ) -> BrowseMediaSource:
        """Return media."""
        # radios = self.radios
        return BrowseMediaSource(
            domain=DOMAIN,
            identifier="funny",
            media_class=MediaClass.CHANNEL,
            media_content_type=MediaType.MUSIC,
            title="Rúv shit",
            can_play=True,
            can_expand=False,
            thumbnail="https://myndir.ruv.is/eyJidWNrZXQiOiAicnV2LXByb2QtcnV2aXMtcHVibGljIiwgImtleSI6ICJtZWRpYS9wdWJsaWMvS3JpbmdsdW15bmRpci9wb3J0cmFpdF9wb3N0ZXJzLzZoZnBmZy1jZm92MC5qcGciLCAiZWRpdHMiOiB7InJlc2l6ZSI6IHsid2lkdGgiOiA1MDAsICJoZWlnaHQiOiA3NTB9fX0=",
        )

        # return BrowseMediaSource(
        #     domain=DOMAIN,
        #     identifier=None,
        #     media_class=MediaClass.CHANNEL,
        #     media_content_type=MediaType.MUSIC,
        #     title=self.entry.title,
        #     can_play=False,
        #     can_expand=True,
        #     children_media_class=MediaClass.DIRECTORY,
        #     children=[
        #         *await self._async_build_popular(radios, item),
        #         *await self._async_build_by_tag(radios, item),
        #         *await self._async_build_by_language(radios, item),
        #         *await self._async_build_by_country(radios, item),
        #     ],
        # )

    # @callback
    # @staticmethod
    # def _async_get_station_mime_type(station: Station) -> str | None:
    #     """Determine mime type of a radio station."""
    #     mime_type = CODEC_TO_MIMETYPE.get(station.codec)
    #     if not mime_type:
    #         mime_type, _ = mimetypes.guess_type(station.url)
    #     return mime_type
