#!/usr/bin/env python3
from setuptools import setup

PLUGIN_ENTRY_POINT = 'ovos-phal-plugin-gpsd=ovos_phal_plugin_gpsd:GPSDPlugin'
setup(
    name='ovos-phal-plugin-gpsd',
    version='0.0.1a0',
    description='A PHAL plugin for mycroft',
    url='https://github.com/OpenVoiceOS/ovos-PHAL-plugin-gpsd',
    author='JarbasAi',
    author_email='jarbasai@mailfence.com',
    license='Apache-2.0',
    packages=['ovos_phal_plugin_gpsd'],
    install_requires=["ovos-plugin-manager>=0.0.1",
                      "gpsdclient",
                      "reverse_geocoder",
                      "python-geoip-geolite2",
                      "timezonefinder"],
    zip_safe=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Text Processing :: Linguistic',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    entry_points={'ovos.plugin.phal': PLUGIN_ENTRY_POINT}
)
