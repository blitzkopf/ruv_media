# RÚV media browser

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

![Project Maintenance][maintenance-shield]

[![Discord][discord-shield]][discord]
[![Community Forum][forum-shield]][forum]

_Integration to play media from Icelandic National Broadcasting Service [RÚV][ruv_is]._

This integration is in no way affiliated with or endorsed by RÚV.
Everything here is reverse engineered from [www.ruv.is][ruv_is].

**This integration will set up the following platforms.**

Platform | Description
-- | --
`media_source` | Provide media to play in `media_player`.

## Installation via HACS
The preferred type of installation is via [HACS](https://hacs.xyz). This way, you'll get updates when there are new versions.

1. Add [https://github.com/blitzkopf/ruv_media_browser][ruv_media_browser] to HACS under: HACS → Integrations → 3 dots(top right) → Custom repositories.
1. Select RÚV Media Browser under HACS → Integrations, or search for it if it not on the front page.

## Manual Installation
This is the hard way, HACS above is easier, at least after you have HACS set up.

1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
1. If you do not have a `custom_components` directory (folder) there, you need to create it.
1. In the `custom_components` directory (folder) create a new folder called `ruv_media_browser`.
1. Download _all_ the files from the `custom_components/ruv_media_browser/` directory (folder) in this repository. Or get the zip file from the lates release.
1. Place the files you downloaded in the new directory (folder) you created.
1. Restart Home Assistant
1. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "RÚV media browser"

## No configuration is needed

## Using the integration
To use the integration you can either click on the Media icon on the player device you want to play on. or select  _Media/Efni_ in the main menu and then select the device you want to play on in bottom right, most media can also be played in the browser.

Not all `media_player` devices will be able to play/browse RÚV media, and sometimes you will need to add an extra `integration` for the same physical device. For example the Sony Bravia TV integration will not play arbitrary media, but the Chromecast integration on the same TV will.

### Using RÚV media in scripts and automations
It is easy to use the integration in automations.
Just add an action Media player &rarr; Play media &rarr; _select media player*_

and then: Pick media &rarr; RÚV media browser &rarr; Channel &rarr; RÚV
The yaml should look something like this
```yml
service: media_player.play_media
target:
  entity_id: media_player.blitztv
data:
  media_content_id: media-source://ruv_media_browser/channel.ruv
  media_content_type: video
metadata:
  title: RÚV
  thumbnail: null
  media_class: channel
  children_media_class: null
  navigateIds:
    - {}
    - media_content_type: app
      media_content_id: media-source://ruv_media_browser
    - media_content_type: video
      media_content_id: media-source://ruv_media_browser/channel
```
You can remove all the metadata it does not matter for running the action.

<!---->

## Contributions are welcome!

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)

***

[ruv_is]: https://www.ruv.is/
[ruv_media_browser]: https://github.com/blitzkopf/ruv_media_browser
[commits-shield]: https://img.shields.io/github/commit-activity/y/blitzkopf/ruv_media_browser.svg?style=for-the-badge
[commits]: https://github.com/blitzkopf/ruv_media_browser/commits/main
[discord]: https://discord.gg/Qa5fW2R
[discord-shield]: https://img.shields.io/discord/330944238910963714.svg?style=for-the-badge
[exampleimg]: example.png
[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg?style=for-the-badge
[forum]: https://community.home-assistant.io/
[license-shield]: https://img.shields.io/github/license/blitzkopf/ruv_media_browser.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-Yngvi%20Þór%20Sigurjónsson%20%40blitzkopf-blue.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/blitzkopf/ruv_media_browser.svg?style=for-the-badge
[releases]: https://github.com/blitzkopf/ruv_media_browser/releases
