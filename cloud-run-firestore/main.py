import os
import time
import firebase_admin
import google.auth.credentials
from datetime import datetime
from random import randint
from firebase_admin import credentials
from firebase_admin import firestore
from flask import Flask, jsonify, request

if os.getenv('GOOGLE_APPLICATION_CREDENTIALS', '') != '':
    # Use a service account
    firebase_admin.initialize_app()
    db = firestore.client()
else:
    # Use emulator
    # os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8000"
    # os.environ["FIRESTORE_PROJECT_ID"] = "asomas"

    from unittest import mock
    credentials = mock.Mock(spec=google.auth.credentials.Credentials)
    db = firestore.Client(project=os.environ.get('FIRESTORE_PROJECT_ID'), credentials=credentials)

app = Flask(__name__)

@app.route('/')
def hello_world():
    target = os.environ.get('TARGET', 'World')
    return jsonify({'message': 'Hello {}!\n'.format(target)})

@app.route('/logs', methods=['GET', 'POST'])
def log():
    # add data
    now = datetime.now()
    id = str(int(time.time()))
    doc_ref = db.collection(u'logs').document(id)
    doc_ref.set({
        u'value': request.json['value'],
        u'timestamp': now,
    }, merge=True)
    return jsonify(doc_ref.get().to_dict())


if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 5000)))
