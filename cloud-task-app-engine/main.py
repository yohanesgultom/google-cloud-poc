import os
import json
from datetime import datetime
from flask import Flask, jsonify, request
from google.cloud import tasks_v2
from google.protobuf import timestamp_pb2

app = Flask(__name__)


@app.route('/')
def hello_world():
    return jsonify({'message': 'Hello world!'})

@app.route('/submit-task', methods=['POST'])
def submit_task():
    # config
    project = 'metal-arc-273007'
    queue = 'cloud-run-queue'
    location = 'us-central1'
    
    # data
    data = { 'value': request.json['value'] }
    task = {
        'http_request': {
            'http_method': 'POST',
            'url': 'https://cloud-run-firestore-alhodubq5q-uc.a.run.app/logs',
            'headers': {
                'Content-Type': 'application/json',
                'Send-By': 'cloud-task-app-engine',
            },
            'body': json.dumps(data).encode('UTF-8'),
        }
    }

    # submit
    client = tasks_v2.CloudTasksClient()
    parent = client.queue_path(project, location, queue)
    response = client.create_task(parent, task)
    print(response)
    return jsonify({'message': f'Created task {response.name}'})


if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.getenv('PORT', 5000)))