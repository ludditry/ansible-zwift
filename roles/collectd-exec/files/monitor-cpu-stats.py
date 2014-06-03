#!/usr/bin/python

import socket
import time
import sys

interval = 10
hostname = socket.gethostname()

def get_stats():
    cpu_info = ('user', 'nice', 'sys', 'idle', 'iowait',
                'hardirq', 'softirq', 'steal', 'guest', 'guest_nice')

    with open('/proc/stat', 'r') as fd:
        stats = fd.read().split('\n')
    
    stat_dict = {}

    for stat in stats:
        if stat == '':
            continue

        stat_array = stat.split()

        if(stat_array[0].startswith('cpu')):
            stat_dict[stat_array[0]] = dict(
                zip(cpu_info, [int(x) for x in stat_array[1:]]))

    return stat_dict

def print_stats(last_stats, stats, interval, epoch):
    for cpu in stats:
        last_total_ticks = sum(last_stats[cpu].values(), 0)
        total_ticks = sum(stats[cpu].values(), 0)

        ticks_this_interval = total_ticks - last_total_ticks

        for value in stats[cpu].keys():
            ticks = stats[cpu][value] - last_stats[cpu][value]

            percent = (ticks * 100) / ticks_this_interval

            print 'PUTVAL "%s/altcpu-%s/gauge-%s" interval=%d %s:%d' % (
                hostname, cpu, value, interval, epoch, percent)


if __name__ == '__main__':
    last_stats = get_stats()
    time.sleep(interval)

    while(True):
        epoch = int(time.time())
        stats = get_stats()
        print_stats(last_stats, stats, interval, epoch)
        sys.stdout.flush()
        last_stats = stats

        time.sleep(interval)

