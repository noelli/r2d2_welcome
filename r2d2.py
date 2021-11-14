# coding=utf-8
import time
from time import sleep

from pylgbst import *
from pylgbst.hub import MoveHub
from pylgbst.peripherals import EncodedMotor, TiltSensor, Current, Voltage, COLORS, COLOR_BLACK

log = logging.getLogger("demo")


def led_colors(movehub):
    # LED colors demo
    log.info("LED colors demo")

    # We get a response with payload and port, not x and y here...
    def color_callback(named):
        log.info("LED Color callback: %s", named)

    movehub.led.subscribe(color_callback)
    for color in list(COLORS.keys())[1:] + [COLOR_BLACK]:
        log.info("Setting LED color to: %s", COLORS[color])
        movehub.led.set_color(color)
        sleep(1)


def get_options():
    import argparse
    arg_parser = argparse.ArgumentParser(
        description='Demonstrate move-hub communications',
    )
    arg_parser.add_argument(
        '-c', '--connection',
        default='auto://',
        help='''Specify connection URL to use, `protocol://mac?param=X` with protocol in:
    "gatt","pygatt","gattlib","gattool", "bluepy","bluegiga"'''
    )
    return arg_parser


def connection_from_url(url):
    import pylgbst
    if url == 'auto://':
        return None
    try:
        from urllib.parse import urlparse, parse_qs
    except ImportError:
        from urlparse import urlparse, parse_qs
    parsed = urlparse(url)
    name = 'get_connection_%s' % parsed.scheme
    factory = getattr(pylgbst, name, None)
    if not factory:
        msg = "Unrecognised URL scheme/protocol, expect a get_connection_<protocol> in pylgbst: %s"
        raise ValueError(msg % parsed.protocol)
    params = {}
    if parsed.netloc.strip():
        params['hub_mac'] = parsed.netloc
    for key, value in parse_qs(parsed.query).items():
        if len(value) == 1:
            params[key] = value[0]
        else:
            params[key] = value
    return factory(
        **params
    )


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(relativeCreated)d\t%(levelname)s\t%(name)s\t%(message)s')
    try:
        import local_settings
        connection = get_connection_bluepy(hub_mac=local_settings.mac) # connection_from_url("bluepy://")
    except ValueError as err:
        log.warning("%s", err)
    
    i = True
    while i:
        try:
            hub = MoveHub(connection=connection)
        except err:
            log.warning("%s", err)
        finally:
            i = False

    i = True
    while i:
        x = input("Beenden? Dann > 0")
        if x > 0:
            i = False
        try:
            led_colors(hub)
        except err:
            log.warning("%s", err)
    hub.disconnect()

