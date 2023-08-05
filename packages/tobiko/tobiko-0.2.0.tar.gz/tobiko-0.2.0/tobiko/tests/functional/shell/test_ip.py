# Copyright (c) 2019 Red Hat, Inc.
#
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
from __future__ import absolute_import

import netaddr
import six
import testtools

import tobiko
from tobiko.shell import ip
from tobiko.shell import ssh
from tobiko.openstack import stacks


class IpTest(testtools.TestCase):

    centos_stack = tobiko.required_setup_fixture(
        stacks.CentosServerStackFixture)

    cirros_stack = tobiko.required_setup_fixture(
        stacks.CirrosServerStackFixture)

    ubuntu_stack = tobiko.required_setup_fixture(
        stacks.UbuntuServerStackFixture)

    def test_list_ip_addresses(self, ip_version=None, scope=None,
                               **execute_params):
        ips = ip.list_ip_addresses(ip_version=ip_version, scope=scope,
                                   **execute_params)
        self.assertIsInstance(ips, tobiko.Selection)
        for ip_address in ips:
            self.assertIsInstance(ip_address, netaddr.IPAddress)
        if ip_version:
            self.assertEqual(ips.with_attributes(version=ip_version), ips)
        if scope:
            if scope == 'link':
                self.assertEqual(ips.with_attributes(version=4), [])
                self.assertEqual(ips.with_attributes(version=6), ips)
            elif scope == 'host':
                self.assertEqual(ips.with_attributes(version=4),
                                 [netaddr.IPAddress('127.0.0.1')])
                self.assertEqual(ips.with_attributes(version=6),
                                 [netaddr.IPAddress('::1')])
            elif scope == 'global':
                self.assertNotIn(netaddr.IPAddress('127.0.0.1'), ips)
                self.assertNotIn(netaddr.IPAddress('::1'), ips)

    def test_list_ip_addresses_with_host_scope(self, **execute_params):
        self.test_list_ip_addresses(scope='host', **execute_params)

    def test_list_ip_addresses_with_link_scope(self, **execute_params):
        self.test_list_ip_addresses(scope='link', **execute_params)

    def test_list_ip_addresses_with_global_scope(self, **execute_params):
        self.test_list_ip_addresses(scope='global', **execute_params)

    def test_list_ip_addresses_with_ipv4(self):
        self.test_list_ip_addresses(ip_version=4)

    def test_list_ip_addresses_with_ipv6(self):
        self.test_list_ip_addresses(ip_version=6)

    def test_list_ip_addresses_with_centos_server(self):
        self.test_list_ip_addresses(ssh_client=self.centos_stack.ssh_client)

    def test_list_ip_addresses_with_cirros_server(self):
        self.test_list_ip_addresses(ssh_client=self.cirros_stack.ssh_client)

    def test_list_ip_addresses_with_ubuntu_server(self):
        self.test_list_ip_addresses(ssh_client=self.ubuntu_stack.ssh_client)

    def test_list_ip_addresses_with_proxy_ssh_client(self):
        ssh_client = ssh.ssh_proxy_client()
        if ssh_client is None:
            self.skip('SSH proxy server not configured')
        self.test_list_ip_addresses(ssh_client=ssh_client)

    def test_list_ip_addresses_with_proxy_ssh_client_and_host_scope(
                self, **execute_params):
        self.test_list_ip_addresses(scope='host', **execute_params)

    def test_list_ip_addresses_with_proxy_ssh_client_and_link_scope(
                self, **execute_params):
        self.test_list_ip_addresses(scope='link', **execute_params)

    def test_list_ip_addresses_with_proxy_ssh_client_and_global_scope(
                self, **execute_params):
        self.test_list_ip_addresses(scope='global', **execute_params)

    def test_list_namespaces(self, **execute_params):
        namespaces = ip.list_network_namespaces(**execute_params)
        self.assertIsInstance(namespaces, list)
        for namespace in namespaces:
            self.assertIsInstance(namespace, six.string_types)
            self.test_list_ip_addresses(network_namespace=namespace)

    def test_list_namespaces_with_centos_server(self):
        self.test_list_namespaces(ssh_client=self.centos_stack.ssh_client)

    def test_list_namespaces_with_ubuntu_server(self):
        self.test_list_namespaces(ssh_client=self.ubuntu_stack.ssh_client)

    def test_list_namespaces_with_proxy_ssh_client(self):
        ssh_client = ssh.ssh_proxy_client()
        if ssh_client is None:
            self.skip('SSH proxy server not configured')
        self.test_list_namespaces(ssh_client=ssh_client)
