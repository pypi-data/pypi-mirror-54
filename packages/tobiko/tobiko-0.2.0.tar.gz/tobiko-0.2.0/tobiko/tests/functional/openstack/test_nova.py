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

import os

import testtools

import tobiko

from tobiko.openstack import nova
from tobiko.openstack import stacks


class KeyPairTest(testtools.TestCase):

    stack = tobiko.required_setup_fixture(stacks.KeyPairStackFixture)

    def test_key_files(self):
        self.assertTrue(os.path.isfile(self.stack.key_file))
        self.assertTrue(os.path.isfile(self.stack.key_file + '.pub'))


class ClientTest(testtools.TestCase):

    #: Stack of resources with a server attached to a floating IP
    stack = tobiko.required_setup_fixture(stacks.CirrosServerStackFixture)

    @nova.skip_if_missing_hypervisors(count=1)
    def test_list_hypervisors(self):
        hypervisors = nova.list_hypervisors()
        self.assertTrue(hypervisors)
        self.assertEqual(1, hypervisors[0].id)
        self.assertTrue(hasattr(hypervisors[0], 'cpu_info'))

    @nova.skip_if_missing_hypervisors(count=1)
    def test_list_hypervisors_without_details(self):
        hypervisors = nova.list_hypervisors(detailed=False)
        self.assertTrue(hypervisors)
        self.assertEqual(1, hypervisors[0].id)
        self.assertFalse(hasattr(hypervisors[0], 'cpu_info'))

    @nova.skip_if_missing_hypervisors(count=1)
    def test_list_hypervisors_with_hypervisor_hostname(self):
        hypervisor = nova.list_hypervisors()[0]
        hypervisors = nova.list_hypervisors(
            hypervisor_hostname=hypervisor.hypervisor_hostname)
        self.assertEqual([hypervisor], hypervisors)

    @nova.skip_if_missing_hypervisors(count=1)
    def test_find_hypervisor(self):
        hypervisor = nova.find_hypervisor()
        self.assertIsNotNone(hypervisor)

    @nova.skip_if_missing_hypervisors(count=2)
    def test_find_hypervisor_with_unique(self):
        self.assertRaises(tobiko.MultipleObjectsFound, nova.find_hypervisor,
                          unique=True)

    @nova.skip_if_missing_hypervisors(count=2)
    def test_find_hypervisor_without_unique(self):
        hypervisor = nova.find_hypervisor()
        self.assertIsNotNone(hypervisor)

    def test_get_console_output(self):
        output = nova.get_console_output(server=self.stack.server_id,
                                         length=50,
                                         timeout=60.)
        self.assertTrue(output)

    def test_list_servers(self):
        server_id = self.stack.server_id
        for server in nova.list_servers():
            if server_id == server.id:
                break
        else:
            self.fail('Server {} not found'.format(server_id))

    def test_find_server(self):
        server_id = self.stack.server_id
        server = nova.find_server(id=server_id, unique=True)
        self.assertEqual(server_id, server.id)


class HypervisorTest(testtools.TestCase):

    def test_skip_if_missing_hypervisors(self, count=1, should_skip=False,
                                         **params):
        if should_skip:
            expected_exeption = self.skipException
        else:
            expected_exeption = self.failureException

        @nova.skip_if_missing_hypervisors(count=count, **params)
        def method():
            raise self.fail('Not skipped')

        exception = self.assertRaises(expected_exeption, method)
        if should_skip:
            hypervisors = nova.list_hypervisors(**params)
            message = "missing {!r} hypervisor(s)".format(
                count - len(hypervisors))
            if params:
                message += " with {!s}".format(
                    ','.join('{!s}={!r}'.format(k, v)
                             for k, v in params.items()))
            self.assertEqual(message, str(exception))
        else:
            self.assertEqual('Not skipped', str(exception))

    def test_skip_if_missing_hypervisors_with_no_hypervisors(self):
        self.test_skip_if_missing_hypervisors(id=-1,
                                              should_skip=True)

    def test_skip_if_missing_hypervisors_with_big_count(self):
        self.test_skip_if_missing_hypervisors(count=1000000,
                                              should_skip=True)
