# (C) Copyright 2015,2016 Hewlett Packard Enterprise Development LP
# Copyright 2017 Fujitsu LIMITED
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import requests
import ujson as json

from debtcollector import removals
from oslo_config import cfg

from monasca_notification.plugins import abstract_notifier

CONF = cfg.CONF


def register_opts(conf):
    gr = cfg.OptGroup(name='%s_notifier' % WebhookNotifier.type)
    opts = [
        cfg.IntOpt(name='timeout', default=5, min=1)
    ]

    conf.register_group(gr)
    conf.register_opts(opts, group=gr)


class WebhookNotifier(abstract_notifier.AbstractNotifier):

    type = 'webhook'

    def __init__(self, log):
        super(WebhookNotifier, self).__init__()
        self._log = log

    @removals.remove(
        message='Configuration of notifier is available through oslo.cfg',
        version='1.9.0',
        removal_version='3.0.0'
    )
    def config(self, config_dict):
        pass

    @property
    def statsd_name(self):
        return 'sent_webhook_count'

    def send_notification(self, notification):
        """Send the notification via webhook
            Posts on the given url
        """

        body = {'alarm_id': notification.alarm_id,
                'alarm_definition_id': notification.raw_alarm['alarmDefinitionId'],
                'alarm_name': notification.alarm_name,
                'alarm_description': notification.raw_alarm['alarmDescription'],
                'alarm_timestamp': notification.alarm_timestamp,
                'state': notification.state,
                'old_state': notification.raw_alarm['oldState'],
                'message': notification.message,
                'tenant_id': notification.tenant_id,
                'metrics': notification.metrics}

        headers = {'content-type': 'application/json'}

        url = notification.address

        try:
            # Posting on the given URL
            result = requests.post(url=url,
                                   data=json.dumps(body),
                                   headers=headers,
                                   timeout=CONF.webhook_notifier.timeout)

            if result.status_code in range(200, 300):
                self._log.info("Notification successfully posted.")
                return True
            else:
                self._log.error("Received an HTTP code {} when trying to post on URL {}."
                                .format(result.status_code, url))
                return False
        except Exception:
            self._log.exception("Error trying to post on URL {}".format(url))
            return False
