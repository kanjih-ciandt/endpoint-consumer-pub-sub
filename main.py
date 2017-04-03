# Copyright 2016 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# [START imports]

import endpoints
from protorpc import messages
from protorpc import remote
import logging
from google.cloud import pubsub

##TOPIC = 'xpto-develop-All'
##SUBSCRIPTION = 'test-k'


# [END imports]


# [START messages]

class PullResponse(messages.Message):
    message_data = messages.StringField(1)
    message_attribute_kind = messages.StringField(2)
    message_id = messages.StringField(3)
    messageid = messages.StringField(4)
    publish_time = messages.StringField(5)
    publishtime = messages.StringField(6)
    topic_name = messages.StringField(7)
    subscription = messages.StringField(8)

SUBSCRIBER_RESOURCE = endpoints.ResourceContainer(
    topic_name=messages.StringField(1, required=True),
    subscription=messages.StringField(2, required=True))
# [END messages]


# [START greeting_api]
@endpoints.api(name='clientpubsub', version='v1')
class PubSubClientApi(remote.Service):

    @endpoints.method(
        SUBSCRIBER_RESOURCE,
        PullResponse,
        path='pull', http_method='GET',
        name='pull.get'
    )
    def get_pull(self, request):

        pubsub_client = pubsub.Client()
        topic = pubsub_client.topic(request.topic_name)
        subscription = topic.subscription(request.subscription)

        # Change return_immediately=False to block until messages are
        # received.
        results = subscription.pull(return_immediately=True)

        logging.info('Received {} messages.'.format(len(results)))
        logging.info(results[:])

        # for ack_id, message in results:
        #     logging.info('* {}: {}, {}'.format(
        #         message.message_id, message.data, message.attributes))

        ack_id, message = results[0]
        logging.info(message.__dict__)
        # request.id is used to access the URL parameter.
        return PullResponse(message_data=str(message.data),
                            message_attribute_kind=str(message.attributes),
                            message_id=message.message_id,
                            messageid= message.message_id,
                            publish_time='publish_time',
                            publishtime='publishtime',
                            topic_name=request.topic_name,
                            subscription=request.subscription)




# [START api_server]
api = endpoints.api_server([PubSubClientApi])
# [END api_server]
