#!/usr/bin/env python

import alerter
import time
import socket

CONF = alerter.config.CONF
LOG = alerter.log.LOG
ALERTER = alerter.alert.ALERTER
HOSTNAME = socket.gethostname()
SOCKET_PATH = "/var/run/haproxy.sock"


def get_stats():
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    stats = ""
    sock.connect(SOCKET_PATH)
    sock.send("show stat\n")
    while True:
        b = sock.recv(1024)
        stats += b
        if b == "":
            break
    return parse_stats_string(stats)


def parse_stats_string(s):
    stat_lines = s.strip().split("\n")
    fields = stat_lines[0]
    del stat_lines[0]
    fields = fields.strip("#").strip(",").strip().split(",")
    return [dict(zip(fields, line.split(",")))
            for line in stat_lines]


def get_down_backends(parsed_stats):
    return [x for x in parsed_stats if x["svname"] == "BACKEND"
            and x["status"] != "UP"]


def get_up_backends(parsed_stats):
    return [x for x in parsed_stats if x["svname"] == "BACKEND"
            and x["status"] == "UP"]


def check_haproxy():
    try:
        stats = get_stats()
        down_backends = get_down_backends(stats)
    except socket.error, msg:
        ALERTER.failure("haproxy-socket",
                        "stats socket error",
                        host=HOSTNAME,
                        description="Unable to connect to socket '%s': %s" % (
                            SOCKET_PATH, msg))
        return False
    ALERTER.okay("haproxy-socket",
                 "stats socket available",
                 host=HOSTNAME,
                 description="haproxy stats socket available")
    for backend in down_backends:
        ALERTER.failure(
            "haproxy-backend-%s" % backend["pxname"],
            "haproxy backend '%s' down" % backend["pxname"],
            host=HOSTNAME,
            description="haproxy backend down: '%s': '%s'" % (
                backend["pxname"], backend["status"]))
    for backend in get_up_backends(stats):
        ALERTER.okay(
            "haproxy-backend-%s" % backend["pxname"],
            "haproxy backend '%s' up" % backend["pxname"],
            host=HOSTNAME,
            description="haproxy backend '%s' available." % backend["pxname"])
    if len(down_backends) > 0:
        return False
    return True


def add_to_pool():
    pass


def remove_from_pool():
    pass


def main():
    interval = CONF.get("interval", 10)
    while True:
        try:
            if check_haproxy():
                add_to_pool()
            else:
                remove_from_pool()
            time.sleep(interval)
            ALERTER.okay(
                "haproxy-monitoring",
                "haproxy monitoring succeeded",
                HOSTNAME,
                description="haproxy monitoring succeeded.")
        except Exception, msg:
            ALERTER.failure(
                "haproxy-monitoring",
                "haproxy monitoring exception",
                HOSTNAME,
                description="haproxy monitoring unexpectedly excepted: %s" % (
                    msg))


if __name__ == "__main__":
    main()
