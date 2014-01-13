# Copyright (c) 2014 Ron Pedde <ron@pedde.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from ansible import utils, errors
import os
import ipaddr

class LookupModule(object):

    def __init__(self, basedir=None, **kwargs):
        self.basedir = basedir

    def templatize(self, term, inject=None):
        return utils.template.template(self.basedir, term, inject)

    def run(self, terms, inject=None, **kwargs):
        terms = utils.listify_lookup_plugin_terms(terms, self.basedir, inject)

        if isinstance(terms, basestring):
            terms = [ terms ]

        ret = []

        hostname = kwargs['vars'].get('inventory_hostname', 'unknown')

        for term in terms:
            termlist = term.split()
            termdict = dict([(item.split('=', 1)[0],
                              self.templatize(item.split('=', 1)[1], inject))
                             for item in termlist])


            hostvars = kwargs['vars']
            if 'host' in termdict:
                hostvars = kwargs['vars']['hostvars'].get(termdict['host'], {})

            # sensible defaults?
            cidr = termdict.get('cidr', '0.0.0.0/32')

            net = ipaddr.IPv4Network(cidr)

            found_addr = None

            for addr in hostvars.get('ansible_all_ipv4_addresses', []):
                if ipaddr.IPv4Address(addr) in net:
                    found_addr = addr

            # for iface in kwargs['vars'].get('ansible_interfaces', []):
            #     addrs = kwargs['vars'].get('ansible_%s' % iface, {}).get('ipv4', [])
            #     if isinstance(addrs, dict):
            #         addrs = [ addrs ]

            #     for addr in addrs:
            #         if 'address' in addr and ipaddr.IPv4Address(addr['address']) in net:
            #             found_addr = addr['address']

            if found_addr is None:
                # raise?
                found_addr = hostvars.get('ansible_default_ipv4', '0.0.0.0')

            ret.append(found_addr)

        return ret
