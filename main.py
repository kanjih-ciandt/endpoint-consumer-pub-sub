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
@endpoints.api(name='greeting', version='v1')
class GreetingApi(remote.Service):

    @endpoints.method(
        # This method does not take a request message.
        message_types.VoidMessage,
        # This method returns a GreetingCollection message.
        GreetingCollection,
        path='greetings',
        http_method='GET',
        name='greetings.list')
    def list_greetings(self, unused_request):
        return STORED_GREETINGS

    # ResourceContainers are used to encapsuate a request body and url
    # parameters. This one is used to represent the Greeting ID for the
    # greeting_get method.
    GET_RESOURCE = endpoints.ResourceContainer(
        # The request body should be empty.
        message_types.VoidMessage,
        # Accept one url parameter: an integer named 'id'
        id=messages.IntegerField(1, variant=messages.Variant.INT32))

    @endpoints.method(
        # Use the ResourceContainer defined above to accept an empty body
        # but an ID in the query string.
        GET_RESOURCE,
        # This method returns a Greeting message.
        Greeting,
        # The path defines the source of the URL parameter 'id'. If not
        # specified here, it would need to be in the query string.
        path='greetings/{id}',
        http_method='GET',
        name='greetings.get')
    def get_greeting(self, request):
        try:
            # request.id is used to access the URL parameter.
            return STORED_GREETINGS.items[request.id]
        except (IndexError, TypeError):
            raise endpoints.NotFoundException(
                'Greeting {} not found'.format(request.id))
    # [END greeting_api]

    # [START multiply]
    # This ResourceContainer is similar to the one used for get_greeting, but
    # this one also contains a request body in the form of a Greeting message.
    MULTIPLY_RESOURCE = endpoints.ResourceContainer(
        Greeting,
        times=messages.IntegerField(2, variant=messages.Variant.INT32,
                                    required=True))

    @endpoints.method(
        # This method accepts a request body containing a Greeting message
        # and a URL parameter specifying how many times to multiply the
        # message.
        MULTIPLY_RESOURCE,
        # This method returns a Greeting message.
        Greeting,
        path='greetings/multiply/{times}',
        http_method='POST',
        name='greetings.multiply')
    def multiply_greeting(self, request):
        return Greeting(message=request.message * request.times)

    @endpoints.method(
        SUBSCRIBER_RESOURCE,
        PullResponse,
        path='requesters', http_method='GET',
        name='requesters.get'
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
