from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.exceptions import AuthenticationFailed, NotFound
from rest_framework import status
from google.cloud import pubsub_v1

import json
import base64
import google.auth
import logging
logger = logging.getLogger(__name__)

service_name = 'Gamma'
publisher = pubsub_v1.PublisherClient()
cred, project = google.auth.default()

received_messages = []


@api_view(['GET'])
def index(request: Request):
    res = {
        'message': f'this is {service_name} service',
        'headers': request.headers,
    }
    return Response(res, status=status.HTTP_200_OK)


@api_view(['POST'])
def action(request: Request):
    """
    PubSub-push-subscription-compatible endpoint
    Extracts "message" from the payload and appends it to static received_messages
    :param request:
    :return:
    """
    body = request.data
    headers = request.headers
    if 'message' in body:
        # body['message']
        # {
        #     "data": "eyJtZXNzYWdlIjogImhlbGxvIn0=",
        #     "messageId": "1844899979127750",
        #     "message_id": "1844899979127750",
        #     "publishTime": "2020-12-14T14:58:51.443Z",
        #     "publish_time": "2020-12-14T14:58:51.443Z"
        # }
        if 'data' in body['message']:
            data = json.loads(base64.b64decode(body['message']['data']))
            if 'message' in data:
                received_messages.append(data['message'])
    res = {
        'headers': headers,
        'message': f'{service_name} action success', 
    }
    return Response(res, status=status.HTTP_200_OK)


@api_view(['GET'])
def messages(request: Request):
    """
    Display received_messages
    :param request:
    :return:
    """
    res = {
        'message': f'this is {service_name} service',
        'received_messages': received_messages,
    }
    return Response(res, status=status.HTTP_200_OK)


@api_view(['POST'])
def publish(request: Request):
    """
    Publish message containing "message" field to PubSub topic "hello"
    :param request:
    :return:
    """
    if 'message' in request.data:
        topic = 'hello'
        topic_path = publisher.topic_path(project, topic)
        data = {
            'message': request.data['message'],
        }
        future = publisher.publish(topic_path, json.dumps(data).encode('utf-8'))
        res = future.result()
        logger.info(res)
        return Response({"result": str(res)}, status=status.HTTP_200_OK)
    else:
        return Response({"message": "this field is required"}, status=status.HTTP_400_BAD_REQUEST)
