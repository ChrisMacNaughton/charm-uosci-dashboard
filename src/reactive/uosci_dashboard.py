# Copyright 2018 Canonical Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import subprocess
import charmhelpers.core.hookenv as hookenv
from charms.reactive import when, when_not, set_state
from charms.layer.nginx import configure_site


@when('nginx.available')
def configure_website():
    config = hookenv.config()
    configure_site('uosci_dashboard', 'uosci.conf', app_path='/var/www/html')
    subprocess.check_call(['uosci-dashboard', '--path', '/var/www/html'])
    hookenv.open_port('80')
    hookenv.status_set('active', 'UOSCI Dashboard is now available')
    set_state('dashboard.init')

@when('dashboard.init')
@when_not('crontab.installed')
def setup_crontab():
    crontab_file = """#!/bin/bash
    uosci-dashboard --path=/var/www/html
    """
    with open("/etc/cron.hourly/uosci_dashboard", 'w') as f:
        f.write(crontab_file)
    set_state('crontab.installed')