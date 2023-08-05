# Copyright 2019 Red Hat
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

import tobiko
from tobiko import config
from tobiko.openstack import glance
from tobiko.openstack.stacks import _nova

CONF = config.CONF

FEDORA_IMAGE_URL = \
    ('https://download.fedoraproject.org/pub/fedora/linux/releases/'
     '30/Cloud/x86_64/images/Fedora-Cloud-Base-30-1.2.x86_64.qcow2')


class FedoraImageFixture(glance.URLGlanceImageFixture):

    image_url = CONF.tobiko.fedora.image_url or FEDORA_IMAGE_URL
    image_name = CONF.tobiko.fedora.image_name
    image_file = CONF.tobiko.fedora.image_file
    disk_format = CONF.tobiko.fedora.disk_format or "qcow2"
    container_format = CONF.tobiko.fedora.container_format or "bare"
    username = CONF.tobiko.fedora.username or 'fedora'
    password = CONF.tobiko.fedora.password


class FedoraFlavorStackFixture(_nova.FlavorStackFixture):
    ram = 512


class FedoraServerStackFixture(_nova.ServerStackFixture):

    #: Glance image used to create a Nova server instance
    image_fixture = tobiko.required_setup_fixture(FedoraImageFixture)

    #: Glance image used to create a Nova server instance
    flavor_stack = tobiko.required_setup_fixture(FedoraFlavorStackFixture)
