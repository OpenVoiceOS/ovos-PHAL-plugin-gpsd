import threading

import reverse_geocoder
from gpsdclient import GPSDClient
from ovos_utils.log import LOG
from timezonefinder import TimezoneFinder

from ovos_plugin_manager.phal import PHALPlugin


class GPSDPlugin(PHALPlugin):
    def __init__(self, bus=None):
        super().__init__(bus, 'ovos-phal-plugin-gpsd')
        self.config = {}
        places = self.config.get("decimal_places", 3)
        self.location = {}
        self.tf = TimezoneFinder()
        self.gps = GPSDaemon(decimal_places=places)
        self.gps.on_location_update = self.on_location_update
        self.gps.start()

    def get_tz(self, lat, lon):
        try:
            tz = self.tf.timezone_at(lat=lat, lng=lon)
            return {"code": tz, "name": tz}
        except:
            return {}

    @staticmethod
    def reverse_geocode(lat, lon):
        try:
            geocode = reverse_geocoder.search((lat, lon))[0]
            return {
                "code": geocode["admin2"],
                "name": geocode["name"],
                "state": {
                    "code": geocode["cc"],
                    "name": geocode["admin1"],
                    "country": {
                        "code": geocode["cc"],
                        "name": geocode["cc"],
                    }
                }
            }
        except:
            return {}

    def on_location_update(self, lat, lon):
        LOG.debug(f"Latitude: {lat} Longitude: {lon}")
        # use self.gps for extra decimal places
        self.location["coordinate"] = {
            "latitude": self.gps.lat,
            "longitude": self.gps.lon
        }
        tz = self.get_tz(lat=self.gps.lat, lon=self.gps.lon)
        LOG.debug(f"Timezone: {tz}")
        if tz:
            self.location["timezone"] = tz
        geocode = self.reverse_geocode(self.gps.lat, self.gps.lon)
        LOG.debug(f"Geocode: {geocode}")
        if geocode:
            self.location["city"] = geocode

        # TODO update config
        self.emit("location", self.location)


class GPSDaemon(threading.Thread):
    def __init__(self, decimal_places=5, host="127.0.0.1", port=2947, daemonic=True):
        super(GPSDaemon, self).__init__()
        if daemonic:
            self.setDaemon(True)
        self.client = GPSDClient(host=host, port=port)
        self.data_points = []
        self.decimal_places = decimal_places
        self.speed = self.alt = self.lat = self.lon = None

    def on_location_update(self, lat, lon):
        LOG.debug(f"Latitude: {lat} Longitude: {lon}")

    def run(self) -> None:
        for result in self.client.dict_stream():
            if result["class"] == "TPV":
                if result.get("lat"):
                    prev_lat = self.lat
                    prev_lon = self.lon

                    # keep a rolling average to smooth results
                    self.data_points.append(result)
                    self.data_points = self.data_points[-15:]
                    self.lat = sum(float(s.get("lat", 0)) for s in self.data_points) / len(self.data_points)
                    self.lon = sum(float(s.get("lon", 0)) for s in self.data_points) / len(self.data_points)
                    self.speed = sum(float(s.get("speed", 0)) for s in self.data_points) / len(self.data_points)
                    self.alt = sum(float(s.get("alt", 0)) for s in self.data_points) / len(self.data_points)

                    # location update event
                    rounded_lat = round(self.lat, self.decimal_places)
                    rounded_lon = round(self.lon, self.decimal_places)
                    if not prev_lat or not prev_lon:
                        self.on_location_update(rounded_lat, rounded_lon)
                    elif rounded_lat != round(prev_lat, self.decimal_places) or \
                            rounded_lon != round(prev_lon, self.decimal_places):
                        self.on_location_update(rounded_lat, rounded_lon)
