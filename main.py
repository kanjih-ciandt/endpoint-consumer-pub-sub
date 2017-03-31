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
from protorpc import message_types
from protorpc import messages
from protorpc import remote
# [END imports]


# [START messages]
class Greeting(messages.Message):
    """Greeting that stores a message."""
    message = messages.StringField(1)


class GreetingCollection(messages.Message):
    """Collection of Greetings."""
    items = messages.MessageField(Greeting, 1, repeated=True)


STORED_GREETINGS = GreetingCollection(items=[
    Greeting(message='hello world!'),
    Greeting(message='goodbye world!'),
])


class PullResponse(messages.Message):
    message_data = messages.StringField(1)
    message_attribute_kind = messages.StringField(2)
    message_id = messages.StringField(3)
    messageid = messages.StringField(4)
    publish_time = messages.StringField(5)
    publishtime = messages.StringField(6)
    url = messages.StringField(7)

SUBSCRIBER_RESOURCE = endpoints.ResourceContainer(
    subscriber=messages.StringField(1, required=True))
# [END messages]


# [START greeting_api]
@endpoints.api(name='clientpubsub', version='v1')
class GreetingApi(remote.Service):

    @endpoints.method(
        SUBSCRIBER_RESOURCE,
        PullResponse,
        path='pull', http_method='GET',
        name='pull.get'
    )
    def get_pull(self, request):

        # request.id is used to access the URL parameter.
        return PullResponse(message_data='message_data',
                            message_attribute_kind='message_attribute_kind',
                            message_id='message_id',
                            messageid='messageid',
                            publish_time='publish_time',
                            publishtime='publishtime',
                            url=request.subscriber)

    # [END multiply]


# [START api_server]
api = endpoints.api_server([GreetingApi])
# [END api_server]
