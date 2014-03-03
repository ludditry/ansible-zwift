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

    def run(self, terms, inject=None, **kwargs):
        terms = utils.listify_lookup_plugin_terms(terms, self.basedir, inject)

        if isinstance(terms, basestring):
            terms = [ terms ]

        ret = []

        for term in terms:
            # only term we have is a cidr
            if not 'hostvars' in kwargs['vars']:
                ret.append(['127.0.0.1:11211'])
                break

            this_result = []
            net = ipaddr.IPv4Network(term)

            for host in kwargs['vars']['hostvars']:
                hostvars = kwargs['vars']['hostvars'][host]

                if not 'groups' in kwargs['vars'] or (not 'proxy' in kwargs['vars']['groups'] and
                                                      not 'auth-proxy' in kwargs['vars']['groups']):
                    continue

                if host not in kwargs['vars']['groups'].get('proxy', []) and \
                   host not in kwargs['vars']['groups'].get('auth-proxy', []):
                    continue


                found_addr = None

                for addr in hostvars.get('ansible_all_ipv4_addresses', []):
                    if ipaddr.IPv4Address(addr) in net:
                        found_addr = addr

                if found_addr is not None:
                    this_result.append(found_addr)

            if len(this_result) == 0:
                ret.append('127.0.0.1:11211')
            else:
                ret.append(','.join(['%s:11211' % x for x in this_result]))

        return ret
