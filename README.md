# ovos-PHAL-plugin-gpsd

A [PHAL](https://github.com/OpenVoiceOS/ovos-PHAL) plugin that reads location data from [gpsd](https://gpsd.io/). It connects to a running gpsd daemon and smooths the reported coordinates. It then updates the OpenVoiceOS user configuration with the current location, timezone, and city.

## Install

```bash
pip install ovos-PHAL-plugin-gpsd
```

The plugin needs a running gpsd daemon that has access to a GPS device. It connects to gpsd at `127.0.0.1:2947` by default.

## Usage

PHAL loads the plugin by its entry point, `ovos-phal-plugin-gpsd`. No manual setup is needed beyond installing the package and having gpsd running.

The plugin polls gpsd for `TPV` (time-position-velocity) reports. It keeps a rolling average of the last 15 points to smooth the latitude, longitude, speed, and altitude. It rounds the result to a configurable number of decimal places (`decimal_places`, default `3`).

When the smoothed coordinates change, the plugin does this:

- looks up the timezone for the coordinates with [timezonefinder](https://github.com/jannikmi/timezonefinder)
- reverse-geocodes the coordinates to a city, region, and country with [reverse_geocoder](https://github.com/thampiman/reverse-geocoder)
- writes the location, timezone, and city into the user configuration
- emits `configuration.updated` and `configuration.patch` on the OVOS message bus

## Related projects

- [OpenVoiceOS/ovos-PHAL](https://github.com/OpenVoiceOS/ovos-PHAL): the PHAL framework this plugin runs under
- [OpenVoiceOS/ovos-PHAL-plugin-ipgeo](https://github.com/OpenVoiceOS/ovos-PHAL-plugin-ipgeo): a PHAL plugin that resolves location from an IP address instead of a GPS device

## License

Apache-2.0. See [LICENSE](LICENSE).
