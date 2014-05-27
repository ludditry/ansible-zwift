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

        for term in terms:
            found_iface = "eth0"

            net = ipaddr.IPv4Network(term)
            for iface in kwargs['vars'].get('ansible_interfaces', []):
                addrs = kwargs['vars'].get('ansible_%s' % iface, {}).get('ipv4', [])
                if isinstance(addrs, dict):
                    addrs = [addrs]

                for addr in addrs:
                    if 'address' in addr and ipaddr.IPv4Address(addr['address']) in net:
                        found_iface = iface

            ret.append(found_iface)
        return ret
