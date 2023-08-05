# Copyright 2018 Red Hat
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

from tobiko.common import _asserts
from tobiko.common import _detail
from tobiko.common import _exception
from tobiko.common import _fixture
from tobiko.common import _logging
from tobiko.common.managers import testcase as testcase_manager
from tobiko.common.managers import loader as loader_manager
from tobiko.common import _os
from tobiko.common import _select
from tobiko.common import _skip


details_content = _detail.details_content

FailureException = _asserts.FailureException
fail = _asserts.fail

TobikoException = _exception.TobikoException
check_valid_type = _exception.check_valid_type
exc_info = _exception.exc_info

is_fixture = _fixture.is_fixture
get_fixture = _fixture.get_fixture
fixture_property = _fixture.fixture_property
required_fixture = _fixture.required_fixture
required_setup_fixture = _fixture.required_setup_fixture
get_fixture_name = _fixture.get_fixture_name
get_fixture_class = _fixture.get_fixture_class
get_fixture_dir = _fixture.get_fixture_dir
remove_fixture = _fixture.remove_fixture
reset_fixture = _fixture.reset_fixture
setup_fixture = _fixture.setup_fixture
cleanup_fixture = _fixture.cleanup_fixture
list_required_fixtures = _fixture.list_required_fixtures
SharedFixture = _fixture.SharedFixture
FixtureManager = _fixture.FixtureManager

CaptureLogTest = _logging.CaptureLogTest
CaptureLogFixture = _logging.CaptureLogFixture

load_object = loader_manager.load_object
load_module = loader_manager.load_module

makedirs = _os.makedirs
open_output_file = _os.open_output_file

discover_testcases = testcase_manager.discover_testcases

Selection = _select.Selection
select = _select.select
ObjectNotFound = _select.ObjectNotFound
MultipleObjectsFound = _select.MultipleObjectsFound

SkipException = _skip.SkipException
skip = _skip.skip
skip_if = _skip.skip_if
skip_unless = _skip.skip_unless


from tobiko import config  # noqa
config.init_config()
